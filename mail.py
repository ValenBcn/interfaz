import imaplib
import email
from email.header import decode_header
import streamlit as st
import pandas as pd

# Configuración del servidor IMAP
IMAP_SERVER = "mail.tudominio.com"  # Cambia esto por tu servidor IMAP
IMAP_PORT = 993  # Puerto seguro SSL

st.title("📧 Bandeja de Entrada")

# Variables de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Campos de login
    email_user = st.text_input("Correo Electrónico:", placeholder="usuario@tudominio.com")
    password = st.text_input("Contraseña:", type="password", placeholder="••••••••")

    if st.button("Iniciar Sesión"):
        try:
            # Conectar al servidor IMAP
            st.session_state.mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
            st.session_state.mail.login(email_user, password)
            st.session_state.logged_in = True
            st.session_state.email_user = email_user
            st.session_state.password = password
            st.rerun()
        except imaplib.IMAP4.error as e:
            st.error(f"❌ Error de autenticación: {e}")

# Si ya inició sesión, mostrar correos en tabla
if st.session_state.logged_in:
    st.success(f"✅ Conectado como {st.session_state.email_user}")

    try:
        mail = st.session_state.mail
        mail.select("INBOX")  # Seleccionar bandeja de entrada

        # Buscar los últimos 10 correos
        status, messages = mail.search(None, "ALL")
        mail_ids = messages[0].split()

        if mail_ids:
            data = []
            for mail_id in reversed(mail_ids[-10:]):  # Últimos 10 correos
                _, msg_data = mail.fetch(mail_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])

                        # Obtener fecha, asunto y remitente
                        sender = msg["From"]
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8")
                        date = msg["Date"]

                        # Extraer el contenido del email (500 caracteres)
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode(errors="ignore")
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode(errors="ignore")

                        body_extract = body[:500] + "..." if len(body) > 500 else body  # Limitar a 500 chars

                        # Agregar a la lista
                        data.append({"Fecha": date, "Asunto": subject, "Remitente": sender, "Extracto": body_extract})

            # Convertir en DataFrame y mostrar en tabla
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True)

        else:
            st.info("📭 No tienes correos nuevos.")

    except Exception as e:
        st.error(f"⚠️ Error al recuperar los correos: {str(e)}")
