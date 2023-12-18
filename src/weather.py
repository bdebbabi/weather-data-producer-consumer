import json
import urllib.parse
import urllib.request

import geocoder


def get_current_coordinates() -> [int, int]:
    """Returns current gps coordiantes

    Returns:
        [int, int]: list containing latitude and longitude
    """
    return geocoder.ip("me").latlng


def get_weather_data(lat: float, long: float, api_key: str) -> dict:
    """Returns current weather data from a specific location

    Args:
        lat (float): Latitude to get the data for
        long (float): Longitude to get the data for
        api_key (str): openweathermap api key

    Returns:
        dict: weather data
    """
    service_url = "http://api.openweathermap.org/data/2.5/weather?"
    url = service_url + urllib.parse.urlencode(
        {"lat": lat, "lon": long, "APPID": api_key, "units": "metric"}
    )
    url_read = json.loads(urllib.request.urlopen(url).read().decode())

    return url_read
