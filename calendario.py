import streamlit as st
import requests
import datetime
import calendar

# Configuración del diseño de la página
title_color = "#3B81F6"  # Azul corporativo
st.markdown(f"""
    <style>
        .title-text {{ color: {title_color}; text-align: center; font-size: 24px; font-weight: bold; }}
        .calendar-container {{ text-align: center; }}
    </style>
""", unsafe_allow_html=True)

st.markdown('<h2 class="title-text">📅 Calendario Laboral</h2>', unsafe_allow_html=True)

# Obtener lista de países de la API
country_api = "https://date.nager.at/Api/v2/AvailableCountries"
countries_response = requests.get(country_api).json()

# Diccionario para seleccionar países
countries = {country['key']: country['value'] for country in countries_response}
selected_country = st.selectbox("Selecciona un país", list(countries.keys()), format_func=lambda x: countries[x])

# Obtener el año actual y mes actual
year = datetime.datetime.now().year
month = datetime.datetime.now().month

# Obtener los días festivos para el país seleccionado
holiday_api = f"https://date.nager.at/Api/v2/PublicHolidays/{year}/{selected_country}"
holidays_response = requests.get(holiday_api).json()

# Formatear los días festivos
holidays = {datetime.datetime.strptime(holiday['date'], '%Y-%m-%d').date(): holiday['localName'] for holiday in holidays_response}

# Crear el calendario en Streamlit
st.write(f"### {calendar.month_name[month]} {year}")
cal = calendar.Calendar()

days_grid = ""  # Generar una tabla para mostrar el calendario
for week in cal.monthdatescalendar(year, month):
    days_grid += "<tr>"
    for day in week:
        if day.month == month:
            color = "background-color: #f0f0f0;"  # Fondo normal
            if day in holidays:
                color = "background-color: #3B81F6; color: white; font-weight: bold;"  # Resaltar festivos
            days_grid += f'<td style="padding:10px; {color}">{day.day}</td>'
        else:
            days_grid += '<td></td>'  # Espacio vacío para días fuera del mes
    days_grid += "</tr>"

# Mostrar el calendario en Streamlit
st.markdown(f"""
<table style="width:100%; text-align: center; border-collapse: collapse;">
    <tr>{''.join([f'<th style="padding:10px; border-bottom: 2px solid {title_color};">{day}</th>' for day in ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']])}</tr>
    {days_grid}
</table>
""", unsafe_allow_html=True)
