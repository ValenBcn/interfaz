import streamlit as st
import requests

# Configuración de la API de Monday.com
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQ4NDExMTkyNCwiYWFpIjoxMSwidWlkIjo3MzMxMDUyOCwiaWFkIjoiMjAyNS0wMy0xMVQxNzo1NToyNS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjg0ODc4MzgsInJnbiI6ImV1YzEifQ.Pp_UNPi-wRC1Y9yxFEQ_Rs9VC2J78QLjK58x7puQBAM"
BOARD_ID = "1863450371"
API_URL = "https://api.monday.com/v2"

# Consulta GraphQL para obtener el nombre del board, tareas y atributos
QUERY = """
{
    boards(ids: %s) {
        id
        name
        items_page {
            items {
                id
                name
                column_values {
                    id
                    text
                }
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
        return None, []
    
    if not data.get("data") or not data["data"].get("boards"):
        st.warning("No se encontraron tableros con este ID.")
        return None, []
    
    board = data["data"]["boards"][0]
    tasks = board["items_page"]["items"]
    
    return board["name"], tasks

# ---- INTERFAZ STREAMLIT ----
board_name, tasks = get_monday_tasks()

if board_name:
    st.title(f"📋 Tareas en {board_name}")

if tasks:
    for task in tasks:
        # Inicializar valores con "No definido" por si no existen
        start_date = "No definido"
        due_date = "No definido"
        status = "No definido"
        priority = "No definido"
        notes = "No definido"

        for column in task["column_values"]:
            if column["id"] == "start_date" and column["text"]:
                start_date = column["text"]
            if column["id"] == "due_date" and column["text"]:
                due_date = column["text"]
            if column["id"] == "status" and column["text"]:
                status = column["text"]
            if column["id"] == "priority" and column["text"]:
                priority = column["text"]
            if column["id"] == "notes" and column["text"]:
                notes = column["text"]

        st.write(f"📝 **{task['name']}**")
        st.write(f"   📅 **Inicio:** {start_date}  |  ⏳ **Vencimiento:** {due_date}")
        st.write(f"   🔴 **Estado:** {status}  |  ⭐ **Prioridad:** {priority}")
        st.write(f"   📝 **Notas:** {notes}")
        st.markdown("---")  # Línea separadora entre tareas

else:
    st.info("No hay tareas disponibles.")
