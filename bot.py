# Dentro de tu función de WhatsApp en bot.py
payload = {
    "contents": [{"parts": [{"text": msg_recibido}]}]
}
response = requests.post(URL_API, json=payload)
data = response.json()
respuesta_ares = data["candidates"][0]["content"]["parts"][0]["text"]
