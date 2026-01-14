from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

CLAVE = "AIzaSyAGRktuSRioeoFdInaffp7erkkMnkR-5Io"
genai.configure(api_key=CLAVE)



@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    mensaje_usuario = request.values.get('Body', '')
    try:
        payload = {"contents": [{"parts": [{"text": f"Responde breve: {mensaje_usuario}"}]}]}
        r = requests.post(URL_API, json=payload, headers={'Content-Type': 'application/json'})
        data = r.json()
        respuesta_ares = data["candidates"][0]["content"]["parts"][0]["text"] if "candidates" in data else "🤖 Ares: Reintentando conexión..."
    except:
        respuesta_ares = "🤖 Ares: Error de red."

    resp = MessagingResponse()
    resp.message(respuesta_ares)
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
