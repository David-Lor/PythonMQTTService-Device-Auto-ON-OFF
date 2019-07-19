
# # Native # #
import datetime
from collections import deque
from threading import Event

# # Installed # #
# noinspection PyPackageRequirements
import pytest
import paho.mqtt.client as mqtt

# # Package # #
from iot_service_dev_auto_on_off.settings import settings
from iot_service_dev_auto_on_off.service_scheduler import schedule_turn_on, schedule_turn_off, scheduler
from iot_service_dev_auto_on_off.service_processing import on_message as service_on_message_callback
from iot_service_dev_auto_on_off.helpers import hour_str_to_when_dict

_received_messages = deque()
_received_one_message_event = Event()
_received_two_messages_event = Event()


class TestTimer:
    _client = mqtt.Client()

    def setup_class(self):
        """Setup before all the tests must initialize a MQTT client and subscribe to the OFF/ON command topics.
        """
        self._client.on_message = self._on_message
        self._client.connect(settings.broker, settings.port)
        self._client.subscribe(settings.off_topic)
        self._client.subscribe(settings.on_topic)
        self._client.subscribe(settings.set_auto_topic)
        self._client.loop_start()

    def teardown_class(self):
        """Teardown after all the tests must disconnect the MQTT client.
        """
        self._client.loop_stop(force=True)
        self._client.disconnect()

    @staticmethod
    def teardown_method():
        """Teardown after each test method must clear all lists and events.
        """
        _received_two_messages_event.clear()
        _received_one_message_event.clear()
        _received_messages.clear()
        scheduler.remove_all_jobs()

    @staticmethod
    def _on_message(*args):
        """Callback to be executed when a message is received on the MQTT client created for this test.
        """
        message = next(a for a in args if isinstance(a, mqtt.MQTTMessage))
        print(f"RX (Test) @ {message.topic}: {message.payload.decode()}")

        if message.topic in (settings.on_topic, settings.off_topic):
            _received_messages.append((message, datetime.datetime.now()))
            _received_one_message_event.set()
            if len(_received_messages) == 2:
                _received_two_messages_event.set()

        service_on_message_callback(*args)

    @staticmethod
    def _get_on_off_hours():
        """Generate two hours to send the OFF and ON commands, based on the current datetime."""
        off = (datetime.datetime.now() + datetime.timedelta(seconds=3))
        on = (off + datetime.timedelta(seconds=1)).strftime("%H:%M:%S")
        off = off.strftime("%H:%M:%S")
        return off, on

    # noinspection PyUnusedLocal
    def test_timer_on_off(self):
        """Test that the timer is set and the ON/OFF messages are properly sent over MQTT.
        """
        off_hour, on_hour = self._get_on_off_hours()

        schedule_turn_off(
            client=self._client,
            when=hour_str_to_when_dict(off_hour)
        )
        schedule_turn_on(
            client=self._client,
            when=hour_str_to_when_dict(on_hour)
        )

        assert _received_two_messages_event.wait(timeout=6)

        off_message, off_datetime = next(
            m for m in _received_messages if m[0].payload.decode() == settings.off_payload
        )
        on_message, on_datetime = next(
            m for m in _received_messages if m[0].payload.decode() == settings.on_payload
        )
        # assert off_datetime.strftime("%H:%M:%S") == off_hour
        # assert on_datetime.strftime("%H:%M:%S") == on_hour

    # noinspection PyUnusedLocal
    def test_timer_disabled(self):
        """Test that no OFF message is sent when the timer is temporary disabled.
        The ON message is expected to be sent.
        """
        self._client.publish(settings.set_auto_topic, settings.set_auto_disable_payload)

        off_hour, on_hour = self._get_on_off_hours()

        schedule_turn_off(
            client=self._client,
            when=hour_str_to_when_dict(off_hour)
        )
        schedule_turn_on(
            client=self._client,
            when=hour_str_to_when_dict(on_hour)
        )

        assert _received_one_message_event.wait(timeout=4)

        on_message, on_datetime = next(
            m for m in _received_messages if m[0].payload.decode() == settings.on_payload
        )
        with pytest.raises(StopIteration):
            off_message, off_datetime = next(
                m for m in _received_messages if m[0].payload.decode() == settings.off_payload
            )

    # noinspection PyUnusedLocal
    def test_timer_disabled_reenabled(self):
        """Test that the timer is set and the ON/OFF messages are properly sent over MQTT,
        after switching OFF and back to ON the timer.
        """
        self._client.publish(settings.set_auto_topic, settings.set_auto_disable_payload)
        self._client.publish(settings.set_auto_topic, settings.set_auto_enable_payload)

        off_hour, on_hour = self._get_on_off_hours()

        schedule_turn_off(
            client=self._client,
            when=hour_str_to_when_dict(off_hour)
        )
        schedule_turn_on(
            client=self._client,
            when=hour_str_to_when_dict(on_hour)
        )

        assert _received_two_messages_event.wait(timeout=6)

        off_message, off_datetime = next(
            m for m in _received_messages if m[0].payload.decode() == settings.off_payload
        )
        on_message, on_datetime = next(
            m for m in _received_messages if m[0].payload.decode() == settings.on_payload
        )
