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

# Tu clave nueva
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
        client = genai.Client(api_key=CLAVE)
        with st.chat_message("assistant"):
            # Usamos el nombre de modelo más crudo y directo disponible
            # Sin prefijos de 'models/' ni versiones secundarias
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt
            )
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("El modelo no devolvió texto. Intenta con otra pregunta.")
                
    except Exception as e:
        # Si esto falla, mostramos el error real para saber qué corregir
        st.error(f"Fallo de conexión: {e}")
        st.info("Asegúrate de que el archivo requirements.txt esté correcto en GitHub.")
