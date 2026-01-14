import streamlit as st
import requests
import json
from datetime import datetime

# --- Configuración Visual Estilo Ares ---
st.set_page_config(page_title="Ares System", page_icon="🌐", layout="wide")
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #001524 0%, #000000 100%); color: white; }
    h1 { color: #00f2ff !important; text-shadow: 0 0 10px #00f2ff; text-align: center; font-family: 'Orbitron', sans-serif; }
    .stChatInput { border-radius: 20px; border: 1px solid #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 A R E S · S Y S T E M")

# CONFIGURACIÓN DE ACCESO (Tu nueva clave y la ruta -latest)
CLAVE = "AIzaSyBuubE6NudTGNF2Y4uKDqNf1WG-koQfb7o"
URL_API = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={CLAVE}"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial de chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe tu comando Ares..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Petición directa a Google
        payload = {
            "contents": [{"parts": [{"text": f"Eres Ares, un sistema inteligente. Responde: {prompt}"}]}]
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
            st.error("Error de configuración de API.")
            st.json(data) # Esto nos dirá el error exacto si persiste
            
    except Exception as e:
        st.error(f"Error de conexión: {e}")
