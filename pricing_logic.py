def calculate_recommended_price(data):
    current_price = data.current_price
    competitor_avg = sum(data.competitor_prices) / len(data.competitor_prices)

    internal_weight = 0.6
    external_weight = 0.4

    base_price = (current_price * internal_weight) + (competitor_avg * external_weight)

    adjustment_details = []

    # WEATHER LOGIC
    temperature = data.weather.temperature
    if temperature > 30:
        base_price *= 1.05
        adjustment_details.append("Hot weather → demand increases (+5%)")
    elif temperature < 20:
        base_price *= 0.95
        adjustment_details.append("Cold weather → demand decreases (-5%)")
    else:
        adjustment_details.append("Normal weather → no change")

    # EVENT LOGIC
    if data.events:
        for event in data.events:
            if event.popularity.lower() == "high":
                base_price *= 1.10
                adjustment_details.append(f"Event '{event.name}' high popularity (+10%)")
            elif event.popularity.lower() == "medium":
                base_price *= 1.05
                adjustment_details.append(f"Event '{event.name}' medium popularity (+5%)")

            if event.distance_km <= 3:
                base_price *= 1.05
                adjustment_details.append(f"Event is nearby ({event.distance_km} km) (+5%)")

    recommended_price = round(base_price, 2)

    reasoning = " | ".join(adjustment_details)

    factors = {
        "internal_weight": internal_weight,
        "external_weight": external_weight
    }

    return recommended_price, factors, reasoning
