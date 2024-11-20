import json
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
import pickle
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


# Descargar stopwords de NLTK si no lo tienes
nltk.download('stopwords')
nltk.download('punkt')  # Para lematización

# Cargar los datos
try:
    with open('preguntas.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print("Error: El archivo 'preguntas.json' no se encuentra en el directorio especificado.")
    exit()
except json.JSONDecodeError as e:
    print(f"Error al decodificar el archivo JSON: {e}")
    exit()

# Inicializar el lematizador
lemmatizer = WordNetLemmatizer()

# Preparar las preguntas y etiquetas
preguntas = []
etiquetas = []

# Eliminar caracteres especiales y convertir a minúsculas
def limpiar_texto(texto):
    # Convertir a minúsculas, eliminar caracteres especiales excepto letras con acentos
    texto = texto.lower()
    texto = re.sub(r'[^\w\sáéíóúüñ]', '', texto)  # Conserva letras con acentos y caracteres relevantes
    texto = ' '.join([lemmatizer.lemmatize(word) for word in texto.split()])  # Lematizar cada palabra
    return texto.strip()  # Eliminar espacios en blanco al inicio y final

# Iterar sobre las categorías y sus preguntas
for categoria, items in data.items():
    if isinstance(items, list):
        for item in items:
            if isinstance(item, dict) and 'questions' in item:
                for pregunta in item['questions']:
                    pregunta_limpia = limpiar_texto(pregunta)
                    preguntas.append(pregunta_limpia)
                    etiquetas.append(categoria)

# Cargar nuevas interacciones si existen
try:
    with open('nuevas_interacciones.json', 'r', encoding='utf-8') as f:
        nuevas_interacciones = [json.loads(line) for line in f]
        for interaccion in nuevas_interacciones:
            if interaccion['expected_category'] != 'unknown':
                pregunta_limpia = limpiar_texto(interaccion['input'])
                preguntas.append(pregunta_limpia)
                etiquetas.append(interaccion['expected_category'])
except FileNotFoundError:
    print("No hay nuevas interacciones para agregar.")

# Limpiar el archivo de nuevas interacciones después de procesarlas
with open('nuevas_interacciones.json', 'w', encoding='utf-8') as f:
    pass  # Sobrescribir con un archivo vacío

# Comprobar que las preguntas y etiquetas se hayan preparado correctamente
print(f"Total de preguntas: {len(preguntas)}")
print(f"Total de etiquetas: {len(etiquetas)}")

# Definir stopwords en español (si deseas un mejor control)
stop_words = stopwords.words('spanish')

# Crear un modelo de pipeline con TF-IDF y un clasificador
vectorizer = TfidfVectorizer(stop_words=stop_words, ngram_range=(1, 3), max_features=8000, sublinear_tf=True)
modelo = make_pipeline(vectorizer, MultinomialNB(alpha=0.5))

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(preguntas, etiquetas, test_size=0.2, random_state=42)

# Realizar la búsqueda en cuadrícula (GridSearch) para optimizar los hiperparámetros
param_grid = {
    'tfidfvectorizer__ngram_range': [(1, 1), (1, 2), (1, 3)],
    'tfidfvectorizer__max_features': [5000, 8000, 10000],
    'multinomialnb__alpha': [0.1, 0.5, 1.0]
}

grid_search = GridSearchCV(modelo, param_grid, cv=5, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Mostrar los mejores parámetros encontrados
print(f"Mejores parámetros encontrados: {grid_search.best_params_}")
print(f"Mejor puntuación de validación: {grid_search.best_score_}")

# Usar el mejor modelo encontrado por GridSearch
modelo = grid_search.best_estimator_

# Evaluar el modelo con el conjunto de prueba
y_pred = modelo.predict(X_test)
print(f"Precisión del modelo: {modelo.score(X_test, y_test)}")
print(classification_report(y_test, y_pred))

# Guardar el modelo entrenado
with open('modelo_chatbot.pkl', 'wb') as archivo:
    pickle.dump(modelo, archivo)

print("Modelo mejorado entrenado y guardado con éxito.")
