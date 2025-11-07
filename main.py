from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from types import SimpleNamespace

from pricing_logic import calculate_recommended_price
from external_services.weather_api import get_weather
from external_services.event_api import get_events
from database import get_db
from models import PriceHistory


app = FastAPI(
    title="AI Menu Pricing API",
    description="Recommends menu prices based on internal & external factors"
)


# ----------- Request Body Model -----------

class PriceRequest(BaseModel):
    menu_item_id: int
    current_price: float
    competitor_prices: list[float]
    city: str   # ✅ We only ask for city, not weather or events manually


# ----------- API Endpoint -----------

@app.post("/api/pricing/suggest")
def suggest_price(data: PriceRequest, db: Session = Depends(get_db)):

    # ✅ Fetch external data automatically
    weather_data = get_weather(data.city)
    event_data = get_events(data.city)

    # ✅ Format data for pricing logic
    simple_data = {
        "menu_item_id": data.menu_item_id,
        "current_price": data.current_price,
        "competitor_prices": data.competitor_prices,
        "weather": weather_data,
        "events": event_data
    }

    recommended_price, factors, reasoning = calculate_recommended_price(
        SimpleNamespace(**simple_data)
    )

    # ✅ Save the result in PostgreSQL
    record = PriceHistory(
        menu_item_id=data.menu_item_id,
        recommended_price=recommended_price,
        reasoning=reasoning
    )
    db.add(record)
    db.commit()

    # ✅ Response
    return {
        "menu_item_id": data.menu_item_id,
        "recommended_price": recommended_price,
        "factors": factors,
        "reasoning": reasoning
    }
