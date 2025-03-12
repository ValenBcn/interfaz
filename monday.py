import streamlit as st
import requests
import json

# Configuración de la API
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQ4NDExMTkyNCwiYWFpIjoxMSwidWlkIjo3MzMxMDUyOCwiaWFkIjoiMjAyNS0wMy0xMVQxNzo1NToyNS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjg0ODc4MzgsInJnbiI6ImV1YzEifQ.Pp_UNPi-wRC1Y9yxFEQ_Rs9VC2J78QLjK58x7puQBAM"  # Reemplaza con tu clave
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

# ✅ Aplicando estilos
st.markdown(
    f"""
    <style>
        .main-container {{
            background-color: #2B6CB0;
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            max-width: 40%;
            margin: auto;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        }}
        .task-item {{
            background: rgba(255, 255, 255, 0.2);
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            text-align: left;
        }}
        .task-title {{
            font-size: 18px;
            font-weight: bold;
        }}
        .task-detail {{
            font-size: 14px;
            margin: 5px 0;
        }}
        .task-container {{
            padding: 15px;
            border-radius: 10px;
            background-color: #1E4A7B;
            margin-bottom: 10px;
            color: white;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

#st.markdown(f'<div class="main-container"><h2>📋 Tareas en **{board_name}**</h2></div>', unsafe_allow_html=True)
st.markdown(f'<div class="main-container"><h2>📋 <a href="https://datatobe.monday.com/boards/{BOARD_ID}" target="_blank" style="color: white; text-decoration: none;">Tareas en {board_name}</a></h2></div>', unsafe_allow_html=True)

for task in tasks:
    task_name = task["name"]
    columns = {col["id"]: json.loads(col["value"]) if col["value"] else None for col in task["column_values"]}

    # Extraer valores
    start_date = columns.get("project_timeline", {}).get("from", "No definido")
    due_date = columns.get("project_timeline", {}).get("to", "No definido")
    status = columns.get("project_status", {}).get("index", "No definido")
    priority = columns.get("priority_1", {}).get("index", "No definido")
    notes = columns.get("text9", "No definido")

    # Mapear el índice del estado a nombres reales
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

    # Mostrar en formato visualmente atractivo
    st.markdown(f"""
    <div class="task-container">
        <h3 class="task-title">📝 {task_name}</h3>
        <p class="task-detail">📅 <strong>Inicio:</strong> {start_date} | ⏳ <strong>Vencimiento:</strong> {due_date}</p>
        <p class="task-detail">🔴 <strong>Estado:</strong> {status_text} | ⭐ <strong>Prioridad:</strong> {priority_text}</p>
        <p class="task-detail">📄 <strong>Notas:</strong> {notes if notes else "No definido"}</p>
    </div>
    """, unsafe_allow_html=True)
