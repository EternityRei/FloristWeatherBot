import os
import requests

from langchain.tools import tool


@tool
def current_weather(city: str):
    """
    Used to find weather details based on provided city.
    """

    api_key = os.environ.get('WEATHER_API_KEY')

    lat, lon = get_geolocation(api_key, city)

    url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        c_temp = __convert_k_into_c(data['main'])
        data['main']['temp'] = c_temp
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


def __convert_k_into_c(main_data: dict):
    temp = main_data['temp']
    return temp - 273.15
