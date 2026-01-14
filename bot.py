from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json

app = Flask(__name__)

# CONFIGURACIÓN DE ACCESO
CLAVE = "AIzaSyBuubE6NudTGNF2Y4uKDqNf1WG-koQfb7o"
URL_API = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={CLAVE}"

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    # Recibimos el mensaje del usuario desde WhatsApp
    pregunta_usuario = request.values.get('Body', '')

    try:
        # Consultamos a Gemini
        payload = {
            "contents": [{"parts": [{"text": f"Eres Ares, responde por WhatsApp de forma breve: {pregunta_usuario}"}]}]
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(URL_API, json=payload, headers=headers)
        data = response.json()

        if "candidates" in data:
            respuesta_ares = data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            respuesta_ares = "Lo siento, tuve un problema con mi cerebro digital. 🤖"

    except Exception as e:
        respuesta_ares = "Error de conexión. Inténtalo de nuevo en un momento."

    # Respondemos a través de Twilio
    resp = MessagingResponse()
    resp.message(respuesta_ares)
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
