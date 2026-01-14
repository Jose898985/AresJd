import streamlit as st
import requests
import json
from datetime import datetime

# --- Estética Ares ---
st.set_page_config(page_title="Ares Gemini Pro", page_icon="🌐", layout="wide")
st.markdown("""
    <style>
    .stApp { background: #000c14; color: white; }
    .stChatInput { border-radius: 20px; border: 1px solid #00f2ff; }
    h1 { color: #00f2ff; text-align: center; text-shadow: 0 0 10px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 A R E S · S Y S T E M")

# CLAVE Y URL (Cambiamos a v1beta que es donde vive Flash actualmente)
CLAVE = "AIzaSyA6F-3ZkIxuFwDCVEuvQD3m-L8jBNgddeg"
URL_API = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={CLAVE}"

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
        # Estructura de datos exacta para la API
        payload = {
            "contents": [{
                "parts": [{"text": f"Eres Ares, un sistema inteligente. Responde al usuario: {prompt}"}]
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
            # Si vuelve a fallar, el código nos dirá exactamente por qué
            st.error(f"Error detectado: {json.dumps(data)}")

    except Exception as e:
        st.error(f"Error de conexión: {e}")
