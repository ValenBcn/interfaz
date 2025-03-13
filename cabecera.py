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

    # Definición de idiomas
    lang_options = {
        "🇪🇸 Español": "es",
        "🇬🇧 English": "en",
        "🇩🇪 Deutsch": "de",
        "🇨🇦 Català": "ca",
        "🇫🇷 Français": "fr"
    }

    # Obtener el idioma de los parámetros de la URL
    query_params = st.query_params
    if "lang" in query_params:
        selected_lang = query_params["lang"]
    else:
        selected_lang = "es"  # Español por defecto

    # Guardar el idioma en la sesión de Streamlit
    st.session_state.selected_lang = selected_lang

    # CSS para los botones
    st.markdown(
        f"""
        <style>
            .lang-buttons {{
                display: flex;
                justify-content: center;
                gap: 10px;
                margin-bottom: 10px;
            }}
            .lang-button {{
                background-color: white;
                color: black;
                border: none;
                padding: 8px 12px;
                font-size: 14px;
                cursor: pointer;
                border-radius: 5px;
                transition: background 0.3s;
            }}
            .lang-button:hover {{
                background-color: #f0f0f0;
            }}
            .selected {{
                background-color: #3B81F6 !important;
                color: white !important;
            }}
        </style>
        <div class="lang-buttons">
        """ + "".join(
            f"""<a href="?lang={lang_code}" class="lang-button {'selected' if lang_code == selected_lang else ''}">
                 {flag} 
                 </a>"""
            for flag, lang_code in lang_options.items()
        ) + "</div>",
        unsafe_allow_html=True
    )

    # Mensajes en cada idioma
    messages = {
        "es": f"👋 Hola, hoy es {formatted_date}, el clima actual en 📍 {city} es {weather_info}.",
        "en": f"👋 Hello, today is {formatted_date}, the current weather in 📍 {city} is {weather_info}.",
        "de": f"👋 Hallo, heute ist {formatted_date}, das aktuelle Wetter in 📍 {city} beträgt {weather_info}.",
        "ca": f"👋 Hola, avui és {formatted_date}, el clima actual a 📍 {city} és {weather_info}.",
        "fr": f"👋 Bonjour, aujourd'hui c'est {formatted_date}, le temps actuel à 📍 {city} est {weather_info}."
    }

    # Renderizar el mensaje seleccionado
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
            <div class='header-container'>{messages[selected_lang]}</div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
