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

# 🌍 API para obtener países
COUNTRIES_API = "https://restcountries.com/v3.1/all"

# 🚀 Obtener lista de países
@st.cache_data
def get_countries():
    try:
        response = requests.get(COUNTRIES_API)
        if response.status_code == 200:
            countries = response.json()
            return sorted([(c["name"]["common"], c["cca2"]) for c in countries if "cca2" in c])
    except Exception as e:
        st.error("⚠️ No se pudieron cargar los países.")
        return []
    return []

# 📅 Obtener días festivos
@st.cache_data
def get_holidays(year, country_code):
    try:
        response = requests.get(f"{HOLIDAY_API}/{year}/{country_code}")
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error("⚠️ No se pudieron obtener los días festivos.")
        return []
    return []

# 🎨 Estilos personalizados
st.markdown(
    f"""
    <style>
        .calendar-container {{
            background-color: {SECONDARY_COLOR};
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            color: black;
            text-align: center;
        }}
        h2 {{
            color: {PRIMARY_COLOR};
            text-align: center;
        }}
        .holiday {{
            background-color: #FFCC00 !important;
            color: black;
            font-weight: bold;
            padding: 2px 5px;
            border-radius: 5px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# 📌 Encabezado
st.markdown(f'<h2>📅 Calendario Laboral</h2>', unsafe_allow_html=True)

# 🌍 Seleccionar país
countries = get_countries()
if countries:
    country_name, country_code = st.selectbox("Selecciona un país", countries, index=30)
else:
    st.error("No se pudieron cargar los países. Inténtalo más tarde.")

# 📆 Seleccionar año
current_year = datetime.datetime.now().year
year = st.selectbox("Selecciona el año", list(range(current_year, current_year + 3)))

# 📅 Obtener días festivos
if country_code:
    holidays = get_holidays(year, country_code)
    holiday_dates = {datetime.datetime.strptime(h["date"], "%Y-%m-%d").day: h["localName"] for h in holidays}

    # 📆 Mostrar calendario
    st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
    st.markdown(f"### {calendar.month_name[datetime.datetime.now().month]} {year}")

    cal = calendar.TextCalendar()
    month_days = cal.monthdayscalendar(year, datetime.datetime.now().month)

    table = "<table style='width:100%; text-align:center;'><tr>"
    for day in ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]:
        table += f"<th>{day}</th>"
    table += "</tr>"

    for week in month_days:
        table += "<tr>"
        for day in week:
            if day == 0:
                table += "<td></td>"
            elif day in holiday_dates:
                table += f"<td class='holiday'>{day}</td>"
            else:
                table += f"<td>{day}</td>"
        table += "</tr>"
    
    table += "</table>"
    st.markdown(table, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 📜 Mostrar lista de días festivos
if holidays:
    st.markdown("### 📌 Días festivos")
    for h in holidays:
        st.markdown(f"🗓️ **{h['date']}** - {h['localName']}")
else:
    st.warning("No se encontraron días festivos para este país y año.")
