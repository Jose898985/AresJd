import streamlit as st
import google.generativeai as genai

# --- Configuración Visual ---
st.set_page_config(page_title="Ares Gemini Pro", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #001524 0%, #000000 100%); }
    .stChatMessage { background: rgba(0, 242, 255, 0.05) !important; border-radius: 15px !important; }
    h1 { color: #00f2ff !important; text-shadow: 0 0 10px #00f2ff; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 A R E S · G E M I N I")

# Tu clave de API
CLAVE = "AIzaSyA6F-3ZkIxuFwDCVEuvQD3m-L8jBNgddeg"
genai.configure(api_key=CLAVE)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Dibujar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Lógica de Chat
if prompt := st.chat_input("Escribe tu comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Usamos gemini-pro para evitar errores de ruta 404
        model = genai.GenerativeModel("gemini-pro")
        
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            
            if response.text:
                respuesta_texto = response.text
                st.markdown(respuesta_texto)
                st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
            else:
                st.warning("No se recibió respuesta del modelo.")
                
    except Exception as e:
        # Alineación corregida del bloque except
        st.error(f"Error de conexión: {e}")
