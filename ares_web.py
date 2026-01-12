import streamlit as st
from google import genai

# --- Estética Cyber-Pro ---
st.set_page_config(page_title="Ares Gemini Pro", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #001524 0%, #000000 100%); }
    .stChatMessage { background: rgba(0, 242, 255, 0.05) !important; border-radius: 15px !important; border: 1px solid rgba(0, 242, 255, 0.1); }
    h1 { color: #00f2ff !important; text-shadow: 0 0 10px #00f2ff; text-align: center; font-family: 'Orbitron', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 A R E S · G E M I N I")

# --- Conexión Blindada ---
CLAVE = "AIzaSyAoqBy9sY3naxGYKbhvW7wKLPxjKkRGqEE"

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Interfaz de Chat ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe tu comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Aquí es donde estaban los espacios mal puestos:
        client = genai.Client(api_key=CLAVE)
        
        with st.chat_message("assistant"):
            # Usamos el modelo 2.0 que es el más potente y compatible actualmente
            response = client.models.generate_content(
                model="gemini-2.0-flash-exp", 
                contents=prompt
            )
            
            respuesta_texto = response.text
            st.markdown(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
            
    except Exception as e:
        st.error(f"ERROR DE SISTEMA: {e}")
        st.info("Intenta refrescar la página (F5) si el error persiste.")
