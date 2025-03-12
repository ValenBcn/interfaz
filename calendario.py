import streamlit as st
import requests
import datetime
import calendar

# API para obtener los días festivos
HOLIDAYS_API_URL = "https://date.nager.at/api/v3/PublicHolidays"

# Diccionario de países y sus códigos
COUNTRIES = {
    "España": "ES",
    "México": "MX",
    "Francia": "FR",
    "Alemania": "DE",
    "Reino Unido": "GB",
    "Estados Unidos": "US"
}

# Obtener el año y mes actual
current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month
selected_year = current_year
selected_month = list(calendar.month_name[1:])[current_month - 1]

# **📌 Estilos CSS Mejorados**
st.markdown(
    """
    <style>
        /* Fondo general */
        .stApp {
            max-width: 100% !important;
            background-color: white !important;
            padding: 20px;
        }

        /* Contenedor del filtro */
        .filters-container {
            background: #DCE8FF !important;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 15px;
            text-align: center;
        }

        /* Estilos del selectbox */
        div[data-testid="stWidgetLabel"] label {
            color: black !important;
            font-weight: bold;
            font-size: 16px;
        }

        div[data-testid="stSelectbox"] {
            background-color: #DCE8FF !important;
            border-radius: 8px;
        }

        div[data-testid="stSelectbox"] div {
            background-color: #DCE8FF !important;
            color: black !important;
        }

        div[data-testid="stSelectbox"] select {
            background-color: #DCE8FF !important;
            color: black !important;
            font-size: 14px;
            padding: 10px;
        }

        div[data-testid="stSelectbox"] option {
            background-color: #DCE8FF !important;
            color: black !important;
        }

        /* Calendario */
        .calendar-title {
            font-size: 18px;
            font-weight: bold;
            color: black !important;
            text-align: center;
            margin-bottom: 5px;
        }

        .calendar-table {
            border-collapse: collapse;
            width: 100%;
            font-size: 16px;
            color: black !important;
        }

        .calendar-table th, .calendar-table td {
            border: 1px solid #ccc;
            text-align: center;
            padding: 8px;
            color: black !important;
        }

        .calendar-table th {
            background-color: #3B81F6;
            color: white;
        }

        .holiday {
            background-color: #FFC107 !important;
            font-weight: bold;
            color: black !important;
        }

        /* Contenedor de días festivos */
        .holidays-container {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
        }

        .holidays-title {
            font-size: 16px;
            font-weight: bold;
            color: black !important;
            text-align: center;
            margin-bottom: 5px;
        }

        .holiday-item {
            font-size: 14px;
            color: black !important;
            padding: 3px 0;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# **📌 Contenedor de filtro de país**
st.markdown('<div class="filters-container">', unsafe_allow_html=True)
country = st.selectbox("🌍 País", list(COUNTRIES.keys()), index=0)
st.markdown('</div>', unsafe_allow_html=True)  # Cierra el contenedor del filtro

# Obtener el código del país seleccionado
country_code = COUNTRIES[country]

# Obtener los días festivos del año seleccionado
response = requests.get(f"{HOLIDAYS_API_URL}/{selected_year}/{country_code}")
holidays = response.json() if response.status_code == 200 else []

# Filtrar días festivos por mes seleccionado
holidays_by_month = [
    h for h in holidays if int(h["date"].split("-")[1]) == (list(calendar.month_name[1:]).index(selected_month) + 1)
]

# **📅 Mostrar el calendario**
st.markdown(f'<div class="calendar-title">📅 {selected_month} - {selected_year}</div>', unsafe_allow_html=True)

# Obtener la estructura del mes
month_calendar = calendar.monthcalendar(selected_year, list(calendar.month_name[1:]).index(selected_month) + 1)

# Generar la tabla del calendario con los días festivos
table = f"""
<table class="calendar-table">
<tr>
    <th>Lun</th><th>Mar</th><th>Mié</th><th>Jue</th><th>Vie</th><th>Sáb</th><th>Dom</th>
</tr>
"""

# Mapeo de días festivos
holiday_dates = {int(h["date"].split("-")[2]): h["localName"] for h in holidays_by_month}

for week in month_calendar:
    table += "<tr>"
    for day in week:
        if day == 0:
            table += "<td></td>"
        elif day in holiday_dates:
            table += f'<td class="holiday">{day}</td>'
        else:
            table += f"<td>{day}</td>"
    table += "</tr>"

table += "</table>"

st.markdown(table, unsafe_allow_html=True)

# **📌 Días festivos del mes seleccionado**
st.markdown('<div class="holidays-container">', unsafe_allow_html=True)
st.markdown(f'<div class="holidays-title">📌 Días festivos en {country}</div>', unsafe_allow_html=True)

if holidays_by_month:
    for h in holidays_by_month:
        st.markdown(f'<div class="holiday-item">📅 <b>{h["date"]}</b> - {h["localName"]}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="holiday-item">No hay días festivos en este mes.</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Cierra el contenedor de días festivos
