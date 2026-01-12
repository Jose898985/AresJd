import streamlit as st
from google import genai
from google.genai import types

# --- CONFIGURACIÓN DE PÁGINA Y FUENTES EXTERNAS ---
st.set_page_config(page_title="Ares Cyber-Core", page_icon="⚡", layout="wide")

# Inyectamos Google Fonts y CSS Avanzado
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;500&display=swap');

    /* Fondo con rejilla tecnológica */
    .stApp {
        background-color: #00050a;
        background-image: 
            linear-gradient(0deg, transparent 24%, rgba(0, 242, 255, .05) 25%, rgba(0, 242, 255, .05) 26%, transparent 27%, transparent 74%, rgba(0, 242, 255, .05) 75%, rgba(0, 242, 255, .05) 76%, transparent 77%, transparent),
            linear-gradient(90deg, transparent 24%, rgba(0, 242, 255, .05) 25%, rgba(0, 242, 255, .05) 26%, transparent 27%, transparent 74%, rgba(0, 242, 255, .05) 75%, rgba(0, 242, 255, .05) 76%, transparent 77%, transparent);
        background-size: 50px 50px;
    }

    /* Título con Glow Animado */
    .cyber-title {
        font-family: 'Orbitron', sans-serif;
        color: #00f2ff;
        text-align: center;
        font-size: 3rem;
        text-shadow: 0 0 10px #00f2ff, 0 0 20px #00f2ff;
        animation: blink 2s infinite;
        margin-bottom: 0px;
    }

    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    /* Contenedores de Chat (Glassmorphism Pro) */
    .stChatMessage {
        background: rgba(0, 15, 25, 0.7) !important;
        border-left: 5px solid #00f2ff !important;
        border-radius: 0px 15px 15px 0px !important;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.1);
        backdrop-filter: blur(10px);
        margin: 10px 0px;
        transition: 0.4s;
    }

    .stChatMessage:hover {
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.4);
        transform: translateX(10px);
    }

    /* Sidebar futurista */
    [data-testid="stSidebar"] {
        background-color: #000a0f !important;
        border-right: 1px solid #00f2ff;
    }

    /* Botones estilo Sci-Fi */
    .stButton>button {
        width: 100%;
        background: transparent;
        color: #00f2ff;
        border: 1px solid #00f2ff;
        font-family: 'Orbitron', sans-serif;
        transition: 0.5s;
    }

    .stButton>button:hover {
        background: #00f2ff;
        color: black;
        box-shadow: 0 0 20px #00f2ff;
    }

    /* Input de texto */
    .stChatInput {
        border-top: 1px solid #00f2ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="cyber-title">A R E S · S Y S T E M</h1>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00f2ff; font-family: Rajdhani;'>UNIDAD DE INTELIGENCIA JD ARES</p>", unsafe_allow_html=True)

# --- LÓGICA DE CONEXIÓN INMORTAL ---
CLAVE = "AIzaSyAoqBy9sY3naxGYKbhvW7wKLPxjKkRGqEE"

@st.cache_resource
def get_client():
    return genai.Client(api_key=CLAVE)

if "chat" not in st.session_state:
    try:
        client = get_client()
        st.session_state.chat = client.chats.create(
            model="gemini-flash-latest",
            config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())])
        )
    except:
        st.error("ERROR CRÍTICO: No se pudo establecer conexión con el núcleo.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR DETALLADA ---
with st.sidebar:
    st.markdown("<h2 style='color: #00f2ff; font-family: Orbitron;'>STATUS</h2>", unsafe_allow_html=True)
    st.image("https://i.pinimg.com/originals/3d/8c/60/3d8c603a1d13f8981c2f78505500c50d.gif", width=250) # Animación de carga
    st.divider()
    st.write("🌐 RED: **ACTIVA**")
    st.write("🧠 NÚCLEO: **Ares v1.0**")
    st.write("🛡️ SEGURIDAD: **NIVEL 4**")
    if st.button("PURGAR MEMORIA"):
        st.session_state.messages = []
        st.rerun()

# --- RENDER DE MENSAJES ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"<div style='font-family: Rajdhani; font-size: 1.1rem;'>{message['content']}</div>", unsafe_allow_html=True)

if prompt := st.chat_input("Escribe tu comando..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        # Reintento automático silencioso
        client = get_client()
        st.session_state.chat = client.chats.create(model="gemini-flash-latest")
        response = st.session_state.chat.send_message(prompt)
        st.markdown(response.text)