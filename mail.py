import streamlit as st

st.title("📧 Accede a tu Correo Empresarial")

# Ingresar correo (solo para prellenar, no se almacena)
email_user = st.text_input("Correo electrónico", placeholder="correo@tu-dominio.com")

# Mostrar Webmail en un iframe
if email_user:
    webmail_url = f"https://webmail.datatobe.com/"
    st.markdown(f'<iframe src="{webmail_url}" width="100%" height="600px"></iframe>', unsafe_allow_html=True)
