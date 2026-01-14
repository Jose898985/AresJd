import streamlit as st
import requests
from datetime import datetime

# --- Interfaz ---
st.set_page_config(page_title="Ares System", page_icon="🌐")
st.title("🌐 A R E S · S Y S T E M")

# Configuración limpia
CLAVE = "AIzaSyBuubE6NudTGNF2Y4uKDqNf1WG-koQfb7o"
# Forzamos la versión v1 estable con el modelo flash
URL_API = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={CLAVE}"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe aquí..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        payload = {
            "contents": [{"parts": [{"text": f"Eres Ares, un sistema operativo inteligente. Responde: {prompt}"}]}]
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(URL_API, json=payload, headers=headers)
        data = response.json()

        if "candidates" in data:
            respuesta = data["candidates"][0]["content"]["parts"][0]["text"]
            with st.chat_message("assistant"):
                st.markdown(respuesta)
                st.session_state.messages.append({"role": "assistant", "content": respuesta})
        else:
            # Si falla, este mensaje nos dirá el motivo exacto de Google
            st.error("Respuesta fallida del núcleo.")
            st.write(data) 

    except Exception as e:
        st.error(f"Fallo de conexión: {e}")
