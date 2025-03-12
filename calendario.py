import streamlit as st
import requests
import json
import datetime
import calendar

# 🎨 Colores
PRIMARY_COLOR = "#3B81F6"
SECONDARY_COLOR = "#ffffff"  # Fondo blanco

# 📅 API gratuita para días festivos
HOLIDAY_API = "https://date.nager.at/api/v3/PublicHolidays"

# 🌍 Lista de países y ciudades predefinidas
COUNTRIES = {
    "España": {"code": "ES", "cities": ["Madrid", "Barcelona", "Valencia", "Sevilla"]},
    "México": {"code": "MX", "cities": ["CDMX", "Monterrey", "Guadalajara", "Cancún"]},
    "Francia": {"code": "FR", "cities": ["París", "Lyon", "Marsella", "Toulouse"]},
    "Alemania": {"code": "DE", "cities": ["Berlín", "Múnich", "Hamburgo", "Colonia"]}
}

# 📆 Traducción de nombres de meses
month_names = {
    "ES": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    "MX": ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    "FR": ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"],
    "DE": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Dezember"]
}

# 📌 Obtener fecha actual
today = datetime.datetime.now()
current_year = today.year
current_month = today.month

# 📌 Función para obtener días festivos
@st.cache_data
def get_holidays(year, country_code):
    try:
        response = requests.get(f"{HOLIDAY_API}/{year}/{country_code}")
        if response.status_code == 200:
            return response.json()
    except Exception:
        return []
    return []

# 📌 Fila de filtros (país, ciudad, año, mes)
with st.container():
    col1, col2, col3, col4 = st.columns([2, 2, 1, 1])

    # Selección de país
    with col1:
        country_name = st.selectbox("🌍 País", list(COUNTRIES.keys()), index=0)
        country_code = COUNTRIES[country_name]["code"]

    # Selección de ciudad
    with col2:
        city = st.selectbox("🏙 Ciudad", COUNTRIES[country_name]["cities"], index=0)

    # Selección de año
    with col3:
        year = st.selectbox("📅 Año", list(range(current_year, current_year + 3)), index=0)

    # Selección de mes
    with col4:
        month = st.selectbox("🗓 Mes", month_names[country_code], index=current_month - 1)

# 📌 Obtener días festivos para el país y año seleccionados
holidays = get_holidays(year, country_code)
holiday_dates = {datetime.datetime.strptime(h["date"], "%Y-%m-%d").day: h["localName"] for h in holidays if int(h["date"].split("-")[1]) == current_month}

# 📆 Mostrar título alineado al estilo
st.markdown(f"<h2 style='color:{PRIMARY_COLOR}; text-align:center;'>📅 Calendario Laboral {year}</h2>", unsafe_allow_html=True)

# 📅 Mostrar calendario con fondo blanco y resaltando días festivos
st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
st.markdown(f"### {month}")

cal = calendar.TextCalendar()
month_days = cal.monthdayscalendar(year, current_month)

# 📌 Renderizar el calendario con Streamlit
table = f"<table style='width:100%; text-align:center; border-collapse: collapse; background: {SECONDARY_COLOR};'>"
table += f"<tr style='background-color: {PRIMARY_COLOR}; color: white;'>"

for day in ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]:
    table += f"<th style='padding: 8px; border: 1px solid white;'>{day}</th>"
table += "</tr>"

for week in month_days:
    table += "<tr>"
    for day in week:
        if day == 0:
            table += "<td style='border: 1px solid #ccc; height:40px;'></td>"
        elif day in holiday_dates:
            table += f"<td style='background-color: #FFD700; font-weight: bold; border: 1px solid black;'>{day}</td>"
        else:
            table += f"<td style='border: 1px solid #ccc;'>{day}</td>"
    table += "</tr>"

table += "</table>"
st.markdown(table, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 📜 Mostrar lista de días festivos formateados (solo del mes seleccionado)
filtered_holidays = [h for h in holidays if int(h["date"].split("-")[1]) == current_month]

if filtered_holidays:
    st.markdown(f"### 📌 Días festivos en {city}")
    for h in filtered_holidays:
        date_formatted = datetime.datetime.strptime(h['date'], "%Y-%m-%d").strftime("%d/%m/%Y")
        st.markdown(f"📅 **{date_formatted}** - {h['localName']}")
else:
    st.warning("No se encontraron días festivos para este país y mes.")
