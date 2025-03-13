import streamlit as st
import requests
import json

# Configuración de la API
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQ4NDExMTkyNCwiYWFpIjoxMSwidWlkIjo3MzMxMDUyOCwiaWFkIjoiMjAyNS0wMy0xMVQxNzo1NToyNS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjg0ODc4MzgsInJnbiI6ImV1YzEifQ.Pp_UNPi-wRC1Y9yxFEQ_Rs9VC2J78QLjK58x7puQBAM"
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
    0: ("No iniciado", "🔴"),
    1: ("Listo", "🟢"),
    2: ("En curso", "🔵"),
    3: ("Detenido", "🔴")
}
priority_mapping = {
    7: "Baja",
    109: "Media",
    110: "Alta"
}

# **Aplicar Estilos Minimalistas**
st.markdown(
    """
    <style>
        .stApp {
            max-width: 100% !important;
            background-color: white !important;
            padding: 10px;
        }
        .scroll-container {
            max-height: 400px;
            overflow-y: auto;
            padding: 5px;
            border-radius: 8px;
            background-color: #f8f9fa;
            box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
        }
        .task-card {
            background: #fff;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 5px;
            box-shadow: 1px 1px 4px rgba(0, 0, 0, 0.1);
            border-left: 4px solid #3B81F6;
            font-size: 12px;
        }
        .task-title {
            font-weight: bold;
            font-size: 14px;
            color: black !important;
        }
        .task-info {
            font-size: 12px;
            color: #555;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        [data-testid="stToolbar"] {visibility: hidden !important;} /* Oculta la barra superior de Streamlit */
        .block-container {padding-top: 0px !important;} /* Elimina espacio superior */
        .stTextInput, .stSelectbox {display: none !important;} /* Oculta campos de texto/selección vacíos */
    </style>
    """,
    unsafe_allow_html=True
)

# **Mostrar las tareas con el filtro aplicado**
st.markdown('<div class="scroll-container">', unsafe_allow_html=True)

for task in tasks:
    task_name = task["name"]
    columns = {col["id"]: json.loads(col["value"]) if col["value"] else None for col in task["column_values"]}

    # Extraer valores
    start_date = columns.get("project_timeline", {}).get("from", "No definido")
    due_date = columns.get("project_timeline", {}).get("to", "No definido")
    status, status_icon = status_mapping.get(columns.get("project_status", {}).get("index"), ("Desconocido", "⚪"))
    priority = priority_mapping.get(columns.get("priority_1", {}).get("index"), "Desconocida")
    notes = columns.get("text9", "No definido")

    # **Mostrar tarea en un contenedor estilizado minimalista**
    st.markdown(f"""
    <div class="task-card">
        <p class="task-title">📝 {task_name}</p>
        <p class="task-info">📅 <strong>Inicio:</strong> {start_date} | ⏳ <strong>Vencimiento:</strong> {due_date}</p>
        <p class="task-info">{status_icon} <strong>Estado:</strong> {status} | ⭐ <strong>Prioridad:</strong> {priority}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Cierra el contenedor del scroll
