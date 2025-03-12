import streamlit as st
import imaplib
import email
from email.header import decode_header

# Configuración del servidor IMAP de HostGator
IMAP_SERVER = "mail.tudominio.com"  # Cambia esto por el servidor IMAP de tu dominio
IMAP_PORT = 993

# Título de la App
st.markdown("## 📧 Bandeja de Entrada")

# Formulario de Login
st.sidebar.header("🔐 Iniciar Sesión en Webmail")
email_user = st.sidebar.text_input("Correo Electrónico", placeholder="tuemail@tudominio.com")
password = st.sidebar.text_input("Contraseña", type="password", placeholder="••••••••")
login_button = st.sidebar.button("Iniciar Sesión")

if login_button and email_user and password:
    try:
        # Conectar a la cuenta de correo
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(email_user, password)
        mail.select("INBOX")  # Seleccionar la bandeja de entrada

        # Obtener los últimos 10 correos
        result, data = mail.search(None, "ALL")
        email_ids = data[0].split()[-10:]  # Últimos 10 correos

        st.markdown("### 📩 Últimos Correos")
        
        # Diccionario para almacenar correos
        emails = {}

        for num in email_ids[::-1]:  # Recorrer los IDs en orden descendente (más recientes primero)
            result, msg_data = mail.fetch(num, "(RFC822)")
            raw_email = msg_data[0][1]
            msg = email.message_from_bytes(raw_email)

            # Decodificar el asunto
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")

            # Obtener el remitente
            from_email = msg.get("From")

            # Obtener la fecha
            date = msg.get("Date")

            # Almacenar en el diccionario
            emails[num] = {"subject": subject, "from": from_email, "date": date, "content": msg}

            # Mostrar en Streamlit
            with st.expander(f"📨 {subject} ({date})"):
                st.markdown(f"**Remitente:** {from_email}")
                st.markdown(f"**Fecha:** {date}")

                # Extraer el contenido del correo
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                            break
                else:
                    body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")

                st.text_area("Contenido:", body, height=200)

        mail.logout()

    except Exception as e:
        st.error(f"⚠️ Error al conectar: {str(e)}")
