import streamlit as st
import requests
import datetime

def get_user_location():
    try:
        ip_response = requests.get("https://ipapi.co/json/")
        ip_data = ip_response.json()
        city = ip_data.get("city", "Desconocido")
        country = ip_data.get("country_name", "Desconocido")
        lat = ip_data.get("latitude", 0)
        lon = ip_data.get("longitude", 0)
        return city, country, lat, lon
    except:
        return "Desconocido", "Desconocido", 0, 0

def get_weather(lat, lon):
    try:
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=weathercode&timezone=auto"
        response = requests.get(weather_url)
        weather_data = response.json()
        temp = weather_data.get("current_weather", {}).get("temperature", "No disponible")
        forecast_code = weather_data.get("daily", {}).get("weathercode", ["No disponible"])[0]
        return temp, forecast_code
    except:
        return "No disponible", "No disponible"

def get_weather_description(code, lang):
    descriptions = {
        "es": {"No disponible": "No disponible", "0": "Despejado", "1": "Parcialmente nublado", "2": "Nublado", "3": "Lluvia"},
        "en": {"No disponible": "Not available", "0": "Clear", "1": "Partly cloudy", "2": "Cloudy", "3": "Rain"},
        "de": {"No disponible": "Nicht verfügbar", "0": "Klar", "1": "Teilweise bewölkt", "2": "Bewölkt", "3": "Regen"},
        "ca": {"No disponible": "No disponible", "0": "Clar", "1": "Parcialment ennuvolat", "2": "Ennuvolat", "3": "Pluja"}
    }
    return descriptions.get(lang, descriptions["es"]).get(str(code), "No disponible")

def main():
    st.set_page_config(layout="wide")
    city, country, lat, lon = get_user_location()
    temp, forecast_code = get_weather(lat, lon)
    now = datetime.datetime.now()
    formatted_date = now.strftime("%A, %d %B %Y")
    
    lang_options = {"Español": "es", "English": "en", "Deutsch": "de", "Català": "ca"}
    lang_selected = st.selectbox("Selecciona un idioma / Select a language:", list(lang_options.keys()))
    lang = lang_options[lang_selected]
    
    weather_description = get_weather_description(forecast_code, lang)
    
    messages = {
        "es": f"Hola, hoy es {formatted_date}, el clima actual en {city} es de {temp}°C y esperamos que el día sea {weather_description} en las próximas horas.",
        "en": f"Hello, today is {formatted_date}, the current weather in {city} is {temp}°C and we expect the day to be {weather_description} in the next few hours.",
        "de": f"Hallo, heute ist {formatted_date}, das aktuelle Wetter in {city} beträgt {temp}°C und wir erwarten, dass der Tag in den nächsten Stunden {weather_description} sein wird.",
        "ca": f"Hola, avui és {formatted_date}, el clima actual a {city} és de {temp}°C i esperem que el dia sigui {weather_description} en les pròximes hores."
    }
    
    st.markdown(
        f"""
        <style>
            .weather-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                background: #3B81F6;
                color: white;
                padding: 15px;
                border-radius: 8px;
                font-size: 18px;
                font-family: 'Arial', sans-serif;
                width: calc(100% - 40px);
                margin: auto;
                text-align: center;
            }}
            @media (max-width: 600px) {{
                .weather-container {{
                    font-size: 14px;
                }}
            }}
        </style>
        <div class='weather-container'>{messages[lang]}</div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
