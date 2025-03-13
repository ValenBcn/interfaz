import streamlit as st
import requests
import datetime

def get_user_location():
    try:
        ip_response = requests.get("https://ipapi.co/json/")
        ip_data = ip_response.json()
        city = ip_data.get("city", "Desconocido")
        return city
    except:
        return "Desconocido"

def get_weather(city):
    try:
        return "🌡️ 25°C ☀️ Despejado"  # Simulación
    except:
        return "No disponible"

def main():
    st.set_page_config(layout="wide")
    city = get_user_location()
    weather_info = get_weather(city)
    now = datetime.datetime.now()
    formatted_date = now.strftime("%d %b %Y")
    
    lang_options = {
        "🇪🇸 Español": "es", 
        "🇬🇧 English": "en", 
        "🇩🇪 Deutsch": "de", 
        "🇨🇦 Català": "ca", 
        "🇫🇷 Français": "fr"
    }
    
    if "selected_lang" not in st.session_state:
        st.session_state.selected_lang = "🇪🇸 Español"
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    if col1.button("🇪🇸 Español"):
        st.session_state.selected_lang = "🇪🇸 Español"
    if col2.button("🇬🇧 English"):
        st.session_state.selected_lang = "🇬🇧 English"
    if col3.button("🇩🇪 Deutsch"):
        st.session_state.selected_lang = "🇩🇪 Deutsch"
    if col4.button("🇨🇦 Català"):
        st.session_state.selected_lang = "🇨🇦 Català"
    if col5.button("🇫🇷 Français"):
        st.session_state.selected_lang = "🇫🇷 Français"
    
    lang = lang_options[st.session_state.selected_lang]
    
    messages = {
        "es": f"👋 Hola, hoy es {formatted_date}, el clima actual en 📍 {city} es {weather_info}.",
        "en": f"👋 Hello, today is {formatted_date}, the current weather in 📍 {city} is {weather_info}.",
        "de": f"👋 Hallo, heute ist {formatted_date}, das aktuelle Wetter in 📍 {city} beträgt {weather_info}.",
        "ca": f"👋 Hola, avui és {formatted_date}, el clima actual a 📍 {city} és {weather_info}.",
        "fr": f"👋 Bonjour, aujourd'hui c'est {formatted_date}, le temps actuel à 📍 {city} est {weather_info}."
    }
    
    with st.container():
        st.markdown(
            f"""
            <style>
                .stApp {{
                    background-color: white !important;
                }}
                .header-container {{
                    background-color: #3B81F6;
                    color: #f7f8ff;
                    text-align: center;
                    padding: 8px 15px;
                    border-radius: 8px;
                    font-size: 14px;
                    font-family: 'Arial', sans-serif;
                }}
            </style>
            <div class='header-container'>{messages[lang]}</div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
