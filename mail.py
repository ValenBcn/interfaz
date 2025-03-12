import streamlit as st

st.title("📧 Accede a tu Correo Empresarial")

# Input para ingresar el correo (solo para prellenar, no se almacena)
email_user = st.text_input("Correo electrónico", placeholder="correo@tu-dominio.com")

# URL de Webmail en HostGator (ajústala según tu dominio)
webmail_url = "https://webmail.datatobe.com/"  

# Verifica si el usuario ingresó un correo antes de mostrar Webmail
if email_user:
    st.markdown(f"""
        <iframe src="{webmail_url}" width="100%" height="600px" style="border:none;"></iframe>
    """, unsafe_allow_html=True)
