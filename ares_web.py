import streamlit as st
import requests
import json
from datetime import datetime

# --- Estética ---
st.set_page_config(page_title="Ares Universal", page_icon="🌐", layout="wide")
st.markdown("<style>.stApp { background: #000c14; color: white; }</style>", unsafe_allow_html=True)
st.title("🌐 A R E S · S Y S T E M")

# CLAVE Y URL (Cambiamos a gemini-pro, la ruta más estable)
CLAVE = "AIzaSyA6F-3ZkIxuFwDCVEuvQD3m-L8jBNgddeg"
URL_API = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={CLAVE}"

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
        payload = {
            "contents": [{
                "parts": [{"text": f"Eres Ares. Hoy es {datetime.now().strftime('%d/%m/%Y')}. Responde: {prompt}"}]
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
            # Si esto falla, el problema es definitivamente la API Key en Google AI Studio
            st.error("Error crítico: El modelo 'gemini-pro' tampoco responde. Verifica tu API Key en Google AI Studio.")
            st.write(data)

    except Exception as e:
        st.error(f"Error de conexión: {e}")
