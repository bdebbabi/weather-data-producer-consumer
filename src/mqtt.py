import time
from abc import ABC
from dataclasses import dataclass
from typing import Callable

import paho.mqtt.client as paho_mqtt

from logger import logging


@dataclass
class mqtt(ABC):
    """Creates an mqtt client and connects to it

    Args:
        name (str): client id used when connecting to the broker.
        host (str): Hostname of the remote broker.
        username (str): The username to authenticate with. Default to `admin`.
        password (str|None): The password to authenticate with. Defaults to None.
        port (int): Port of the server host to connect to. Defaults to 1883.
        keepalive (int): Maximum period in seconds between communications with the broker. Defaults to 60.
    """

    name: str
    host: str
    username: str = "admin"
    password: str | None = None
    port: int = 1883
    keepalive: int = 60

    def __post_init__(self):
        self.client = paho_mqtt.Client(self.name)
        if self.username and self.password:
            self.client.username_pw_set(
                self.username,
                self.password,
            )
        self.client.on_connect = (
            lambda client, userdata, flags, rc: logging.info(f"Connected to the broker")
            if rc == 0
            else logging.error(
                f"Error while connecting to the broker. Error code: {rc}"
            )
        )
        self.client.connect(self.host, self.port, self.keepalive)


@dataclass
class mqtt_producer(mqtt):
    def publish(
        self, topic: str, message: Callable[[], str], frequency: int = 10
    ) -> None:
        """Publishes a message on a topic

        Args:
            topic (str): The topic that the message should be published on.
            message (Callable[[], str]): A function that returns the actual message to send.
            frequency (int, optional): Seconds between 2 consecutive messages. Defaults to 10.
        """
        self.client.on_publish = lambda client, userdata, result: logging.info(
            f"Message published on {topic}"
        )
        self.client.loop_start()
        while True:
            self.client.publish(topic, message())
            time.sleep(frequency)


@dataclass
class mqtt_consumer(mqtt):
    def receive(
        self,
        topic: str,
        on_message: Callable[[str], None],
    ) -> None:
        """Subscribes to a topic and performs an action on each message

        Args:
            topic (str): Topic to subscribe to
            on_message (Callable[[str], None]): Function that performs an action on the received message
        """
        self.client.subscribe(topic)

        def on_complete_message(client, userdata, msg):
            logging.info(f"Message received on {topic}")
            on_message(msg.payload.decode())

        self.client.on_message = on_complete_message
        self.client.loop_forever()
