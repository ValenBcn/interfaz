import streamlit as st
import requests
import json

# Configuración de la API
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQ4NDExMTkyNCwiYWFpIjoxMSwidWlkIjo3MzMxMDUyOCwiaWFkIjoiMjAyNS0wMy0xMVQxNzo1NToyNS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjg0ODc4MzgsInJnbiI6ImV1YzEifQ.Pp_UNPi-wRC1Y9yxFEQ_Rs9VC2J78QLjK58x7puQBAM"  # Reemplaza con tu clave
BOARD_ID = "1863450371"  # ID del tablero HR
API_URL = "https://api.monday.com/v2"

# Consulta GraphQL corregida para obtener tareas y estados
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

# Mapeo de estados y prioridades
status_mapping = {
    0: "No iniciado",
    1: "Listo",
    2: "Detenido"
}
priority_mapping = {
    7: "Baja",
    109: "Media",
    110: "Alta"
}

# Obtener todos los estados disponibles en las tareas
status_options = list(set(status_mapping.get(json.loads(task["column_values"][1]["value"])["index"], "Desconocido") 
                          for task in tasks if task["column_values"][1]["value"]))
status_options.insert(0, "Todos")  # Agregar opción "Todos" al inicio

# **Filtro de estado**
selected_status = st.selectbox("📌 Filtrar por estado:", status_options)

# **Contenedor con scroll**
st.markdown(
    """
    <style>
        .scroll-container {
            max-height: 400px; /* Altura fija */
            overflow-y: auto;  /* Scroll vertical */
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 8px;
            background-color: #f8f9fa;
        }
    </style>
    """, unsafe_allow_html=True
)

# **Título con link al board**
st.markdown(f'<div class="main-container"><h2>📋 <a href="https://datatobe.monday.com/boards/{BOARD_ID}" target="_blank" style="color: white; text-decoration: none;">Tareas en {board_name}</a></h2></div>', unsafe_allow_html=True)

# **Contenedor con scroll**
st.markdown('<div class="scroll-container">', unsafe_allow_html=True)

# **Mostrar las tareas con el filtro aplicado**
for task in tasks:
    task_name = task["name"]
    columns = {col["id"]: json.loads(col["value"]) if col["value"] else None for col in task["column_values"]}

    # Extraer valores
    start_date = columns.get("project_timeline", {}).get("from", "No definido")
    due_date = columns.get("project_timeline", {}).get("to", "No definido")
    status = status_mapping.get(columns.get("project_status", {}).get("index"), "Desconocido")
    priority = priority_mapping.get(columns.get("priority_1", {}).get("index"), "Desconocida")
    notes = columns.get("text9", "No definido")

    # **Aplicar filtro de estado**
    if selected_status != "Todos" and status != selected_status:
        continue

    # **Mostrar tarea**
    st.markdown(f"""
    ### 📝 {task_name}
    - 📅 **Inicio:** {start_date} | ⏳ **Vencimiento:** {due_date}
    - 🔴 **Estado:** {status} | ⭐ **Prioridad:** {priority}
    - 📝 **Notas:** {notes if notes else "No definido"}
    ---
    """)

st.markdown('</div>', unsafe_allow_html=True)  # Cierra el contenedor del scroll
