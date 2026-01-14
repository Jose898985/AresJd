import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- CONFIGURACIÓN DE IA ---
CLAVE = "AIzaSyA6F-3ZkIxuFwDCVEuvQD3m-L8jBNgddeg"
genai.configure(api_key=CLAVE)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- PARTE 1: INTERFAZ WEB (Streamlit) ---
st.set_page_config(page_title="Ares Multi-Canal", page_icon="🌐")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #001524 0%, #000000 100%); }
    h1 { color: #00f2ff !important; text-align: center; font-family: 'Orbitron'; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 A R E S · S Y S T E M")
st.write("Conectado a WhatsApp vía Twilio")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe aquí (Web)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    response = model.generate_content(prompt)
    with st.chat_message("assistant"):
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# --- PARTE 2: LÓGICA DE WHATSAPP ---
# Nota: Para que WhatsApp funcione, necesitamos una URL pública.
# Streamlit no es ideal para recibir Webhooks directamente, 
# pero puedes ver los mensajes aquí abajo si los sincronizamos.
st.sidebar.info("Para activar WhatsApp, vincula tu URL de Streamlit en el Sandbox de Twilio.")

