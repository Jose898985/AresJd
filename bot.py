import google.generativeai as genai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Tu clave que ya confirmamos que funciona en la web
CLAVE = "AIzaSyAGRktuSRioeoFdInaffp7erkkMnkR-5Io"
genai.configure(api_key=CLAVE)

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    mensaje_usuario = request.values.get('Body', '')
    resp = MessagingResponse()
    
    try:
        # Usamos el modelo más rápido disponible
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(mensaje_usuario)
        
        # Limpiamos la respuesta para que no tenga errores de formato
        texto_ares = response.text.strip()
        resp.message(texto_ares)
        
    except Exception as e:
        # Si falla la IA, que el bot nos diga el error exacto por WhatsApp
        resp.message(f"🤖 Ares: Error en el núcleo. {str(e)[:50]}")
        
    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
