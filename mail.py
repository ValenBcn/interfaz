import imaplib
import streamlit as st

# Configuración del servidor IMAP
IMAP_SERVER = "mail.datatobe.com"  # Cambia esto por tu servidor IMAP
IMAP_PORT = 993  # IMAP seguro por SSL

st.title("📧 Diagnóstico de Conexión IMAP")

# Pedir credenciales al usuario
email = st.text_input("Correo Electrónico:", placeholder="usuario@tudominio.com")
password = st.text_input("Contraseña:", type="password", placeholder="••••••••")

if st.button("Probar Conexión"):
    try:
        st.write("⏳ Intentando conectar al servidor IMAP...")
        
        # Intentar conectar con un timeout para evitar bloqueos
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(email, password)

        st.success("✅ Conexión exitosa con el servidor IMAP")
        
        # Listar los buzones disponibles
        st.write("📂 Carpetas disponibles en el servidor:")
        status, folders = mail.list()
        if status == "OK":
            for folder in folders:
                st.write(f"📁 {folder.decode()}")  # Decodificar UTF-8
        else:
            st.warning("⚠️ No se pudieron obtener las carpetas del correo.")

        mail.logout()

    except imaplib.IMAP4.error as e:
        st.error(f"❌ Error de autenticación: {e}")
    except Exception as e:
        st.error(f"⚠️ Error desconocido: {str(e)}")
