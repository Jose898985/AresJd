import streamlit as st
from google import genai

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
        # Forzamos al cliente a usar una configuración base
        client = genai.Client(api_key=CLAVE)
        
        with st.chat_message("assistant"):
            # Probamos con el ID de modelo más básico (v1)
            response = client.models.generate_content(
                model="gemini-1.5-flash-8b", # Versión ultra-ligera y muy estable
                contents=prompt
            )
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        # Si el 8b falla, intentamos el pro de respaldo
        try:
            response = client.models.generate_content(model="gemini-1.5-pro", contents=prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e2:
            st.error(f"Fallo de protocolo: {e2}")
