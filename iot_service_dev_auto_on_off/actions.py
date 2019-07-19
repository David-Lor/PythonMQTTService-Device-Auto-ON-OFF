"""Callbacks with the actions to execute at each event (ON and OFF).
"""

# # Native # #
from threading import Event

# # Installed # #
from paho.mqtt.client import Client

# # Package # #
from .settings import settings

__all__ = ("turn_on", "turn_off", "disable_auto", "enable_auto", "auto_disabled")

disable_auto_event = Event()
"""Event to be set whenever the Turn OFF action wants to be disabled.
Event is cleared when the action would perform."""


def disable_auto():
    print("Auto Disabled")
    disable_auto_event.set()


def enable_auto():
    print("Auto Enabled")
    disable_auto_event.clear()


def auto_disabled():
    return disable_auto_event.is_set()


def turn_on(client: Client):
    """Action executed when the device must be Turn ON."""
    client.publish(settings.on_topic, settings.on_payload)
    print("Tx ON: Requested device to turn ON/WakeUp")


def turn_off(client: Client):
    """Action executed when the device must be Turn OFF."""
    if auto_disabled():
        enable_auto()
        print("OFF action skipped")
    else:
        client.publish(settings.off_topic, settings.off_payload)
        print("Tx OFF: Requested device to turn OFF/Sleep")
