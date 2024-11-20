from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import pickle
import random
import re
import logging
import os

# Configuración de la aplicación Flask
app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = False  # Desactivar modo de depuración
app.config['ENV'] = 'production'  # Establecer el entorno como producción
logging.basicConfig(level=logging.INFO)  # Configurar logging

# Ruta de los archivos
RUTA_MODELO = 'modelo_chatbot.pkl'
RUTA_PREGUNTAS = 'preguntas.json'
RUTA_INTERACCIONES = 'nuevas_interacciones.json'

# Cargar el modelo entrenado
try:
    with open(RUTA_MODELO, 'rb') as archivo:
        modelo = pickle.load(archivo)
    app.logger.info("Modelo cargado correctamente.")
except Exception as e:
    app.logger.error(f"Error al cargar el modelo: {e}")
    modelo = None

# Cargar el archivo preguntas.json
try:
    if os.path.isfile(RUTA_PREGUNTAS):
        with open(RUTA_PREGUNTAS, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, dict):
            raise ValueError("El archivo preguntas.json no tiene el formato esperado.")
        app.logger.info("Archivo JSON cargado correctamente.")
    else:
        raise FileNotFoundError(f"No se encontró {RUTA_PREGUNTAS}.")
except Exception as e:
    app.logger.error(f"Error al cargar el archivo JSON: {e}")
    data = None

# Función para limpiar el texto de entrada
def limpiar_texto(texto):
    texto = texto.lower()
    texto = re.sub(r'[^\w\sáéíóúüñ]', '', texto)  # Conserva letras con acentos y caracteres relevantes
    texto = texto.strip()  # Eliminar espacios en blanco al inicio y final
    return texto

# Ruta principal para renderizar el archivo index.html
@app.route('/')
def home():
    return render_template('index.html')

# Ruta para manejar las solicitudes del chatbot
@app.route('/ask', methods=['POST'])
def responder():
    # Verificar si el modelo y el archivo JSON están cargados correctamente
    if modelo is None or data is None:
        return jsonify({'response': "Error interno. Intenta más tarde."})

    datos = request.get_json()
    entrada_usuario = limpiar_texto(datos.get('input', ''))

    if len(entrada_usuario) < 3:  # Si el mensaje es demasiado corto
        return jsonify({'response': "No entendí tu mensaje. ¿Podrías ser más específico?"})

    # Predecir la categoría usando el modelo
    try:
        categoria = modelo.predict([entrada_usuario])[0]
    except Exception as e:
        app.logger.error(f"Error al predecir la categoría: {e}")
        return jsonify({'response': f"Error al predecir la categoría: {e}"})

    # Buscar respuestas en el archivo JSON
    respuestas_posibles = []
    for item in data.get(categoria, []):
        if isinstance(item.get('answer'), list):
            respuestas_posibles.extend(item['answer'])
        elif isinstance(item.get('answer'), str):
            respuestas_posibles.append(item['answer'])

    # Seleccionar una respuesta aleatoria de las respuestas posibles
    if respuestas_posibles:
        respuesta = random.choice(respuestas_posibles)
    else:
        respuesta = "Lo siento, no tengo una respuesta adecuada."

    # Registrar interacciones no reconocidas
    try:
        with open(RUTA_INTERACCIONES, 'a', encoding='utf-8') as f:
            json.dump({'input': entrada_usuario, 'expected_category': categoria}, f, ensure_ascii=False)
            f.write('\n')
        app.logger.info(f"Interacción no reconocida guardada: {entrada_usuario}")
    except Exception as e:
        app.logger.error(f"Error al registrar la interacción no reconocida: {e}")

    return jsonify({'response': respuesta})

# Ruta para reentrenar el modelo
@app.route('/retrain', methods=['POST'])
def reentrenar():
    try:
        import subprocess
        subprocess.run(['python', 'model_train.py'], check=True)
        with open(RUTA_MODELO, 'rb') as archivo:
            global modelo
            modelo = pickle.load(archivo)
        return jsonify({'response': 'Modelo reentrenado con éxito.'})
    except Exception as e:
        app.logger.error(f"Error al reentrenar el modelo: {e}")
        return jsonify({'response': f"Error al reentrenar el modelo: {e}"})

if __name__ == '__main__':
    app.run(debug=False)
