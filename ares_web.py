import streamlit as st
import google.generativeai as genai

# --- Estética ---
st.set_page_config(page_title="Ares  Pro", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #001524 0%, #000000 100%); }
    h1 { color: #00f2ff !important; text-shadow: 0 0 10px #00f2ff; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 A R E S · ")

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
        # --- ESTRATEGIA DE AUTO-DETECCIÓN ---
        # Listamos los modelos que Google REALMENTE te permite usar hoy
        modelos_disponibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        if not modelos_disponibles:
            st.error("No se encontraron modelos disponibles para esta API Key.")
        else:
            # Intentamos usar el mejor disponible (Flash) o el primero de la lista
            modelo_a_usar = next((m for m in modelos_disponibles if "flash" in m), modelos_disponibles[0])
            
            model = genai.GenerativeModel(modelo_a_usar)
            
            with st.chat_message("assistant"):
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
    except Exception as e:
        st.error(f"Error de sistema: {e}")
        st.info("Revisa si tu cuenta de Google tiene restricciones regionales.")

