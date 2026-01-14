import streamlit as st
import google.generativeai as genai

# --- Estética ---
st.set_page_config(page_title="Ares  Pro", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #001524 0%, #000000 100%); }
    .stChatMessage { background: rgba(0, 242, 255, 0.05) !important; border-radius: 15px !important; }
    h1 { color: #00f2ff !important; text-shadow: 0 0 10px #00f2ff; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 A R E S ")

# Tu clave de API
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
        # Probamos con el nombre técnico más robusto que existe
        model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
        
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        # Si falla, intentamos la versión estable sin el prefijo 'models/'
        try:
            model_alt = genai.GenerativeModel("gemini-1.5-flash")
            response = model_alt.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e2:
            st.error(f"Error crítico de ruta: {e2}")
            st.info("Por favor, verifica que tu API Key no tenga restricciones de IP en Google AI Studio.")


