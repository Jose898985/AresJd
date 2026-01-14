import google.generativeai as genai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Tu clave verificada
CLAVE = "AIzaSyAGRktuSRioeoFdInaffp7erkkMnkR-5Io"
genai.configure(api_key=CLAVE)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    mensaje_usuario = request.values.get('Body', '')
    
    try:
        # Usamos el modelo flash por velocidad
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(mensaje_usuario)
        texto_ares = response.text.strip()
    except Exception as e:
        texto_ares = "🤖 Ares: Error de conexión con el núcleo."

    # Creamos la respuesta oficial para Twilio
    resp = MessagingResponse()
    resp.message(texto_ares)
    
    # IMPORTANTE: Forzamos el formato XML para que Twilio no se confunda
    return str(resp), 200, {'Content-Type': 'text/xml'}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
