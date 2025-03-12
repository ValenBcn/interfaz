import streamlit as st
import requests

# Configuración de la API de Monday.com
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQ4NDExMTkyNCwiYWFpIjoxMSwidWlkIjo3MzMxMDUyOCwiaWFkIjoiMjAyNS0wMy0xMVQxNzo1NToyNS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjg0ODc4MzgsInJnbiI6ImV1YzEifQ.Pp_UNPi-wRC1Y9yxFEQ_Rs9VC2J78QLjK58x7puQBAM"
BOARD_ID = "1863450371"
API_URL = "https://api.monday.com/v2"

# Consulta GraphQL para obtener las tareas
QUERY = """
{
    boards(ids: %s) {
        id
        name
        items_page {
            items {
                id
                name
            }
        }
    }
}
""" % BOARD_ID

def get_monday_tasks():
    headers = {
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.post(API_URL, json={"query": QUERY}, headers=headers)
    data = response.json()
    
    if "errors" in data:
        st.error("Error al obtener los datos de Monday.com")
        st.json(data)  # Muestra los errores en la interfaz
        return []
    
    if not data.get("data") or not data["data"].get("boards"):
        st.warning("No se encontraron tableros con este ID.")
        return []
    
    board = data["data"]["boards"][0]
    tasks = board["items_page"]["items"]
    
    return tasks

# ---- INTERFAZ STREAMLIT ----
st.title("📋 Tareas en Monday.com")
st.subheader(f"Tablero: HR (ID: {BOARD_ID})")

tasks = get_monday_tasks()

if tasks:
    for task in tasks:
        st.write(f"- **{task['name']}**")
else:
    st.info("No hay tareas disponibles.")
