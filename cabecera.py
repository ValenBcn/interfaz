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

    # Definir idiomas
    lang_options = {
        "🇪🇸 Español": "es",
        "🇬🇧 English": "en",
        "🇩🇪 Deutsch": "de",
        "🇨🇦 Català": "ca",
        "🇫🇷 Français": "fr"
    }

    # Inicializar idioma en session_state
    if "selected_lang" not in st.session_state:
        st.session_state.selected_lang = "es"  # Español por defecto

    selected_lang = st.session_state.selected_lang

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
            f"""<a class="lang-button {'selected' if lang_code == selected_lang else ''}">
                 {flag} 
                 </a>"""
            for flag, lang_code in lang_options.items()
        ) + "</div>",
        unsafe_allow_html=True
    )

    # Generar botones para seleccionar idioma
    cols = st.columns(len(lang_options))
    for i, (label, lang_code) in enumerate(lang_options.items()):
        if cols[i].button(label, key=f"btn_{lang_code}"):
            st.session_state.selected_lang = lang_code
            st.rerun()  # Recargar la interfaz sin abrir otra página

    # Obtener el idioma seleccionado
    lang = st.session_state.selected_lang

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
            <div class='header-container'>{messages[lang]}</div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    main()
