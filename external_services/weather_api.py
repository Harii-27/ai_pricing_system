import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WEATHER_API_KEY")

if not API_KEY:
    raise ValueError("WEATHER_API_KEY not found in environment variables")

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    if "main" not in response:
        raise Exception(f"Weather API Error: {response.get('message', 'Unknown error')}")

    return {
        "temperature": response["main"]["temp"],
        "condition": response["weather"][0]["main"]
    }
