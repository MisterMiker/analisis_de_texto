import streamlit as st
from textblob import TextBlob
from googletrans import Translator
from collections import Counter
import matplotlib.pyplot as plt
import json
from streamlit_lottie import st_lottie

# --- Configuración de página ---
st.set_page_config(page_title="Análisis de Sentimientos", layout="centered")

# --- Estilos personalizados ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #656d4a;
        color: #582f0e;
    }
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: #582f0e !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Función para cargar animaciones ---
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

# --- Título ---
st.title("Análisis de Sentimientos con Animaciones")

# --- Entrada de texto ---
st.subheader("Escribe tu texto:")
user_input = st.text_area("Ingresa un texto para analizar", height=200)

if st.button("Analizar"):
    if user_input.strip() != "":
        # Traducción para mejorar análisis
        translator = Translator()
        traduccion = translator.translate(user_input, src="es", dest="en")
        texto_en = traduccion.text

        # Análisis con TextBlob
        blob = TextBlob(texto_en)
        polaridad = blob.sentiment.polarity
        subjetividad = blob.sentiment.subjectivity

        # Mostrar métricas
        st.write("### Resultados:")
        st.write(f"Polaridad: **{polaridad:.2f}**")
        st.write(f"Subjetividad: **{subjetividad:.2f}**")

        # Clasificación del sentimiento
        if polaridad > 0:
            emocion = "Positivo"
            animacion = load_lottiefile("Happy Dog.json")
        elif polaridad < 0:
            emocion = "Negativo"
            animacion = load_lottiefile("Shiba Sad.json")
        else:
            emocion = "Neutral"
            animacion = load_lottiefile("Dancing Bear.json")

        st.write(f"Emoción detectada: **{emocion}**")
        st_lottie(animacion, height=250, key="emocion_anim")

        # Extra: contador de palabras
        palabras = [p.lower() for p in user_input.split() if len(p) > 3]
        contador = Counter(palabras)
        st.bar_chart(contador)

        # Texto final
        st.write("Las animaciones estaban bonitas jaja")
    else:
        st.warning("Por favor escribe un texto antes de analizar.")
