import streamlit as st
import imaplib
import email
from email.header import decode_header

st.title("📬 Correos Recientes")

# Usuario y contraseña
user = st.text_input("Correo:", placeholder="usuario@tu-dominio.com")
password = st.text_input("Contraseña:", placeholder="••••••••", type="password")

if st.button("📩 Consultar Correos"):
    try:
        # Conectar al servidor IMAP de HostGator
        mail = imaplib.IMAP4_SSL("mail.tu-dominio.com")  # Cambia por tu dominio
        mail.login(user, password)
        mail.select("inbox")

        # Obtener los 5 correos más recientes
        result, data = mail.search(None, "ALL")
        email_ids = data[0].split()[-5:]  # Últimos 5 correos

        for e_id in reversed(email_ids):
            _, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Decodificar el remitente y el asunto
                    from_name, encoding = decode_header(msg["From"])[0]
                    if isinstance(from_name, bytes):
                        from_name = from_name.decode(encoding or "utf-8")

                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")

                    date = msg["Date"]
                    
                    st.markdown(f"**📧 {from_name}** - {subject}")
                    st.write(f"🗓 {date}")
                    st.write("---")

        mail.logout()
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
