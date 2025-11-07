from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import Optional, List
from pricing_logic import calculate_recommended_price
from sqlalchemy.orm import Session
from database import get_db
from models import PriceHistory
from external_services.weather_api import get_weather
from external_services.event_api import get_events
from types import SimpleNamespace

app = FastAPI(title="AI Menu Pricing API", description="Recommends menu prices based on internal & external factors")


class Weather(BaseModel):
    temperature: float
    condition: str

class Event(BaseModel):
    name: str
    popularity: str
    distance_km: float

class PriceRequest(BaseModel):
    menu_item_id: int
    current_price: float
    competitor_prices: List[float]
    city: Optional[str] = None              
    weather: Optional[Weather] = None       
    events: Optional[List[Event]] = None    


def convert(obj):
    if isinstance(obj, dict):
        return SimpleNamespace(**{k: convert(v) for k, v in obj.items()})
    if isinstance(obj, list):
        return [convert(i) for i in obj]
    return obj


# API Endpoint 
@app.post("/api/pricing/suggest")
def suggest_price(data: PriceRequest, db: Session = Depends(get_db)):
    
    if data.city:
        weather_data = get_weather(data.city)
        event_data = get_events(data.city)

    else:
        weather_data = data.weather
        event_data = data.events

    formatted = SimpleNamespace(
        menu_item_id=data.menu_item_id,
        current_price=data.current_price,
        competitor_prices=data.competitor_prices,
        weather=convert(weather_data),
        events=convert(event_data)
    )

    recommended_price, factors, reasoning = calculate_recommended_price(formatted)

    history = PriceHistory(
        menu_item_id=data.menu_item_id,
        recommended_price=recommended_price,
        reasoning=reasoning
    )
    db.add(history)
    db.commit()
    db.refresh(history)

    return {
        "menu_item_id": data.menu_item_id,
        "recommended_price": recommended_price,
        "factors": factors,
        "reasoning": reasoning
    }
