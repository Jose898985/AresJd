import streamlit as st
from google import genai

# --- Configuración Visual ---
st.set_page_config(page_title="Ares Gemini Pro", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #001524 0%, #000000 100%); }
    .stChatMessage { background: rgba(0, 242, 255, 0.05) !important; border-radius: 15px !important; border: 1px solid rgba(0, 242, 255, 0.1); }
    h1 { color: #00f2ff !important; text-shadow: 0 0 10px #00f2ff; text-align: center; font-family: 'Orbitron', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 A R E S · G E M I N I")

# --- CONEXIÓN CON TU NUEVA CLAVE ---
CLAVE = "AIzaSyA6F-3ZkIxuFwDCVEuvQD3m-L8jBNgddeg"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Dibujar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada de usuario
if prompt := st.chat_input("Escribe tu comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Iniciamos el cliente con la nueva clave
        client = genai.Client(api_key=CLAVE)
        
        with st.chat_message("assistant"):
            # Usamos gemini-1.5-flash para máxima estabilidad
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt
            )
            
            respuesta_texto = response.text
            st.markdown(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
            
    except Exception as e:
        if "429" in str(e):
            st.error("🚦 Límite de mensajes alcanzado. Espera 30 segundos.")
        else:
            st.error(f"⚠️ Error de sistema: {e}")
