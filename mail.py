import imaplib
import email
from email.header import decode_header
import streamlit as st

# Configuración del servidor IMAP
IMAP_SERVER = "mail.datatobe.com"  # Cambia esto por tu servidor IMAP
IMAP_PORT = 993  # IMAP seguro por SSL

st.title("📧 Bandeja de Entrada")

# Pedir credenciales al usuario
email_user = st.text_input("Correo Electrónico:", placeholder="usuario@tudominio.com")
password = st.text_input("Contraseña:", type="password", placeholder="••••••••")

if st.button("Iniciar Sesión"):
    try:
        st.write("⏳ Conectando al servidor IMAP...")
        
        # Conectar con IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(email_user, password)

        # Seleccionar la bandeja de entrada
        mail.select("INBOX")

        # Buscar todos los correos (puedes filtrar por UNSEEN para no leídos)
        status, messages = mail.search(None, "ALL")

        # Si hay correos
        if status == "OK":
            st.success("✅ Correos cargados correctamente.")

            # Obtener los últimos 10 correos
            mail_ids = messages[0].split()[-10:]

            for mail_id in reversed(mail_ids):  # Mostrar del más reciente al más antiguo
                _, msg_data = mail.fetch(mail_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        # Decodificar el email
                        msg = email.message_from_bytes(response_part[1])

                        # Obtener remitente
                        sender = msg["From"]
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8")

                        # Obtener fecha
                        date = msg["Date"]

                        # Mostrar en Streamlit
                        with st.expander(f"📩 {subject}"):
                            st.write(f"**📝 Remitente:** {sender}")
                            st.write(f"**📅 Fecha:** {date}")

                            # Si el correo tiene cuerpo, extraerlo
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode("utf-8", "ignore")
                                    st.write(f"📄 **Mensaje:**\n\n{body[:500]}...")  # Limitar a 500 caracteres

            mail.logout()
        else:
            st.warning("⚠️ No hay correos en la bandeja de entrada.")

    except imaplib.IMAP4.error as e:
        st.error(f"❌ Error de autenticación: {e}")
    except Exception as e:
        st.error(f"⚠️ Error desconocido: {str(e)}")
