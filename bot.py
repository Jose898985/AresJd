from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai
import os

app = Flask(__name__)

# Configuración de Gemini
CLAVE = "AIzaSyA6F-3ZkIxuFwDCVEuvQD3m-L8jBNgddeg"
genai.configure(api_key=CLAVE)
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    # 1. Recibir el mensaje de WhatsApp
    msg_recibido = request.values.get('Body', '').lower()
    
    # 2. Ares procesa la respuesta
    response = model.generate_content(f"Eres Ares, responde de forma breve a esto: {msg_recibido}")
    respuesta_ares = response.text

    # 3. Twilio envía la respuesta de vuelta a WhatsApp
    resp = MessagingResponse()
    resp.message(respuesta_ares)
    
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
