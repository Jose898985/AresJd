import streamlit as st
import requests
import json
from datetime import datetime

# --- Estética ---
st.set_page_config(page_title="Ares Gemini Pro", page_icon="🌐", layout="wide")
st.markdown("<style>.stApp { background: #001524; color: white; }</style>", unsafe_allow_html=True)
st.title("🌐 A R E S · S Y S T E M")

# Configuración Directa
CLAVE = "AIzaSyA6F-3ZkIxuFwDCVEuvQD3m-L8jBNgddeg"
# Usamos la URL oficial de la API estable v1
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
        # Preparamos el envío directo a Google
        payload = {
            "contents": [{
                "parts": [{"text": f"Eres Ares, un sistema avanzado. Hoy es {datetime.now().strftime('%d/%m/%Y')}. Usuario dice: {prompt}"}]
            }]
        }
        
        response = requests.post(URL_API, json=payload)
        data = response.json()

        if "candidates" in data:
            respuesta_texto = data["candidates"][0]["content"]["parts"][0]["text"]
            with st.chat_message("assistant"):
                st.markdown(respuesta_texto)
                st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
        else:
            st.error(f"Error de Google: {data.get('error', {}).get('message', 'Desconocido')}")

    except Exception as e:
        st.error(f"Error de conexión: {e}")
