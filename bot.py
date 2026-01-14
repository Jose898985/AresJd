from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

# Tu clave y la URL v1 que ya habilitaste
CLAVE = "AIzaSyBuubE6NudTGNF2Y4uKDqNf1WG-koQfb7o"
URL_API = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={CLAVE}"

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    mensaje_usuario = request.values.get('Body', '')
    
    try:
        # Petición simplificada
        payload = {
            "contents": [{"parts": [{"text": f"Responde brevemente: {mensaje_usuario}"}]}]
        }
        headers = {'Content-Type': 'application/json'}
        r = requests.post(URL_API, json=payload, headers=headers, timeout=10)
        data = r.json()

        if "candidates" in data:
            respuesta_ares = data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            # Esto nos dirá exactamente qué modelo prefiere Google
            respuesta_ares = f"Google dice: {data.get('error', {}).get('message', 'Error de modelo')}"

    except Exception as e:
        respuesta_ares = "Error de conexión con el núcleo de Ares."

    resp = MessagingResponse()
    resp.message(respuesta_ares)
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
