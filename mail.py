import imaplib
import email
from email.header import decode_header
import streamlit as st

# Configuración del servidor IMAP
IMAP_SERVER = "mail.datatobe.com"  # Cambia esto por tu servidor IMAP
IMAP_PORT = 993  # IMAP seguro por SSL

st.title("📧 Bandeja de Entrada")

# Variables de sesión para ocultar el login después de iniciar sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    # Pedir credenciales al usuario
    email_user = st.text_input("Correo Electrónico:", placeholder="usuario@tudominio.com")
    password = st.text_input("Contraseña:", type="password", placeholder="••••••••")

    if st.button("Iniciar Sesión"):
        try:
            st.session_state.mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
            st.session_state.mail.login(email_user, password)
            st.session_state.logged_in = True  # Cambia el estado a loggeado
            st.session_state.email_user = email_user
            st.session_state.password = password
            st.rerun()
        except imaplib.IMAP4.error as e:
            st.error(f"❌ Error de autenticación: {e}")

# Si ya inició sesión, mostrar los correos
if st.session_state.logged_in:
    st.success(f"✅ Conectado como {st.session_state.email_user}")
    
    try:
        mail = st.session_state.mail
        mail.select("INBOX")  # Seleccionar bandeja de entrada

        # Buscar solo correos NO LEÍDOS
        status, messages = mail.search(None, "UNSEEN")

        mail_ids = messages[0].split()

        # Si hay correos nuevos
        if mail_ids:
            st.write(f"📩 **Tienes {len(mail_ids)} correos nuevos**")

            for mail_id in reversed(mail_ids[:10]):  # Muestra solo los 10 más recientes
                _, msg_data = mail.fetch(mail_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])

                        # Obtener remitente y asunto
                        sender = msg["From"]
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8")

                        # Obtener fecha
                        date = msg["Date"]

                        # Mostrar en Streamlit
                        st.write(f"📬 **{subject}**")
                        st.write(f"📅 {date} - ✉️ {sender}")
                        st.divider()

        else:
            st.info("📭 No tienes correos nuevos.")

    except Exception as e:
        st.error(f"⚠️ Error al recuperar los correos: {str(e)}")
