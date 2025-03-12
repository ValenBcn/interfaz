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
        temp = weather_data["current_weather"]["temperature"]
        forecast_max = weather_data["daily"]["temperature_2m_max"][0]
        forecast_min = weather_data["daily"]["temperature_2m_min"][0]
        return temp, forecast_max, forecast_min
    except:
        return "No disponible", "No disponible", "No disponible"

def main():
    st.markdown("""
        <style>
            .weather-container {
                max-width: 100%;
                background: #1E88E5;
                color: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                text-align: center;
                font-family: 'Arial', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-wrap: wrap;
                gap: 10px;
            }
            .weather-item {
                display: flex;
                align-items: center;
                gap: 5px;
                background: rgba(255, 255, 255, 0.2);
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
            }
            .weather-icon {
                font-size: 18px;
            }
        </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="weather-container">', unsafe_allow_html=True)
    
    city, country, lat, lon = get_user_location()
    temp, forecast_max, forecast_min = get_weather(lat, lon)
    
    now = datetime.datetime.now()
    formatted_date = now.strftime("%A, %d %B %Y")
    formatted_time = now.strftime("%I:%M %p")
    
    st.markdown(f"<div class='weather-item'><span class='weather-icon'>📍</span><strong> Ciudad:</strong> {city}, {country}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='weather-item'><span class='weather-icon'>📅</span><strong> Fecha:</strong> {formatted_date}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='weather-item'><span class='weather-icon'>⏰</span><strong> Hora Local:</strong> {formatted_time}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='weather-item'><span class='weather-icon'>🌡</span><strong> Temperatura:</strong> {temp}°C</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='weather-item'><span class='weather-icon'>🔮</span><strong> Previsión:</strong> Máx: {forecast_max}°C / Mín: {forecast_min}°C</div>", unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

