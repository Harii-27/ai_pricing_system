from external_services.ai_pricing import get_ai_price_recommendation


def calculate_recommended_price(data):
    current_price = data.current_price
    competitor_avg = sum(data.competitor_prices) / len(data.competitor_prices)
    temperature = data.weather.temperature if data.weather else 25.0
    condition = data.weather.condition if data.weather else "Normal"
    events = data.events or []
    
    recommended_price, reasoning, factors = get_ai_price_recommendation(
        current_price, competitor_avg, temperature, condition, events
    )
    
    recommended_price = round(max(recommended_price, 0), 2)
    
    return recommended_price, factors, reasoning
