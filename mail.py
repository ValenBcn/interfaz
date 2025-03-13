import imaplib
import email
from email.header import decode_header
import streamlit as st

# Estilo CSS minimalista y responsivo
st.markdown(
    """
    <style>
        .stApp {
            max-width: 100% !important;
            padding: 10px !important;
            margin: 0 auto !important;
            background-color: white !important;
            color: black !important;
        }
        .email-container {
            padding: 10px;
            border-radius: 8px;
            background: #f9f9f9;
            box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
            max-height: 80vh;
            overflow-y: auto;
        }
        .email-header {
            font-size: 16px;
            font-weight: bold;
            color: #3B81F6 !important;
            padding-bottom: 5px;
            border-bottom: 2px solid #3B81F6;
            margin-bottom: 10px;
        }
        .email-item {
            padding: 10px;
            border-bottom: 1px solid #ddd;
            cursor: pointer;
            transition: background 0.2s;
            background: white;
            border-radius: 5px;
            font-size: 14px;
        }
        .email-item:hover {
            background: #d0e1ff !important;
        }
        .email-body {
            padding: 15px;
            background: white;
            border-left: 3px solid #3B81F6;
            max-height: 60vh;
            overflow-y: auto;
            font-size: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Configuración del servidor IMAP
IMAP_SERVER = "mail.datatobe.com"
IMAP_PORT = 993

# Variables de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.selected_email = None

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

# Si ya inició sesión, mostrar correos
if st.session_state.logged_in:
    st.success(f"✅ Conectado como [{st.session_state.email_user}](mailto:{st.session_state.email_user})")

    try:
        mail = st.session_state.mail
        mail.select("INBOX")
        status, messages = mail.search(None, "ALL")
        mail_ids = messages[0].split()

        if mail_ids:
            emails = []
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
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode(errors="ignore")
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode(errors="ignore")
                        emails.append({"Fecha": date, "Asunto": subject, "Remitente": sender, "Cuerpo": body, "ID": mail_id})

            col1, col2 = st.columns([2, 3])

            with col1:
                st.markdown("<div class='email-header'>📥 Correos Recibidos</div>", unsafe_allow_html=True)
                for email_data in emails:
                    if st.session_state.selected_email and st.session_state.selected_email["ID"] == email_data["ID"]:
                        st.markdown(f"<div class='email-item' style='background:#d0e1ff;'><strong>✉️ {email_data['Asunto']}</strong><br><small>{email_data['Remitente']}</small></div>", unsafe_allow_html=True)
                    else:
                        if st.button(f"✉️ {email_data['Asunto']} ({email_data['Remitente']})", key=f"email_{email_data['ID']}"):
                            st.session_state.selected_email = email_data

            with col2:
                if st.session_state.selected_email:
                    email_selected = st.session_state.selected_email
                    st.markdown(f"<div class='email-header'>📜 {email_selected['Asunto']}</div>", unsafe_allow_html=True)
                    st.markdown(f"**De:** {email_selected['Remitente']}")
                    st.markdown(f"**Fecha:** {email_selected['Fecha']}")
                    st.markdown("---")
                    st.markdown(email_selected["Cuerpo"])
                else:
                    st.info("Selecciona un correo para leerlo.")
        else:
            st.info("📭 No tienes correos nuevos.")
    except Exception as e:
        st.error(f"⚠️ Error al recuperar los correos: {str(e)}")
