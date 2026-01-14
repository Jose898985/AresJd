import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- Configuración Visual ---
st.set_page_config(page_title="Ares Gemini Pro", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #001524 0%, #000000 100%); }
    h1 { color: #00f2ff !important; text-shadow: 0 0 10px #00f2ff; text-align: center; }
    .stChatMessage { background: rgba(0, 242, 255, 0.05) !important; border-radius: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 A R E S · G E M I N I")

# Configuración de API
CLAVE = "AIzaSyA6F-3ZkIxuFwDCVEuvQD3m-L8jBNgddeg"
genai.configure(api_key=CLAVE)

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
        # FORZAMOS EL MODELO CON RUTA COMPLETA
        # Esto evita que la librería busque en 'v1beta'
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        
        with st.chat_message("assistant"):
            # Usamos una llamada más directa
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        # Si falla el 1.5, intentamos el 1.0 Pro que es el más compatible del mundo
        try:
            model_alt = genai.GenerativeModel(model_name='models/gemini-1.0-pro')
            response = model_alt.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e2:
            st.error(f"Error de acceso total: {e2}")
            st.info("Verifica en Google AI Studio que tu API Key tenga habilitado 'Gemini API'.")
