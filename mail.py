import streamlit as st

st.title("📧 Accede a tu Correo Empresarial")

email_user = st.text_input("Correo electrónico", placeholder="usuario@tu-dominio.com")

# URL de Webmail
webmail_url = "https://webmail.datatobe.com/"

st.markdown(
    f'<a href="{webmail_url}" target="_blank"><button style="background-color:#3B81F6; color:white; padding:10px 15px; border:none; border-radius:5px; cursor:pointer;">📩 Abrir Webmail</button></a>',
    unsafe_allow_html=True
)
