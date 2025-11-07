# AI-Powered Menu Pricing System

## Project Structure
ai_pricing_system/
├── main.py                → API endpoint
├── pricing_logic.py       → Price calculation logic (AI model behavior)
├── database.py            → PostgreSQL connection settings
├── models.py              → Database table for storing pricing history
├── init_db.py             → Creates database tables
└── external_services/
      ├── weather_api.py   → Fetches weather data
      └── event_api.py     → Fetches event data

## Create .env File
Create a file named `.env` in the project folder and add:

WEATHER_API_KEY= YOUR API KEY
EVENT_API_KEY= YOUR API KEY
DATABASE_URL= ENTER YOUR DB DETAILS

## How to Run

1. Install dependencies:
   pip install -r requirements.txt

2. Create PostgreSQL database:
   CREATE DATABASE pricing_db;

3. Update database credentials in database.py:
   DATABASE_URL = "postgresql://postgres:YOUR_PASSWORD@localhost:5432/pricing_db"

4. Create tables:
   python init_db.py

5. Start the API:
   uvicorn main:app --reload

6. Open Swagger UI to test the API:
   http://localhost:8000/docs


## Example Request (Automatic Mode Using City)
{
  "menu_item_id": 101,
  "current_price": 250,
  "competitor_prices": [240, 260, 245],
  "city": "Chennai"
}

## Example Request (Manual Mode)
{
  "menu_item_id": 123,
  "current_price": 250,
  "competitor_prices": [240, 260, 245],
  "weather": { "temperature": 32, "condition": "Sunny" },
  "events": [
    { "name": "Food Festival", "popularity": "High", "distance_km": 2.5 }
  ]
}

## Example Response
{
  "menu_item_id": 101,
  "recommended_price": 272.55,
  "factors": {
    "internal_weight": 0.6,
    "external_weight": 0.4
  },
  "reasoning": "Warm weather and nearby event increased demand."
}
