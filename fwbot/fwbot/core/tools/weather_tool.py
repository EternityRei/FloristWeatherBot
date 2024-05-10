import os
import requests

from langchain.tools import tool


@tool
def current_weather_by_city(
        city: str
):
    """
    Used to find weather details based on provided city.
    """

    api_key = os.environ.get('WEATHER_API_KEY')
    lat, lon = get_geolocation(api_key, city)

    return get_weather(lat, lon)


@tool
def current_weather_by_coordinates(
        lat: str,
        lon: str
):
    """
    Used to find weather details based on provided latitude and longitude.
    """

    return get_weather(lat, lon)


def get_weather(lat: str, lon: str):
    api_key = os.environ.get('WEATHER_API_KEY')
    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
    else:
        return f"Error: {response.status_code}"
    return data


def get_geolocation(api_key: str, city: str):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if data:
            lat = data[0]['lat']
            lon = data[0]['lon']
            return lat, lon
        else:
            return "No data found for the specified city."
    else:
        return f"Error: {response.status_code}"
