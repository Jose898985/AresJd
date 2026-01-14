import streamlit as st
import requests
import json
from datetime import datetime

# --- Interfaz Ares ---
st.set_page_config(page_title="Ares System", page_icon="🌐", layout="wide")
st.markdown("<style>.stApp { background: #000c14; color: white; }</style>", unsafe_allow_html=True)
st.title("🌐 A R E S · S Y S T E M")

# CONFIGURACIÓN DE TU NUEVA CLAVE
CLAVE = "AIzaSyBuubE6NudTGNF2Y4uKDqNf1WG-koQfb7o"
# Usamos la versión v1 estable para evitar el error 404
URL_API = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={CLAVE}"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe tu comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Estructura de mensaje para Gemini 1.5
        payload = {
            "contents": [{
                "parts": [{"text": f"Eres Ares, un asistente avanzado. Hoy es {datetime.now().strftime('%d/%m/%Y')}. Responde: {prompt}"}]
            }]
        }
        
        headers = {'Content-Type': 'application/json'}
        response = requests.post(URL_API, json=payload, headers=headers)
        data = response.json()

        if "candidates" in data:
            respuesta_texto = data["candidates"][0]["content"]["parts"][0]["text"]
            with st.chat_message("assistant"):
                st.markdown(respuesta_texto)
                st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
        else:
            # Si hay error, mostramos el mensaje técnico para ajustar
            st.error("Respuesta inesperada de Google.")
            st.json(data)

    except Exception as e:
        st.error(f"Error de conexión: {e}")
