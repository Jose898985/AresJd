import streamlit as st
import google.generativeai as genai
from datetime import datetime
import pytz # Para asegurar la zona horaria

# --- Configuración Visual ---
st.set_page_config(page_title="Ares  Pro", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #001524 0%, #000000 100%); }
    h1 { color: #00f2ff !important; text-shadow: 0 0 10px #00f2ff; text-align: center; font-family: 'Orbitron', sans-serif; }
    .stChatMessage { background: rgba(0, 242, 255, 0.05) !important; border-radius: 15px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 A R E S · ")

# Configuración de API
CLAVE = "AIzaSyA6F-3ZkIxuFwDCVEuvQD3m-L8jBNgddeg"
genai.configure(api_key=CLAVE)

# --- Gestión del Tiempo ---
# Obtenemos la fecha y hora actual (ajustado a tu zona horaria si es necesario)
ahora = datetime.now()
fecha_formateada = ahora.strftime("%d/%m/%Y %H:%M:%S")

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
        # Buscamos modelos disponibles como hicimos antes para evitar el 404
        modelos_disponibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        modelo_a_usar = next((m for m in modelos_disponibles if "flash" in m), modelos_disponibles[0])
        
        # INSTRUCCIÓN DE TIEMPO: Le decimos a la IA quién es y qué hora es
        instruccion_sistema = f"Eres Ares, un asistente avanzado. La fecha y hora actual es: {fecha_formateada}."
        
        model = genai.GenerativeModel(
            model_name=modelo_a_usar,
            system_instruction=instruccion_sistema
        )
        
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Error de sistema: {e}")

