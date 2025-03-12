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

    # Refrescar cada 60 segundos
    while True:
        try:
            mail = st.session_state.mail
            mail.select("INBOX")  # Seleccionar bandeja de entrada

            # Buscar todos los correos (puedes cambiar a UNSEEN si solo quieres los no leídos)
            status, messages = mail.search(None, "ALL")

            mail_ids = messages[0].split()

            # Si hay correos
            if mail_ids:
                st.write(f"📩 **Mostrando últimos {min(len(mail_ids), 10)} correos**")

                data = []

                for mail_id in reversed(mail_ids[-10:]):  # Muestra los 10 más recientes
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

                            # Agregar a la lista de datos
                            data.append([date, subject, sender])

                # Convertir en DataFrame y mostrar en tabla
                df = pd.DataFrame(data, columns=["📅 Fecha", "📨 Asunto", "🏷️ Remitente"])
                st.dataframe(df, use_container_width=True)

            else:
                st.info("📭 No tienes correos nuevos.")

        except Exception as e:
            st.error(f"⚠️ Error al recuperar los correos: {str(e)}")

        time.sleep(60)  # Espera 1 minuto antes de actualizar
        st.rerun()  # Refrescar automáticamente
