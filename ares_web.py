import streamlit as st
from google import genai

# --- Estética ---
st.set_page_config(page_title="Ares Gemini Pro", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #001524 0%, #000000 100%); }
    .stChatMessage { background: rgba(0, 242, 255, 0.05) !important; border-radius: 15px !important; border: 1px solid rgba(0, 242, 255, 0.1); }
    h1 { color: #00f2ff !important; text-shadow: 0 0 10px #00f2ff; text-align: center; font-family: 'Orbitron', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 A R E S · G E M I N I")

# Tu nueva clave
CLAVE = "AIzaSyA6F-3ZkIxuFwDCVEuvQD3m-L8jBNgddeg"

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
        client = genai.Client(api_key=CLAVE)
        with st.chat_message("assistant"):
            # Cambiamos a esta versión específica para evitar el error 404
            response = client.models.generate_content(
                model="models/gemini-1.5-flash-002", 
                contents=prompt
            )
            respuesta_texto = response.text
            st.markdown(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
            
    except Exception as e:
        # Si vuelve a dar 404, intentamos con el nombre corto
        if "404" in str(e):
            try:
                response = client.models.generate_content(model="gemini-pro", contents=prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except:
                st.error("Error de ruta de modelo. Intenta refrescar la página.")
        else:
            st.error(f"Error de sistema: {e}")
