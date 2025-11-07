import requests

API_KEY = "oJ7OFAFv62FsClDLwGnGyLSFkahMZsLm"
def get_events(city):
    """
    Fetch event data from Ticketmaster for a given city.
    Returns a simplified list of events containing name, popularity, and distance.
    """

    url = f"https://app.ticketmaster.com/discovery/v2/events.json?city={city}&apikey={API_KEY}"
    response = requests.get(url).json()

    events_list = []

    # Ticketmaster returns events under _embedded → events[]
    if "_embedded" in response and "events" in response["_embedded"]:
        for event in response["_embedded"]["events"]:
            events_list.append({
                "name": event.get("name", "Unknown Event"),
                "popularity": event.get("promoter", {}).get("name", "Medium"),
                # We keep distance simple (or you can calculate using lat/long later)
                "distance_km": 2.0  
            })

    return events_list
