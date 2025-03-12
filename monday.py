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

# **Aplicar Estilos Globales**
st.markdown(
    """
    <style>
        /* Fondo blanco y alineación general */
        .stApp {
            max-width: 100% !important;
            background-color: white !important;
            padding: 20px;
        }

        /* Contenedor principal */
        .block-container {
            max-width: 100%;
            margin: auto;
            background: white;
        }

        /* Títulos y subtítulos */
        h1, h2, h3, h4, h5, h6 {
            color: #3B81F6 !important; /* Azul corporativo */
            font-weight: bold;
        }

        /* Bordes y mejoras en alertas */
        .stAlert {
            border-left: 5px solid #3B81F6 !important;
            background-color: #f0f4ff !important;
            padding: 15px;
        }

        /* Botones personalizados */
        .stButton>button {
            background-color: #3B81F6 !important;
            color: white !important;
            border-radius: 5px;
            padding: 10px;
        }

        /* Select box */
        .stSelectbox label {
            color: black !important; /* Texto en negro */
            font-weight: bold;
        }

        /* Contenedor con scroll para tareas */
        .scroll-container {
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 8px;
            background-color: #f8f9fa;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        }

        /* Tarjeta de tarea */
        .task-card {
            background: #fff;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            border-left: 5px solid #3B81F6;
        }

        /* Texto negro en tareas */
        .task-card * {
            color: black !important;
        }

        /* Links */
        a {
            color: #3B81F6 !important;
            text-decoration: none;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# **Filtro de estado**
selected_status = st.selectbox("📌 Filtrar por estado:", status_options)

# **Título con link al board**
st.markdown(f'<h2>📋 <a href="https://datatobe.monday.com/boards/{BOARD_ID}" target="_blank">Tareas en {board_name}</a></h2>', unsafe_allow_html=True)

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

    # **Mostrar tarea en un contenedor estilizado**
    st.markdown(f"""
    <div class="task-card">
        <h3>📝 {task_name}</h3>
        <p>📅 <strong>Inicio:</strong> {start_date} | ⏳ <strong>Vencimiento:</strong> {due_date}</p>
        <p>🔴 <strong>Estado:</strong> {status} | ⭐ <strong>Prioridad:</strong> {priority}</p>
        <p>📝 <strong>Notas:</strong> {notes if notes else "No definido"}</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Cierra el contenedor del scroll
