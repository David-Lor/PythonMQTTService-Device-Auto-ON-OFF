"""Main Service to be started and executed"""

# # Installed # #
import paho.mqtt.client as mqtt

# # Package # #
from .settings import settings
from .service_processing import on_message, on_connect
from .service_scheduler import schedule_turn_on, schedule_turn_off
from .helpers import *

__all__ = ("main",)


def main():
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_disconnect = lambda *args: print("MQTT Disconnected!")
    client.on_message = on_message

    client.connect(settings.broker, settings.port)

    schedule_turn_off(client=client, when=hour_str_to_when_dict(settings.off_hour))
    schedule_turn_on(client=client, when=hour_str_to_when_dict(settings.on_hour))

    client.loop_forever()


if __name__ == '__main__':
    main()
