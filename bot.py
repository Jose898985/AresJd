from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

# CONFIGURACIÓN CON NUEVA CLAVE
CLAVE = "AIzaSyD2IYGK9G-2ndLDxBL8cow1fASSWJe_zNU"
URL_API = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={CLAVE}"
# Usamos gemini-2.0-flash-001 que es el nombre técnico estable según tu lista
URL_API = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-001:generateContent?key={CLAVE}"
@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    mensaje_usuario = request.values.get('Body', '')
    
    try:
        payload = {
            "contents": [{"parts": [{"text": f"Responde como Ares por WhatsApp de forma breve: {mensaje_usuario}"}]}]
        }
        headers = {'Content-Type': 'application/json'}
        r = requests.post(URL_API, json=payload, headers=headers)
        data = r.json()

        if "candidates" in data:
            respuesta_ares = data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            respuesta_ares = "🤖 Ares: Error de cuota o clave. Revisa AI Studio."

    except Exception as e:
        respuesta_ares = "🤖 Ares: Error de conexión con el núcleo."

    resp = MessagingResponse()
    resp.message(respuesta_ares)
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
