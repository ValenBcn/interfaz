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
                background: #3B81F6;
                color: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
                text-align: center;
                font-family: 'Arial', sans-serif;
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 10px;
            }
            .weather-item {
                display: flex;
                align-items: center;
                gap: 10px;
                background: #4C8BF5;
                padding: 10px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                color: white;
            }
            .news-container {
                margin-top: 20px;
                background: white;
                padding: 15px;
                border-radius: 8px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
                color: black;
                text-align: left;
            }
        </style>
    """, unsafe_allow_html=True)
    
    city, country, lat, lon = get_user_location()
    temp, forecast_max, forecast_min = get_weather(lat, lon)
    now = datetime.datetime.now()
    formatted_date = now.strftime("%A, %d %B %Y")
    formatted_time = now.strftime("%I:%M %p")
    
    # Detectar tamaño de pantalla
    is_mobile = st.query_params.get("device", ["desktop"])[0] == "mobile"
    
    st.markdown('<div class="weather-container">', unsafe_allow_html=True)
    st.markdown(f"<div class='weather-item'><span>📍</span> Ciudad: {city}, {country}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='weather-item'><span>📅</span> Fecha: {formatted_date}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='weather-item'><span>⏰</span> Hora Local: {formatted_time}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='weather-item'><span>🌡</span> Temperatura: {temp}°C</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='weather-item'><span>🔮</span> Previsión: Máx: {forecast_max}°C / Mín: {forecast_min}°C</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if not is_mobile:
        st.markdown("<h3 style='color: white; text-align: center;'>Vista de la ciudad</h3>", unsafe_allow_html=True)
        st.image(f"https://source.unsplash.com/600x400/?{city}", caption=f"Vista de {city}", use_container_width=True)
        
        st.markdown("<h3 style='color: white; text-align: center;'>Noticias recientes</h3>", unsafe_allow_html=True)
        news_url = f"https://news.google.com/search?q={city}&hl=es&gl=ES&ceid=ES:es"
        st.markdown(f"<a href='{news_url}' target='_blank' style='color: #FFD700; text-decoration: none;'>Ver noticias sobre {city}</a>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
