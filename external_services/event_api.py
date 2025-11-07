import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EVENT_API_KEY")

if not API_KEY:
    raise ValueError("EVENT_API_KEY not found in environment variables")

def get_events(city):
    """
    Fetch event data from Ticketmaster for a given city.
    Returns a simplified list of events containing name, popularity, and distance.
    """

    url = f"https://app.ticketmaster.com/discovery/v2/events.json?city={city}&apikey={API_KEY}"
    response = requests.get(url).json()

    events_list = []

    if "_embedded" in response and "events" in response["_embedded"]:
        for event in response["_embedded"]["events"]:
            events_list.append({
                "name": event.get("name", "Unknown Event"),
                "popularity": event.get("promoter", {}).get("name", "Medium"),
                "distance_km": 2.0  
            })

    return events_list
