import imaplib
import email
from email.header import decode_header
import streamlit as st
import pandas as pd
import time

# Configuración del servidor IMAP
IMAP_SERVER = "mail.tudominio.com"  # Cambia esto por tu servidor IMAP
IMAP_PORT = 993  # IMAP seguro por SSL

st.title("📧 Bandeja de Entrada")

# Variables de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "selected_email" not in st.session_state:
    st.session_state.selected_email = None

if not st.session_state.logged_in:
    # Campos de login
    email_user = st.text_input("Correo Electrónico:", placeholder="usuario@tudominio.com")
    password = st.text_input("Contraseña:", type="password", placeholder="••••••••")

    if st.button("Iniciar Sesión"):
        try:
            st.session_state.mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
            st.session_state.mail.login(email_user, password)
            st.session_state.logged_in = True
            st.session_state.email_user = email_user
            st.session_state.password = password
            st.rerun()
        except imaplib.IMAP4.error as e:
            st.error(f"❌ Error de autenticación: {e}")

# Si ya inició sesión, mostrar correos en tabla y actualizar cada 1 min
if st.session_state.logged_in:
    st.success(f"✅ Conectado como {st.session_state.email_user}")

    # Contenedor de layout: dividir en 2 columnas
    col1, col2 = st.columns([2, 3])  # 2: lista de correos, 3: contenido del correo

    with col1:
        st.subheader("📩 Correos Recibidos")
        
        while True:
            try:
                mail = st.session_state.mail
                mail.select("INBOX")  # Seleccionar bandeja de entrada

                # Buscar todos los correos (cambiar "ALL" a "UNSEEN" si solo quieres no leídos)
                status, messages = mail.search(None, "ALL")

                mail_ids = messages[0].split()

                if mail_ids:
                    data = []
                    mail_map = {}

                    for mail_id in reversed(mail_ids[-10:]):  # Últimos 10 correos
                        _, msg_data = mail.fetch(mail_id, "(RFC822)")
                        for response_part in msg_data:
                            if isinstance(response_part, tuple):
                                msg = email.message_from_bytes(response_part[1])

                                # Obtener remitente, asunto y fecha
                                sender = msg["From"]
                                subject, encoding = decode_header(msg["Subject"])[0]
                                if isinstance(subject, bytes):
                                    subject = subject.decode(encoding or "utf-8")
                                date = msg["Date"]

                                # Guardar referencia del email
                                mail_map[subject] = msg

                                # Agregar a la lista
                                data.append([date, subject, sender])

                    # Convertir en DataFrame
                    df = pd.DataFrame(data, columns=["📅 Fecha", "📨 Asunto", "🏷️ Remitente"])
                    selected = st.selectbox("Selecciona un correo:", df["📨 Asunto"].tolist(), key="email_select")

                    # Almacenar el correo seleccionado en la sesión
                    if selected:
                        st.session_state.selected_email = mail_map[selected]

                else:
                    st.info("📭 No tienes correos nuevos.")

            except Exception as e:
                st.error(f"⚠️ Error al recuperar los correos: {str(e)}")

            time.sleep(60)  # Refrescar cada minuto
            st.rerun()

    # **📬 Contenedor de correo seleccionado**
    with col2:
        if st.session_state.selected_email:
            st.subheader("📄 Contenido del correo")
            email_msg = st.session_state.selected_email

            # Decodificar el cuerpo del mensaje
            body = ""
            if email_msg.is_multipart():
                for part in email_msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = email_msg.get_payload(decode=True).decode()

            # Mostrar contenido
            st.text_area("📜 Contenido:", body, height=300)
