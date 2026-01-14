try:
        # Creamos el cliente en el momento del envío
        client = genai.Client(api_key=CLAVE)
        
        with st.chat_message("assistant"):
            # Cambiamos al modelo estable 1.5-flash
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt
            )
            
            respuesta_texto = response.text
            st.markdown(respuesta_texto)
            st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
            
    except Exception as e:
        # Si el error es de cuota (429), damos un mensaje más amigable
        if "429" in str(e):
            st.error("🚀 El sistema está saturado. Por favor, espera 30 segundos y vuelve a intentar.")
        else:
            st.error(f"ERROR DE SISTEMA: {e}")

