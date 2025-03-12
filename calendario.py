import streamlit as st
import requests
import datetime
import calendar

# API para obtener los días festivos
HOLIDAYS_API_URL = "https://date.nager.at/api/v3/PublicHolidays"

# Diccionario de países disponibles y sus códigos
COUNTRIES = {
    "España": "ES",
    "México": "MX",
    "Francia": "FR",
    "Alemania": "DE",
    "Reino Unido": "GB",
    "Estados Unidos": "US"
}

# Diccionario de ciudades por país
CITIES = {
    "España": ["Madrid", "Barcelona"],
    "México": ["CDMX", "Guadalajara"],
    "Francia": ["París", "Lyon"],
    "Alemania": ["Berlín", "Múnich"],
    "Reino Unido": ["Londres", "Manchester"],
    "Estados Unidos": ["Nueva York", "Los Ángeles"]
}

# Obtener el año y mes actual
current_year = datetime.datetime.now().year
current_month = datetime.datetime.now().month

# Layout de filtros
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

# Selectores
with col1:
    country = st.selectbox("🌍 País", list(COUNTRIES.keys()), index=0)
with col2:
    city = st.selectbox("🏙️ Ciudad", CITIES[country], index=0)
with col3:
    selected_year = st.selectbox("📅 Año", list(range(current_year, current_year + 5)), index=0)
with col4:
    selected_month = st.selectbox("📆 Mes", list(calendar.month_name[1:]), index=current_month - 1)

# Obtener el código del país seleccionado
country_code = COUNTRIES[country]

# Obtener los días festivos del año seleccionado
response = requests.get(f"{HOLIDAYS_API_URL}/{selected_year}/{country_code}")
holidays = response.json() if response.status_code == 200 else []

# Filtrar días festivos por mes seleccionado
holidays_by_month = [
    h for h in holidays if int(h["date"].split("-")[1]) == (list(calendar.month_name[1:]).index(selected_month) + 1)
]

# Crear el calendario
st.markdown(f"### 📅 {selected_month} - {selected_year}")

# Obtener la estructura del mes
month_calendar = calendar.monthcalendar(selected_year, list(calendar.month_name[1:]).index(selected_month) + 1)

# Mostrar calendario en formato tabla
table = f"""
<style>
    .calendar-table {{
        border-collapse: collapse;
        width: 100%;
    }}
    .calendar-table th, .calendar-table td {{
        border: 1px solid #ccc;
        text-align: center;
        padding: 8px;
        font-size: 16px;
    }}
    .calendar-table th {{
        background-color: #3B81F6;
        color: white;
    }}
    .holiday {{
        background-color: #FFC107 !important;
        font-weight: bold;
    }}
</style>
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

# Mostrar días festivos del mes seleccionado
st.markdown(f"### 📌 Días festivos en {city}")
if holidays_by_month:
    for h in holidays_by_month:
        st.markdown(f"📅 **{h['date']}** - {h['localName']}")
else:
    st.write("No hay días festivos en este mes.")
