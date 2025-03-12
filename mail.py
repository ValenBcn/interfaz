import imaplib
import email
from email.header import decode_header
import streamlit as st
import pandas as pd

# Configuración del servidor IMAP
IMAP_SERVER = "mail.datatobe.com"  # Cambia esto por tu servidor IMAP
IMAP_PORT = 993  # Puerto seguro SSL

# Aplicar estilo CSS para colores y responsividad
st.markdown("""
    <style>
        /* Contenedor principal */
        .main-container {
            max-width: 100%; /* Ajusta el ancho completo */
            padding: 0px;
        }

        /* Ajusta la tabla */
        .email-table {
            width: 100%;
            overflow-x: auto;  /* Scroll horizontal si es necesario */
            white-space: nowrap;
        }

        .email-table table {
            width: 100%;
            min-width: 1000px; /* Hace que la tabla sea más ancha */
            border-collapse: collapse;
        }

        .email-table th {
            background-color: #3B81F6; /* Azul corporativo */
            color: white;
            padding: 12px;
            text-align: left;
        }

        .email-table td {
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }

        /* Asegurar responsividad */
        @media (max-width: 768px) {
            .email-table {
                overflow-x: scroll;
            }
        }

        /* Ajusta el ancho del cuerpo de Streamlit */
        .stApp {
            max-width: 100%;
            padding: 0px;
            margin: auto;
        }
    </style>
""", unsafe_allow_html=True)

#st.title("📧 Bandeja de Entrada")

# Variables de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    email_user = st.text_input("📩 Correo Electrónico:", placeholder="usuario@tudominio.com")
    password = st.text_input("🔑 Contraseña:", type="password", placeholder="••••••••")

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

# Si ya inició sesión, mostrar correos en tabla responsiva
if st.session_state.logged_in:
    st.success(f"✅ Conectado como [{st.session_state.email_user}](mailto:{st.session_state.email_user})")

    try:
        mail = st.session_state.mail
        mail.select("INBOX")  

        # Buscar los últimos 10 correos
        status, messages = mail.search(None, "ALL")
        mail_ids = messages[0].split()

        if mail_ids:
            data = []
            for mail_id in reversed(mail_ids[-10:]):  
                _, msg_data = mail.fetch(mail_id, "(RFC822)")
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])

                        sender = msg["From"]
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding or "utf-8")
                        date = msg["Date"]

                        # Extraer 500 caracteres del cuerpo del email
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode(errors="ignore")
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode(errors="ignore")

                        body_extract = body[:500] + "..." if len(body) > 500 else body  

                        data.append({"Fecha": date, "Asunto": subject, "Remitente": sender, "Extracto": body_extract})

            df = pd.DataFrame(data)

            # Contenedor responsivo para la tabla
            st.markdown('<div class="email-table">', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.info("📭 No tienes correos nuevos.")

    except Exception as e:
        st.error(f"⚠️ Error al recuperar los correos: {str(e)}")
