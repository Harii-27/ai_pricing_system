AI-Powered Menu Pricing System

This project provides a dynamic price recommendation API for restaurant menu items.
Prices are calculated using internal factors (current + competitor prices) and external factors (weather & nearby events).

Objective

Recommend the best selling price for a menu item by predicting demand based on real-world conditions.

Core Logic (AI / ML Approach)
Factor Type	Data Used	Impact
Internal	Current price + Competitor prices	Forms base price (weighted average)
External	Weather + Nearby Events	Adjusts demand (increases or decreases price)

Pricing Formula

Final Price = (0.4 * Current Price + 0.6 * Competitor Average)
              * Weather Adjustment
              * Event Adjustment


Dynamic reasoning is generated to explain why the price changed.

Tech Stack
Component	Choice
API Framework	FastAPI (with Swagger UI)
Weather Source	OpenWeatherMap API
Events Source	Ticketmaster API
Pricing Logic	Weighted AI Model
Database (Optional)	PostgreSQL / Supabase
Project Structure
ai_pricing_system/
│
├── main.py                      # API endpoint
├── pricing_logic.py             # AI pricing logic
├── database.py                  # DB connection (optional)
├── models.py                    # DB tables (optional)
│
└── external_services/
       ├── weather_api.py        # Weather data fetch
       └── event_api.py          # Events data fetch

How to Run
pip install -r requirements.txt
uvicorn main:app --reload


Open Swagger UI:

http://localhost:8000/docs

Example Request
{
  "menu_item_id": 101,
  "current_price": 250,
  "competitor_prices": [240, 260, 245],
  "city": "Chennai"
}

Example Response
{
  "menu_item_id": 101,
  "recommended_price": 272.55,
  "factors": {
    "internal_weight": 0.6,
    "external_weight": 0.4
  },
  "reasoning": "Hot weather → higher demand (+5%); Nearby event → increased customer footfall (+8%)"
}