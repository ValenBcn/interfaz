import imaplib
import email
from email.header import decode_header
import streamlit as st

# Estilo CSS mejorado
st.markdown(
    """
 <style>
    /* Fondo general de la aplicación */
    .stApp {
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 auto !important;
        background-color: white !important; /* Fondo blanco */
        color: black !important; /* Texto en negro */
    }

    /* Contenedor principal */
    .block-container {
        max-width: 100% !important;
        background: white !important;
        padding: 20px;
        color: black !important; /* Texto en negro */
    }

    /* Títulos en azul */
    h1, h2, h3, h4, h5, h6 {
        color: #3B81F6 !important; /* Azul corporativo */
    }

    /* Botones con azul corporativo */
    .stButton>button {
        background-color: #3B81F6 !important;
        color: white !important;
        border-radius: 5px !important;
        padding: 10px !important;
    }

    /* Campos de entrada */
    input, textarea {
        border: 1px solid #3B81F6 !important;
        border-radius: 5px;
        color: black !important; /* Texto en negro */
    }

    /* Lista de correos */
    .email-list {
        border-right: 2px solid #ddd;
        overflow-y: auto;
        max-height: 500px;
        padding: 10px;
        color: black !important; /* Texto en negro */
    }

    .email-item {
        padding: 12px;
        border-bottom: 1px solid #ddd;
        cursor: pointer;
        transition: background 0.2s;
        background: #f9f9f9;
        border-radius: 5px;
        color: black !important; /* Texto en negro */
    }

    .email-item:hover {
        background: #d0e1ff !important;
    }

    /* Contenedor del correo seleccionado */
    .email-body {
        padding: 15px;
        background: white;
        border-left: 3px solid #3B81F6;
        max-height: 500px;
        overflow-y: auto;
        color: black !important; /* Texto en negro */
    }

    /* Mensaje de selección de correo */
    .stAlert {
        background-color: #dcebfe !important; /* Azul claro */
        color: black !important; /* Texto en negro */
    }
</style>
    """,
    unsafe_allow_html=True
)

# Configuración del servidor IMAP
IMAP_SERVER = "mail.datatobe.com"  # Servidor IMAP
IMAP_PORT = 993  # Puerto SSL seguro

st.title("📧 Bandeja de Entrada")

# Variables de sesión
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.selected_email = None  # Variable para almacenar el correo seleccionado

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

        # Buscar los últimos 10 correos
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

                        # Extraer cuerpo del email
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode(errors="ignore")
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode(errors="ignore")

                        emails.append({"Fecha": date, "Asunto": subject, "Remitente": sender, "Cuerpo": body, "ID": mail_id})

            # 📌 **Diseño en columnas** 
            col1, col2 = st.columns([2, 3])

            # **Columna Izquierda - Lista de correos**
            with col1:
                st.subheader("📥 Correos Recibidos")
                for email_data in emails:
                    button_key = f"email_{email_data['ID']}"
                    if st.button(f"✉️ {email_data['Asunto']} - {email_data['Remitente']}", key=button_key):
                        st.session_state.selected_email = email_data

            # **Columna Derecha - Cuerpo del correo seleccionado**
            with col2:
                if st.session_state.selected_email:
                    email_selected = st.session_state.selected_email
                    st.subheader(f"📜 {email_selected['Asunto']}")
                    st.write(f"**De:** {email_selected['Remitente']}")
                    st.write(f"**Fecha:** {email_selected['Fecha']}")
                    st.write("---")
                    st.write(email_selected["Cuerpo"])
                else:
                    st.info("Selecciona un correo para leerlo.")

        else:
            st.info("📭 No tienes correos nuevos.")

    except Exception as e:
        st.error(f"⚠️ Error al recuperar los correos: {str(e)}")
