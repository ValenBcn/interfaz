import imaplib

IMAP_SERVER = "mail.datatobe.com"  # Cambia al servidor IMAP correcto
IMAP_PORT = 993
USERNAME = "demo@datatobe.com"
PASSWORD = "D3m0_2025"

try:
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(USERNAME, PASSWORD)
    print("✅ Conexión exitosa")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
