import streamlit as st
import requests

# Configuración
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQ4NDExMTkyNCwiYWFpIjoxMSwidWlkIjo3MzMxMDUyOCwiaWFkIjoiMjAyNS0wMy0xMVQxNzo1NToyNS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjg0ODc4MzgsInJnbiI6ImV1YzEifQ.Pp_UNPi-wRC1Y9yxFEQ_Rs9VC2J78QLjK58x7puQBAM"
BOARD_ID = "1863450371"  # Board HR
API_URL = "https://api.monday.com/v2"

# Consulta GraphQL para extraer tareas y columnas
query = """
{
  boards(ids: %s) {
    name
    items_page {
      items {
        id
        name
        column_values {
          id
          title
          text
        }
      }
    }
  }
}
""" % BOARD_ID

# Headers para autenticación en Monday.com
headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY
}

# Realizar la petición
response = requests.post(API_URL, json={"query": query}, headers=headers)
data = response.json()

# Verificar si hay errores en la respuesta
if "errors" in data:
    st.error("Error al obtener datos de Monday.com")
    st.json(data)  # Mostrar el error en JSON para depuración
else:
    board_name = data["data"]["boards"][0]["name"]
    tasks = data["data"]["boards"][0]["items_page"]["items"]

    st.markdown(f"## 📋 Tareas en **{board_name}**")

    for task in tasks:
        task_name = task["name"]
        columns = {col["title"]: col["text"] for col in task["column_values"]}

        start_date = columns.get("Inicio", "No definido")
        due_date = columns.get("Vencimiento", "No definido")
        status = columns.get("Estado", "No definido")
        priority = columns.get("Prioridad", "No definido")
        notes = columns.get("Notas", "No definido")

        # Mostrar en formato atractivo
        st.markdown(f"""
        ### 📝 {task_name}
        - 📅 **Inicio:** {start_date} | ⏳ **Vencimiento:** {due_date}
        - 🔴 **Estado:** {status} | ⭐ **Prioridad:** {priority}
        - 📝 **Notas:** {notes}
        ---
        """)
