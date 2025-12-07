# multi_tool_agent/agent.py
import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
import requests
import pprint


# --- Tool: get weather (demo) ---
def get_weather(city: str) -> dict:
    """
    Fetches the current weather for any city using free, keyless APIs.

    This function first uses the Nominatim API to get the latitude and longitude
    for the given city. It then uses these coordinates to query the Open-Meteo
    API for the current weather conditions.

    Args:
        city: The name of the city (e.g., "London", "Tokyo").

    Returns:
        A dictionary containing the status and the weather report, or an error message.
        Example success: {'status': 'success', 'report': 'The weather in Berlin is Overcast with a temperature of 15.2°C.'}
        Example error:   {'status': 'error', 'error_message': "Could not find location: 'Nowhereville'"}
    """
    # Step 1: Geocode the city name to get latitude and longitude using Nominatim
    geocoding_url = "https://nominatim.openstreetmap.org/search"
    geocoding_params = {
        "q": city,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "WeatherApp/1.0 (your-email@example.com)" # Good practice to set a User-Agent
    }

    try:
        geo_response = requests.get(geocoding_url, params=geocoding_params, headers=headers)
        geo_response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        location_data = geo_response.json()

        if not location_data:
            return {"status": "error", "error_message": f"Could not find location: '{city}'"}

        lat = location_data[0]["lat"]
        lon = location_data[0]["lon"]
        display_name = location_data[0]["display_name"]

    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": f"Geocoding API request failed: {e}"}


    # Step 2: Get the weather using the coordinates from Open-Meteo
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": "true"
    }

    try:
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        if "current_weather" not in weather_data:
             return {"status": "error", "error_message": "Could not retrieve current weather data."}

        current_weather = weather_data["current_weather"]
        temperature = current_weather["temperature"]
        weather_code = current_weather["weathercode"]
        weather_description = interpret_weather_code(weather_code)

        # Format the final report
        report_string = (
            f"The weather in {display_name.split(',')[0]} is {weather_description} "
            f"with a temperature of {temperature}°C."
        )

        return {
            "status": "success",
            "report": report_string
        }

    except requests.exceptions.RequestException as e:
        return {"status": "error", "error_message": f"Weather API request failed: {e}"}

def interpret_weather_code(code: int) -> str:
    """Converts WMO weather code to a human-readable string."""
    codes = {
        0: "Clear sky",
        1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Fog", 48: "Depositing rime fog",
        51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
        56: "Light freezing drizzle", 57: "Dense freezing drizzle",
        61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
        66: "Light freezing rain", 67: "Heavy freezing rain",
        71: "Slight snow fall", 73: "Moderate snow fall", 75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
        85: "Slight snow showers", 86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail", 99: "Thunderstorm with heavy hail"
    }
    return codes.get(code, "Unknown weather condition")

# --- Tool: get current time in a city (demo) ---
def get_current_time(city: str) -> dict:
    """Return current time for a small demo set of cities."""
    print("get current time function is being runnnnnnn")
    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    elif city.lower() == "kolkata" or city.lower() == "kolkata, india":
        tz_identifier = "Asia/Kolkata"
    else:
        return {"status": "error", "error_message": f"Timezone for '{city}' unknown."}

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = f"The current time in {city} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
    return {"status": "success", "report": report}


# --- Root agent: pass plain functions directly into tools list ---
# Replace "replace-me-with-model-id" with your model id if required by your provider.
root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.5-flash",   # e.g. "gemini-2.0-flash" or other model id you have access to
    description="Agent to answer simple questions about time and weather in a city.",
    instruction="You are a helpful agent who can answer user questions about the time and weather in a city.",
    tools=[get_weather, get_current_time],
)





# def get_weather(city: str) -> dict:
#     """
#     Demo tool: returns a weather of a city .
#     Return shape: {"status": "success", "report": "..."} or error dict.
#     """
#     print("Get weather function is being runnnnnnn")
#     if city.lower() == "new york":
#         return {
#             "status": "success",
#             "report": (
#                 "The weather in New York is sunny with a temperature of 25 degrees "
#                 "Celsius (77 degrees Fahrenheit)."
#             ),
#         }
#     return {"status": "error", "error_message": f"Weather for '{city}' not available."}