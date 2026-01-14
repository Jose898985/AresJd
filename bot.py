import google.generativeai as genai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Configuración idéntica a tu web funcional
CLAVE = "AIzaSyAGRktuSRioeoFdInaffp7erkkMnkR-5Io"
genai.configure(api_key=CLAVE)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    # 1. Obtener mensaje
    mensaje_usuario = request.values.get('Body', '')
    
    try:
        # 2. Selección de modelo dinámica (como en tu web)
        modelos = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        modelo_final = next((m for m in modelos if "flash" in m), modelos[0])
        
        model = genai.GenerativeModel(modelo_final)
        
        # 3. Generar respuesta
        response = model.generate_content(mensaje_usuario)
        texto_ares = response.text.strip()

    except Exception as e:
        texto_ares = "🤖 Ares: Error interno."

    # 4. Formato TwiML CORRECTO (Crucial para WhatsApp)
    resp = MessagingResponse()
    resp.message(texto_ares)
    
    # Devolvemos la respuesta como string XML
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
