import streamlit as st
import imaplib
import email

st.title("📬 Correos Recientes")

# Usuario y contraseña
user = st.text_input("Correo:", placeholder="usuario@tu-dominio.com")
password = st.text_input("Contraseña:", type="password", placeholder="••••••••")

if st.button("📩 Consultar Correos"):
    try:
        # Conectar al servidor IMAP de HostGator
        mail = imaplib.IMAP4_SSL("mail.datatobe.com")
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
                    st.markdown(f"**📧 {msg['From']} - {msg['Subject']}**")
                    st.write(f"🗓 {msg['Date']}")
                    st.write("---")

        mail.logout()
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
