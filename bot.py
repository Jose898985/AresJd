import google.generativeai as genai  # <--- ESTA LÍNEA ES LA QUE FALTA
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime

app = Flask(__name__)

# --- Configuración del Núcleo Ares ---
CLAVE = "AIzaSyAGRktuSRioeoFdInaffp7erkkMnkR-5Io"
genai.configure(api_key=CLAVE)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    mensaje_usuario = request.values.get('Body', '')
    ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    try:
        # 1. Buscamos el modelo (usando la lógica de tu web que ya funciona)
        modelos_disponibles = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Priorizamos Gemini 2.5 Flash que aparece en tus cuotas
        modelo_a_usar = next((m for m in modelos_disponibles if "2.5" in m), modelos_disponibles[0])
        
        # 2. Instrucción de sistema
        instruccion_sistema = f"Eres Ares, un asistente avanzado. La fecha y hora actual es: {ahora}. Responde de forma concisa."
        
        model = genai.GenerativeModel(
            model_name=modelo_a_usar,
            system_instruction=instruccion_sistema
        )
        
        # 3. Generar respuesta
        response = model.generate_content(mensaje_usuario)
        respuesta_ares = response.text

    except Exception as e:
        respuesta_ares = f"🤖 Ares: Error técnico. ({str(e)})"

    # 4. Enviar a Twilio
    resp = MessagingResponse()
    resp.message(respuesta_ares)
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
