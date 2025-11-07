def calculate_recommended_price(data):
    # ---------------- INTERNAL FACTOR ----------------
    # Weighted average of current price and competitor prices
    competitor_avg = sum(data.competitor_prices) / len(data.competitor_prices)
    internal_score = (data.current_price * 0.4) + (competitor_avg * 0.6)

    # ---------------- EXTERNAL FACTORS ----------------
    weather_factor = 1.0
    reasons = []  # collect reasoning dynamically

    # Weather Logic
    temp = data.weather["temperature"]
    if temp > 30:
        weather_factor += 0.05   # +5% if hot
        reasons.append("Hot weather → higher demand (+5%)")
    elif temp < 20:
        weather_factor -= 0.03   # -3% if cold
        reasons.append("Cold weather → lower demand (-3%)")

    # Event Logic
    event_factor = 1.0
    if len(data.events) > 0:
        event_factor += 0.08  # +8% if event nearby
        reasons.append("Nearby event → increased customer footfall (+8%)")

    # If no external influences
    if not reasons:
        reasons.append("Normal conditions → no demand change")

    # ---------------- FINAL PRICE CALCULATION ----------------
    recommended_price = round(internal_score * weather_factor * event_factor, 2)

    # Weight Description (fixed for explanation — not hardcoded price)
    factors = {
        "internal_weight": 0.6,
        "external_weight": 0.4
    }

    # Convert reasoning list to readable text
    reasoning = "; ".join(reasons)

    return recommended_price, factors, reasoning
