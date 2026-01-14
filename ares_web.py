import streamlit as st
import requests
import json
from datetime import datetime

st.set_page_config(page_title="Ares System", page_icon="🌐", layout="wide")
st.markdown("<style>.stApp { background: #000c14; color: white; }</style>", unsafe_allow_html=True)
st.title("🌐 A R E S · S Y S T E M")

CLAVE = "AIzaSyBuubE6NudTGNF2Y4uKDqNf1WG-koQfb7o"

# Lista de modelos para probar en orden de prioridad
MODELOS_A_PROBAR = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-pro",
    "chat-bison-001"
]

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe tu comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    respuesta_final = None
    
    # Bucle para probar cada modelo hasta que uno funcione
    for modelo in MODELOS_A_PROBAR:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={CLAVE}"
            payload = {"contents": [{"parts": [{"text": f"Eres Ares, responde: {prompt}"}]}]}
            response = requests.post(url, json=payload, timeout=10)
            data = response.json()

            if "candidates" in data:
                respuesta_final = data["candidates"][0]["content"]["parts"][0]["text"]
                break # ¡Funcionó! Salimos del bucle
        except:
            continue

    if respuesta_final:
        with st.chat_message("assistant"):
            st.markdown(respuesta_final)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_final})
    else:
        st.error("Ningún modelo de Google está respondiendo a esta clave. Verifica que la API de Gemini esté activa en Google Cloud Console.")
