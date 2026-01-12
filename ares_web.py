import streamlit as st
from google import genai
from google.genai import types

# --- Estética ---
st.set_page_config(page_title="Ares Gemini Pro", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #001524 0%, #000000 100%); }
    .stChatMessage { background: rgba(0, 242, 255, 0.05) !important; border-radius: 15px !important; }
    h1 { color: #00f2ff !important; text-shadow: 0 0 10px #00f2ff; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 A R E S · G E M I N I")

# --- Conexión ---
CLAVE = "AIzaSyAoqBy9sY3naxGYKbhvW7wKLPxjKkRGqEE"

@st.cache_resource
def obtener_cliente():
    return genai.Client(api_key=CLAVE)

# Inicializamos el chat sin herramientas por un momento para probar estabilidad
if "chat" not in st.session_state:
    client = obtener_cliente()
    # Cambiamos a 'gemini-1.5-flash' que es el nombre estándar más estable
    st.session_state.chat = client.chats.create(model="gemini-1.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Interfaz ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe al sistema..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # Enviamos el mensaje directamente
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error("Reiniciando núcleo de Ares... por favor, repite tu mensaje.")
        # Si falla, recreamos el chat
        client = obtener_cliente()
        st.session_state.chat = client.chats.create(model="gemini-1.5-flash")
