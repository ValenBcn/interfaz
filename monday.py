import streamlit as st
import requests

# Configuración de la API
API_KEY = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQ4NDExMTkyNCwiYWFpIjoxMSwidWlkIjo3MzMxMDUyOCwiaWFkIjoiMjAyNS0wMy0xMVQxNzo1NToyNS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6Mjg0ODc4MzgsInJnbiI6ImV1YzEifQ.Pp_UNPi-wRC1Y9yxFEQ_Rs9VC2J78QLjK58x7puQBAM'
BOARD_ID = '1863450371'
API_URL = 'https://api.monday.com/v2'

# Función para realizar consultas a la API de monday.com
def monday_api_query(query, variables=None):
    headers = {
        'Authorization': API_KEY
    }
    data = {
        'query': query,
        'variables': variables
    }
    response = requests.post(API_URL, json=data, headers=headers)
    return response.json()

# Consulta para obtener los elementos del tablero
query = '''
{
    boards(ids: ''' + BOARD_ID + ''') {
        name
        items {
            name
            column_values {
                title
                text
            }
        }
    }
}
'''

# Realizar la consulta
data = monday_api_query(query)

# Procesar y mostrar los datos en Streamlit
if 'data' in data:
    board = data['data']['boards'][0]
    st.title(f"Tablero: {board['name']}")
    for item in board['items']:
        st.subheader(f"Tarea: {item['name']}")
        for column in item['column_values']:
            st.write(f"**{column['title']}**: {column['text']}")
else:
    st.error("No se pudieron obtener los datos del tablero.")
