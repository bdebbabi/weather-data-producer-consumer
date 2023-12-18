import os
from pathlib import Path

import dotenv

from mqtt import mqtt_consumer

dotenv.load_dotenv()

host = os.getenv("host", "localhost")
username = os.getenv("MOSQUITTO_USERNAME", "admin")
password = os.getenv("MOSQUITTO_PASSWORD", None)


def on_message(msg: str) -> None:
    """Writes received messages in a csv file

    Args:
        msg (str): message to write
    """
    filepath = Path("./opt/output/weather.csv")

    if not filepath.is_file():
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as file:
            file.write("weather,rain,temp,wind,humidity,station,timestamp\n")

    with open(filepath, "a") as file:
        file.write(f"{msg}\n")


# create an mqtt consumer and connect to it
consumer = mqtt_consumer("consumer", host, username, password)

# subscribe to the weather topic and save each message in a csv file
consumer.receive(topic="/weather", on_message=on_message)
