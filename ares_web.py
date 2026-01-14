import streamlit as st
import requests

# --- Interfaz Ares ---
st.set_page_config(page_title="Ares System", page_icon="🌐", layout="wide")
st.markdown("<style>.stApp { background: #000c14; color: white; }</style>", unsafe_allow_html=True)
st.title("🌐 A R E S · S Y S T E M")

# NUEVA CONFIGURACIÓN CON TU CLAVE DE AI STUDIO
CLAVE = "AIzaSyD2IYGK9G-2ndLDxBL8cow1fASSWJe_zNU"
# Usamos gemini-2.0-flash-001 que es el nombre técnico estable según tu lista
URL_API = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-001:generateContent?key={CLAVE}"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe tu comando Ares..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        payload = {
            "contents": [{"parts": [{"text": f"Eres Ares, un sistema inteligente. Responde de forma épica y eficiente: {prompt}"}]}]
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
            st.error("Error en la respuesta del núcleo.")
            st.json(data) 

    except Exception as e:
        st.error(f"Error de conexión: {e}")

