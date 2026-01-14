import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Ares System", page_icon="🌐")
st.title("🌐 A R E S · S Y S T E M")

CLAVE = "AIzaSyBuubE6NudTGNF2Y4uKDqNf1WG-koQfb7o"
# Cambiamos a 'gemini-pro' que es el nombre estándar en la v1
URL_API = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={key=AIzaSyBuubE6NudTGNF2Y4uKDqNf1WG-koQfb7}"

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
        # Estructura obligatoria para Gemini Pro
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
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
            st.error("El núcleo sigue sin reconocer el modelo. Intentando diagnóstico...")
            st.write(data) 

    except Exception as e:
        st.error(f"Fallo de conexión: {e}")
