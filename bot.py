from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

app = Flask(__name__)
genai.configure(api_key="AIzaSyAGRktuSRioeoFdInaffp7erkkMnkR-5Io")

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    user_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    
    try:
        # Usamos el modelo flash-lite para que la respuesta sea instantánea
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        response = model.generate_content(user_msg)
        resp.message(response.text)
    except Exception as e:
        resp.message("🤖 Ares: El núcleo está procesando, intenta de nuevo.")
        
    return str(resp)
