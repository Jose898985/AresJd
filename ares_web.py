import streamlit as st
from google import genai

# --- Estética ---
st.set_page_config(page_title="Ares Gemini Pro", page_icon="🌐", layout="wide")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #001524 0%, #000000 100%); }
    .stChatMessage { background: rgba(0, 242, 255, 0.05) !important; border-radius: 15px !important; border: 1px solid rgba(0, 242, 255, 0.2); }
    h1 { color: #00f2ff !important; text-shadow: 0 0 10px #00f2ff; text-align: center; font-family: 'Orbitron', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌐 A R E S · G E M I N I")

CLAVE = "AIzaSyAoqBy9sY3naxGYKbhvW7wKLPxjKkRGqEE"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe tu comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- PROTOCOLO DE CONEXIÓN MÚLTIPLE ---
    modelos_a_probar = ["gemini-1.5-flash", "gemini-pro", "gemini-1.5-flash-001"]
    respuesta_exitosa = False

    with st.chat_message("assistant"):
        status_placeholder = st.empty()
        
        for modelo in modelos_a_probar:
            try:
                status_placeholder.text(f"Conectando vía {modelo}...")
                client = genai.Client(api_key=CLAVE)
                response = client.models.generate_content(model=modelo, contents=prompt)
                
                respuesta_texto = response.text
                status_placeholder.empty() # Borra el mensaje de carga
                st.markdown(respuesta_texto)
                st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
                respuesta_exitosa = True
                break # Si funciona, salimos del bucle
            except Exception as e:
                continue # Si falla, intenta con el siguiente modelo del bucle

        if not respuesta_exitosa:
            st.error("🚫 Todos los protocolos de conexión han fallado. Es posible que tu API Key necesite ser renovada en Google AI Studio.")
