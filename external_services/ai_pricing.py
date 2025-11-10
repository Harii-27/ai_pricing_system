import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_ai_price_recommendation(current_price, competitor_avg, temperature, condition, events):
    
    data = f"Price: ₹{current_price}, Competitors: ₹{competitor_avg:.2f}, Temp: {temperature}°C ({condition})"
    if events:
        data += f", Events: {len(events)}"
    
    prompt = f"Recommend restaurant menu price. {data}. Return JSON: {{\"recommended_price\": number, \"reasoning\": \"text\", \"factors\": {{\"internal_weight\": 0.6, \"external_weight\": 0.4}}}}"
    
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "user", "content": prompt}]
    )
    
    content = response.choices[0].message.content.strip()
    content = content.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    result = json.loads(content)
    
    return float(result["recommended_price"]), result.get("reasoning", ""), result.get("factors", {})

