from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)
CLAVE = "AIzaSyBuubE6NudTGNF2Y4uKDqNf1WG-koQfb7o"
MODELOS = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    usuario_msg = request.values.get('Body', '')
    respuesta_ares = "Error: No se pudo conectar con ningún modelo de IA."

    for mod in MODELOS:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{mod}:generateContent?key={CLAVE}"
            payload = {"contents": [{"parts": [{"text": usuario_msg}]}]}
            r = requests.post(url, json=payload, timeout=5)
            data = r.json()
            if "candidates" in data:
                respuesta_ares = data["candidates"][0]["content"]["parts"][0]["text"]
                break
        except:
            continue

    resp = MessagingResponse()
    resp.message(respuesta_ares)
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
