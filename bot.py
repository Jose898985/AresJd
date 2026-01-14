import google.generativeai as genai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

app = Flask(__name__)

# --- Configuración del Núcleo Ares ---
CLAVE = "AIzaSyAGRktuSRioeoFdInaffp7erkkMnkR-5Io"
genai.configure(api_key=CLAVE)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    # 1. Capturar mensaje del usuario
    mensaje_usuario = request.values.get('Body', '')
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    try:
        # 2. Selección automática del modelo (igual que tu web funcional)
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        modelo_final = next((m for m in modelos if "flash" in m), modelos[0])
        
        # 3. Configuración del modelo
        model = genai.GenerativeModel(
            model_name=modelo_final,
            system_instruction=f"Eres Ares, un asistente avanzado. Hoy es {ahora}. Responde de forma muy breve."
        )
        
        # 4. Generar y limpiar respuesta
        response = model.generate_content(mensaje_usuario)
        texto_ares = response.text.strip() # Limpiamos espacios extra

    except Exception as e:
        texto_ares = f"🤖 Ares: Error interno ({str(e)})"

    # 5. Respuesta en formato Twilio (Crucial para que llegue el mensaje)
    resp = MessagingResponse()
    resp.message(texto_ares)
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
