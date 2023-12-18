import os
from datetime import datetime

import dotenv

from logger import logging
from mqtt import mqtt_producer
from weather import get_current_coordinates, get_weather_data

dotenv.load_dotenv()

host = os.getenv("host", "localhost")
api_key = os.getenv("API_KEY")
frequency = int(os.getenv("FREQUENCY", 60))
lat = os.getenv("LAT", None)
long = os.getenv("LONG", None)
username = os.getenv("MOSQUITTO_USERNAME", "admin")
password = os.getenv("MOSQUITTO_PASSWORD", None)

# get current coordiantes if not in env variables
if not (lat and long):
    logging.warning(
        f"Coordinates missing from env variables. Getting current position coordiantes."
    )
    lat, long = get_current_coordinates()


def message() -> str:
    """Returns weather data for a specific location

    Returns:
        str: comma separated weather data values
    """

    weather_data = get_weather_data(lat, long, api_key)

    weather = weather_data["weather"][0]["main"]
    rain = weather_data.get("rain", {}).get("1h", "")
    temp = weather_data["main"]["temp"]
    wind = weather_data["wind"]["speed"]
    humidity = weather_data["main"]["humidity"]
    station = weather_data["name"]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return f"{weather},{rain},{temp},{wind},{humidity},{station},{timestamp}"


# create an mqtt producer and connect to it
producer = mqtt_producer("producer", host, username, password)

# send weather data on the weather topic every minute
logging.info(f"Weather data will be collected for: {lat}, {long}")
producer.publish(topic="/weather", message=message, frequency=frequency)
