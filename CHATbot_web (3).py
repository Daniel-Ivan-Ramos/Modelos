from flask import Flask, request, jsonify, render_template
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import random
import json
import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


app = Flask(__name__)
# Cargar las preguntas y respuestas desde el archivo JSON
with open('preguntas.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Crear listas para las preguntas y respuestas de todas las categorías
questions = []
answers = []

# Recopilar preguntas y respuestas de todas las categorías
for category, items in data.items():
    if isinstance(items, list):
        for item in items:
            if 'questions' in item and 'answer' in item:
                questions.extend(item['questions'])
                answers.extend([item['answer']] * len(item['questions']))
            else:
                print(f"Advertencia: La categoría '{category}' tiene un formato incorrecto.")
    elif isinstance(items, dict):
        if 'questions' in items and 'answer' in items:
            questions.extend(items['questions'])
            answers.extend([items['answer']] * len(items['questions']))
        else:
            print(f"Advertencia: La categoría '{category}' tiene un formato incorrecto.")
    else:
        print(f"Advertencia: La categoría '{category}' tiene un formato incorrecto.")

# Crear el DataFrame con las preguntas y respuestas
df = pd.DataFrame({
    'questions': questions,
    'answers': answers
})

# Limpiar las respuestas: asegurar que sean cadenas de texto
df['answers'] = df['answers'].apply(lambda x: x if isinstance(x, str) else str(x))

# Crear el modelo utilizando un pipeline de TF-IDF y Naive Bayes
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Entrenar el modelo con las preguntas y respuestas
model.fit(df['questions'], df['answers'])

# Guardar y cargar el modelo entrenado
joblib.dump(model, 'chatbot_model.pkl')
model = joblib.load('chatbot_model.pkl')

# Respuestas aleatorias para preguntas no reconocidas
def respuesta_aleatoria():
    respuestas = [
        "Mmm, no entendí eso, pero ¿sabías que los koalas duermen hasta 20 horas al día? 🐨💤",
        "¡Buena pregunta! Mientras pienso la respuesta, aquí va un chiste: ¿Qué le dijo un semáforo a otro? ¡No me mires, me estoy cambiando! 🚦😂",
        "No estoy seguro, pero te recomiendo escuchar la banda Queen. ¡Son épicos! 🎵"
    ]
    return random.choice(respuestas)

# Función para detectar preguntas irrelevantes
def detectar_pregunta_irrelevante(question, model, df):
    # Vectorizar la pregunta usando el modelo tfidf
    question_vector = model.named_steps['tfidfvectorizer'].transform([question])
    
    # Predecir las respuestas utilizando el modelo
    predicted_answer = model.predict([question])[0]

    # Comparar la similitud con las respuestas posibles
    answers_vector = model.named_steps['tfidfvectorizer'].transform(df['answers'])
    similarities = cosine_similarity(question_vector, answers_vector)
    
    # Verificar si la similitud más alta es suficientemente baja para considerar la pregunta irrelevante
    threshold = 0.1  # Ajusta este valor según sea necesario
    if max(similarities[0]) < threshold:
        return True
    return False

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data['input']
    
    # Verificar si la pregunta es irrelevante
    if detectar_pregunta_irrelevante(question, model, df):
        return jsonify({"response": "Lo siento, no puedo responder a eso."})
    
    try:
        # Predecir la respuesta con el modelo
        answer = model.predict([question])[0]
        return jsonify({"response": answer})
    except ValueError:
        # Si no se puede predecir, devolver una respuesta aleatoria
        return jsonify({"response": respuesta_aleatoria()})

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
