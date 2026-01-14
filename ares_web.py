try:
        # Cambiamos a 'gemini-pro' que es el nombre más estable y compatible
        model = genai.GenerativeModel("gemini-pro")
        
        with st.chat_message("assistant"):
            response = model.generate_content(prompt)
            
            # Verificamos que la respuesta tenga texto
            if response.text:
                respuesta_texto = response.text
                st.markdown(respuesta_texto)
                st.session_state.messages.append({"role": "assistant", "content": respuesta_texto})
            else:
                st.warning("El modelo recibió la orden pero no generó texto. Intenta de nuevo.")
            
    except Exception as e:
        # Si 'gemini-pro' también falla, intentamos con la versión 1.0 (el abuelo de todos)
        try:
            model_backup = genai.GenerativeModel("gemini-1.0-pro")
            response = model_backup.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.error(f"Error de conexión persistente: {e}")
