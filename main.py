import requests
import ollama
import json

MODEL = "qwen3:8b"

SYSTEM_PROMPT = """
You are a helpful weather assistant.
Use the get_weather tool for current weather questions.
Never invent weather data or city names.
If the user does not specify a city, ask for clarification.
Explain results clearly and concisely.
"""

def get_weather(city: str) -> dict:
    """Get the current weather for a city."""

    if not isinstance(city, str) or not city.strip():
        return {"error": "Please provide a valid city name."}

    city = city.strip()

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    geo_response = requests.get(
        geo_url,
        params=geo_params,
        timeout=10
    )

    geo_response.raise_for_status()
    geo_data = geo_response.json()

    if not geo_data.get("results"):
        return {"error": f"City not found: {city}"}

    location = geo_data["results"][0]
    latitude = location["latitude"]
    longitude = location["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
        "timezone": "auto"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params,
        timeout=10
    )

    weather_response.raise_for_status()

    current = weather_response.json()["current"]

    return {
        "city": location["name"],
        "country": location.get("country", "Unknown"),
        "temperature_°C": current["temperature_2m"],
        "feels_like_°C": current["apparent_temperature"],
        "humidity_percentage_%": current["relative_humidity_2m"],
        "wind_speed_km/h": current["wind_speed_10m"],
        "precipitation_mm": current["precipitation"],
        "weather_code": current["weather_code"]
    }

tools = [get_weather]

messages = [
    {
        "role": "system",
        "content": SYSTEM_PROMPT
    }
]

def run_agent(user_input: str):
    messages.append({
        "role": "user",
        "content": user_input
    })

    for _ in range(5):
        response = ollama.chat(
            model=MODEL,
            messages=messages,
            tools=tools
        )

        messages.append(response.message)

        if not response.message.tool_calls:
            return response.message.content

        for tool_call in response.message.tool_calls:
            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments or {}

            if tool_name != "get_weather":
                result = {"error": "Unsupported tool."}

            elif not isinstance(arguments, dict):
                result = {"error": "Invalid tool arguments."}

            else:
                city = arguments.get("city")

                if not isinstance(city, str) or not city.strip():
                    result = {"error": "Please provide a valid city name."}
                else:
                    try:
                        result = get_weather(city)
                    except (requests.RequestException, KeyError, ValueError) as error:
                        print(f"Weather tool error: {error}")
                        result = {"error": "Weather data is temporarily unavailable."}

            messages.append({
                "role": "tool",
                "name": tool_name,
                "content": json.dumps(result)
            })
            
    return "I couldn't complete request. Please try again."

if __name__ == "__main__":
    print("Weather AI agent ready! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ("exit", "quit"):
            break

        if not user_input:
            continue

        try:
            answer = run_agent(user_input)
            print(f"\nAssistant: {answer}\n")
        except Exception as error:
            print(f"\nError: {error}\n")
