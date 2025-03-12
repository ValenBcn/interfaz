import streamlit as st
import requests
import json

# Configuración de la API
API_KEY = "TU_API_KEY"  # Reemplaza con tu clave
BOARD_ID = "1863450371"  # ID del tablero HR
API_URL = "https://api.monday.com/v2"

# Consulta GraphQL corregida
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
          value
        }
      }
    }
  }
}
""" % BOARD_ID

# Headers para la autenticación
headers = {
    "Content-Type": "application/json",
    "Authorization": API_KEY
}

# Llamada a la API
response = requests.post(API_URL, json={"query": query}, headers=headers)
data = response.json()

# Si hay errores, mostramos el JSON completo para depuración
if "errors" in data:
    st.error("❌ Error al obtener datos de Monday.com")
    st.json(data)
    st.stop()

# Obtener el nombre del board y las tareas
board_name = data["data"]["boards"][0]["name"]
tasks = data["data"]["boards"][0]["items_page"]["items"]

st.markdown(f"## 📋 Tareas en **{board_name}**")

for task in tasks:
    task_name = task["name"]
    columns = {col["id"]: json.loads(col["value"]) if col["value"] else None for col in task["column_values"]}

    # Extraer valores
    start_date = columns.get("project_timeline", {}).get("from", "No definido")
    due_date = columns.get("project_timeline", {}).get("to", "No definido")
    status = columns.get("project_status", {}).get("index", "No definido")
    priority = columns.get("priority_1", {}).get("index", "No definido")
    notes = columns.get("text9", "No definido")

    # Mapear el índice del estado a nombres reales (Asegúrate de revisar en tu tablero los valores correctos)
    status_mapping = {
        0: "No iniciado",
        1: "Listo",
        2: "Detenido"
    }
    status_text = status_mapping.get(status, "Desconocido")

    # Mapear el índice de prioridad a nombres reales
    priority_mapping = {
        7: "Baja",
        109: "Media",
        110: "Alta"
    }
    priority_text = priority_mapping.get(priority, "Desconocida")

    # Mostrar en formato atractivo en Streamlit
    st.markdown(f"""
    ### 📝 {task_name}
    - 📅 **Inicio:** {start_date} | ⏳ **Vencimiento:** {due_date}
    - 🔴 **Estado:** {status_text} | ⭐ **Prioridad:** {priority_text}
    - 📝 **Notas:** {notes if notes else "No definido"}
    ---
    """)
