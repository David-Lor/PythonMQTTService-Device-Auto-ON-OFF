"""Process incoming MQTT messages and other MQTT actions (callback definition).
"""

# # Installed # #
import paho.mqtt.client as mqtt

# # Package # #
from .settings import settings
from .actions import enable_auto, disable_auto

__all__ = ("on_message", "on_connect")


def on_message(*args):
    message = next(a for a in args if isinstance(a, mqtt.MQTTMessage))
    topic = message.topic
    payload = message.payload.decode().strip()
    print(f"Rx @ {topic}: {payload}")

    if topic == settings.set_auto_topic:
        if payload == settings.set_auto_disable_payload:
            disable_auto()
        elif payload == settings.set_auto_enable_payload:
            enable_auto()


def on_connect(*args):
    client = next(a for a in args if isinstance(a, mqtt.Client))
    client.subscribe(settings.set_auto_topic)
    print("MQTT Connected!")
