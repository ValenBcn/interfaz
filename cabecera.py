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
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        response = requests.get(weather_url)
        weather_data = response.json()
        temp = weather_data.get("current_weather", {}).get("temperature", "No disponible")
        forecast_max = weather_data.get("daily", {}).get("temperature_2m_max", ["No disponible"])[0]
        forecast_min = weather_data.get("daily", {}).get("temperature_2m_min", ["No disponible"])[0]
        return temp, forecast_max, forecast_min
    except:
        return "No disponible", "No disponible", "No disponible"

def main():
    city, country, lat, lon = get_user_location()
    temp, forecast_max, forecast_min = get_weather(lat, lon)
    now = datetime.datetime.now()
    formatted_date = now.strftime("%A, %d %B %Y")
    formatted_time = now.strftime("%I:%M %p")
    
    st.markdown(
        """
        <style>
            .header-container {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                align-items: center;
                gap: 10px;
                padding: 10px;
                background: #3B81F6;
                color: white;
                border-radius: 8px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
                font-family: 'Arial', sans-serif;
                max-width: 100%;
                overflow: hidden;
            }
            .header-item {
                display: flex;
                align-items: center;
                gap: 5px;
                background: #4C8BF5;
                padding: 10px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                color: white;
                text-align: center;
                flex: 1 1 auto;
                min-width: 120px;
                max-width: 200px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            }
            @media (min-width: 801px) {
                .header-container {
                    flex-wrap: nowrap;
                }
            }
            @media (max-width: 800px) {
                .header-container {
                    flex-direction: column;
                }
                .header-item {
                    width: 100%;
                    max-width: none;
                }
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        f"""
        <div class='header-container'>
            <div class='header-item'>&#x1F4CD; Ciudad: {city}, {country}</div>
            <div class='header-item'>&#x1F4C5; Fecha: {formatted_date}</div>
            <div class='header-item'>&#x23F0; Hora Local: {formatted_time}</div>
            <div class='header-item'>&#x1F321; Temperatura: {temp}°C</div>
            <div class='header-item'>&#x1F52E; Previsión: Máx: {forecast_max}°C / Mín: {forecast_min}°C</div>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
