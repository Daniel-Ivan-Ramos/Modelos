import pandas as pd
import json

# Cargar el JSON completo
json_data = """
{
  "saludos": [
    {
      "questions": ["hola", "buenas", "¿qué tal?", "¿cómo estás?", "¡hey!"],
      "answer": "¡Hola! Soy tu asistente virtual. ¿En qué puedo ayudarte hoy? 😊"
    },
    {
      "questions": ["adiós", "hasta luego", "nos vemos", "chau", "hasta pronto"],
      "answer": "¡Adiós! Espero haberte ayudado. ¡Nos vemos pronto! 👋"
    },
    {
      "questions": ["buenos días", "buenos días, ¿cómo estás?", "¡buenos días!"],
      "answer": "¡Buenos días! ¿Cómo te sientes hoy? 🌞"
    },
    {
      "questions": ["buenas tardes", "¡buenas tardes!", "hola, buenas tardes", "¿qué tal, buenas tardes?"],
      "answer": "¡Buenas tardes! ¿Qué puedo hacer por ti? 🌇"
    },
    {
      "questions": ["buenas noches", "¡buenas noches!", "hola, buenas noches", "¿cómo va todo, buenas noches?"],
      "answer": "¡Buenas noches! ¿Necesitas ayuda antes de dormir? 🌙"
    },
    {
      "questions": ["¿qué tal?", "¿cómo vas?", "¿cómo te va?", "¿todo bien?"],
      "answer": "¡Todo bien, gracias! ¿Y tú? 😊"
    },
    {
      "questions": ["¿cómo estás?", "¿cómo te encuentras?", "¿qué tal todo?", "¿cómo te sientes hoy?"],
      "answer": "Estoy genial, gracias por preguntar. ¿Cómo puedo ayudarte hoy? 😄"
    }
  ],
    "chistes": [
      {
        "questions": [
          "¿Me cuentas un chiste?",
          "Cuéntame un chiste",
          "¿Tienes algún chiste?",
          "Dime un chiste",
          "¿Sabes un chiste?",
          "Cuéntame algo gracioso",
          "Tienes un buen chiste por ahí",
          "Hazme reír con un chiste",
          "¿Tienes algún chiste para hoy?"
        ],
        "answer": [
          "¡Claro! ¿Por qué el libro de matemáticas está triste? ¡Porque tiene demasiados problemas! 😂",
          "¡Aquí va otro! ¿Por qué los pájaros no usan Facebook? ¡Porque ya tienen Twitter! 🐦",
          "Un chiste rápido: ¿Cómo se llama un boomerang que no vuelve? ¡Un palo! 😂",
          "¿Sabes por qué las focas miran siempre hacia arriba? ¡Porque ahí están los focos! 🦭",
          "¿Por qué el calamar no se pelea con nadie? ¡Porque siempre está en su tinta! 🐙",
          "¿Qué hace una abeja en el gimnasio? ¡Zum-ba! 🐝"
        ]
      }
    ],
    "datos_curiosos": [
      {
        "questions": [
          "¿Me dices un dato curioso?",
          "Dime algo interesante",
          "Quiero un dato curioso",
          "Cuéntame un dato curioso",
          "¿Sabes algo curioso?",
          "¿Conoces un dato interesante?",
          "Dame un dato interesante",
          "Cuéntame algo que no sepa"
        ],
        "answer": [
          "¿Sabías que los tiburones existen desde antes que los árboles? ¡Han estado aquí por más de 400 millones de años! 🦈",
          "¿Sabías que las abejas tienen cinco ojos? ¡Sí, cinco! 🐝",
          "Aquí va uno: los camellos tienen tres párpados para proteger sus ojos de la arena del desierto. 🐫",
          "El corazón de una ballena azul es tan grande que una persona podría nadar a través de sus arterias. 🐋",
          "El sol es tan grande que caben 1.3 millones de planetas Tierra dentro de él. ☀️",
          "Los pulpos tienen tres corazones, uno para cada branquia y uno más para el resto de su cuerpo. 🐙"
        ]
      },
      {
        "questions": [
          "Dime otro dato curioso",
          "Otro dato curioso, por favor",
          "Dame un dato más",
          "Cuéntame algo curioso",
          "¿Sabes otro dato interesante?",
          "Dame otro dato asombroso",
          "¿Tienes más datos interesantes?"
        ],
        "answer": [
          "Sabías que el Sol es 330,000 veces más masivo que la Tierra? ☀️",
          "¿Sabías que el sonido viaja 4 veces más rápido en el agua que en el aire? 🌊",
          "Los elefantes son los únicos animales que no pueden saltar. 🐘",
          "Las tortugas pueden respirar a través de su trasero. 🐢",
          "El hipo no tiene una causa definitiva, pero se dice que es un mal funcionamiento del diafragma. 🤔"
        ]
      }
    ],
    "adivinanzas": [
      {
        "questions": [
          "¿Tienes alguna adivinanza?",
          "Dime una adivinanza",
          "¿Sabes alguna adivinanza?",
          "Quiero una adivinanza",
          "Dame una adivinanza",
          "¿Me das una adivinanza?",
          "¿Te atreves con una adivinanza?"
        ],
        "answer": [
          "Sí, ahí va: Blanco por dentro, verde por fuera. Si quieres que te lo diga, espera. ¿Qué es? (La respuesta es: el coco)",
          "Tengo agujas y no sé coser, guardo el tiempo y lo sé leer. ¿Qué soy? (La respuesta es: un reloj)",
          "Estoy en todas las casas, pero no tengo piernas. ¿Qué soy? (La respuesta es: una silla)",
          "Cuanto más grande soy, menos peso tengo. ¿Qué soy? (La respuesta es: un agujero)",
          "Tengo muchas llaves, pero no puedo abrir ningún candado. ¿Qué soy? (La respuesta es: un piano)"
        ]
      },
      {
        "questions": [
          "¿Sabes otra adivinanza?",
          "Dime una más",
          "Otra adivinanza, por favor",
          "Quiero otra adivinanza",
          "¿Me das una más?"
        ],
        "answer": [
          "¿Qué tiene muchos dientes pero no puede morder? (La respuesta es: un peine)",
          "Siempre va hacia arriba, nunca hacia abajo, pero no se mueve. ¿Qué es? (La respuesta es: la edad)",
          "Si me nombras, ya no me puedes ver. ¿Qué soy? (La respuesta es: el silencio)"
        ]
      }
    ],
    "ideas_para_hacer": [
      {
        "questions": [
          "¿Qué puedo hacer si me aburro?",
          "Dame una idea para no aburrirme",
          "¿Qué me sugieres hacer?",
          "Dime algo divertido para hacer",
          "¿Tienes alguna idea para hacer algo?",
          "¿Qué puedo hacer ahora?",
          "¿Tienes alguna recomendación para divertirme?",
          "¿Qué me recomiendas hacer?"
        ],
        "answer": [
          "Podrías intentar aprender un truco de magia sencillo. ¡Sorprenderás a todos!",
          "Haz una manualidad con materiales reciclados, como una maceta decorada con latas. ¡Es divertido y bueno para el planeta!",
          "¿Por qué no aprendes a hacer origami? ¡Es una actividad creativa y relajante!",
          "Puedes probar hacer una receta nueva y sorprender a tu familia con algo delicioso. 🍰",
          "¿Por qué no te pones a dibujar algo abstracto? ¡Deja volar tu creatividad! 🎨",
          "Puedes comenzar a escribir un diario o una historia corta. ¡Es una forma excelente de expresar tus pensamientos!"
        ]
      },
      {
        "questions": [
          "¿Qué más puedo hacer si me aburro?",
          "Dame más ideas divertidas",
          "Sigue dándome ideas para no aburrirme",
          "¿Qué más puedo hacer ahora?",
          "¿Qué me sugieres para pasar el tiempo?"
        ],
        "answer": [
          "Haz ejercicio en casa con una rutina sencilla. ¡Ponle música y empieza a moverte! 🏋️‍♂️",
          "¿Por qué no organizas un maratón de películas de tu género favorito? 🍿🎬",
          "Puedes empezar a aprender un nuevo idioma. ¡Nunca es tarde para comenzar! 🌍",
          "Arma un rompecabezas o haz un crucigrama, son perfectos para mantener tu mente activa. 🧩",
          "Haz una videollamada con tus amigos o familiares, ¡es una excelente forma de conectarse! 📱"
        ]
      }
    ]
  }
  

"""

# Convertir el JSON a un diccionario de Python
data = json.loads(json_data)

# Iterar sobre las categorías en el JSON y guardar cada una en un archivo CSV
for category, items in data.items():
    # Crear una lista para almacenar las preguntas y respuestas
    rows = []
    
    # Procesar cada entrada de la categoría
    for item in items:
        # Unir todas las preguntas en una sola cadena de texto
        questions = ', '.join(item['questions'])
        # Unir todas las respuestas en una sola cadena de texto
        answers = ', '.join(item['answer'])
        
        # Agregar la fila a la lista
        rows.append([questions, answers])
    
    # Crear el DataFrame para la categoría actual
    df = pd.DataFrame(rows, columns=['questions', 'answers'])
    
    # Guardar el DataFrame en un archivo CSV con el nombre de la categoría
    df.to_csv(f'{category}.csv', index=False)

print("Archivos CSV generados exitosamente.")
