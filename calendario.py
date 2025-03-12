import streamlit as st
import requests
import json
import datetime
import calendar

# 🎨 Configuración de colores
PRIMARY_COLOR = "#3B81F6"
SECONDARY_COLOR = "#f7f8ff"

# 📅 API gratuita para días festivos
HOLIDAY_API = "https://date.nager.at/api/v3/PublicHolidays"

# 🌍 Lista de países disponibles
COUNTRIES = {
    "España": "ES",
    "México": "MX",
    "Francia": "FR",
    "Alemania": "DE"
}

# Traducciones de textos según el país
TRANSLATIONS = {
    "ES": {"calendar": "Calendario Laboral", "holidays": "Días festivos"},
    "MX": {"calendar": "Calendario Laboral", "holidays": "Días festivos"},
    "FR": {"calendar": "Calendrier du Travail", "holidays": "Jours fériés"},
    "DE": {"calendar": "Arbeitskalender", "holidays": "Feiertage"}
}

# 📅 Obtener días festivos
@st.cache_data
def get_holidays(year, country_code):
    try:
        response = requests.get(f"{HOLIDAY_API}/{year}/{country_code}")
        if response.status_code == 200:
            return response.json()
    except Exception:
        return []
    return []

# 📌 Obtener fecha actual
today = datetime.datetime.now()
current_year = today.year
current_month = today.month

# 🌍 Selección de país y año
col1, col2 = st.columns([3, 1])
with col1:
    country_name = st.selectbox("Selecciona un país", list(COUNTRIES.keys()), index=0)
    country_code = COUNTRIES[country_name]

with col2:
    year = st.selectbox("", list(range(current_year, current_year + 3)), index=0)

# 📆 Selección de mes
month_names = {
    "ES": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    "MX": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    "FR": ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
    "DE": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
}

month = st.selectbox("Selecciona el mes", month_names[country_code], index=current_month - 1)

# 📌 Obtener días festivos
holidays = get_holidays(year, country_code)
holiday_dates = {datetime.datetime.strptime(h["date"], "%Y-%m-%d").day: h["localName"] for h in holidays if int(h["date"].split("-")[1]) == current_month}

# 📆 Mostrar título
st.markdown(f"<h2>{TRANSLATIONS[country_code]['calendar']} ({year})</h2>", unsafe_allow_html=True)

# 📅 Mostrar calendario
st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
st.markdown(f"### {month_names[country_code][current_month - 1]} {year}")

cal = calendar.TextCalendar()
month_days = cal.monthdayscalendar(year, current_month)

table = "<table style='width:100%; text-align:center; border-collapse: collapse;'>"
table += "<tr style='background-color: #444; color: white;'>"
for day in ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]:
    table += f"<th style='padding: 5px; border: 1px solid white;'>{day}</th>"
table += "</tr>"

for week in month_days:
    table += "<tr>"
    for day in week:
        if day == 0:
            table += "<td style='border: 1px solid #ccc;'></td>"
        elif day in holiday_dates:
            table += f"<td style='background-color: #FFCC00; font-weight: bold; border: 1px solid black;'>{day}</td>"
        else:
            table += f"<td style='border: 1px solid #ccc;'>{day}</td>"
    table += "</tr>"

table += "</table>"
st.markdown(table, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 📜 Mostrar lista de días festivos formateados
filtered_holidays = [h for h in holidays if int(h["date"].split("-")[1]) == current_month]

if filtered_holidays:
    st.markdown(f"### 📌 {TRANSLATIONS[country_code]['holidays']}")
    for h in filtered_holidays:
        date_formatted = datetime.datetime.strptime(h['date'], "%Y-%m-%d").strftime("%d/%m/%Y")
        st.markdown(f"📅 **{date_formatted}** - {h['localName']}")
else:
    st.warning("No se encontraron días festivos para este país y mes.")
