import requests

API_KEY = "5e9b67830d60ad916e46f8cdd004adc"

def get_weather(city):
    """
    Fetch weather data from OpenWeatherMap API.
    Returns temperature (°C) and condition text.
    """

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    return {
        "temperature": response["main"]["temp"],
        "condition": response["weather"][0]["main"]
    }
