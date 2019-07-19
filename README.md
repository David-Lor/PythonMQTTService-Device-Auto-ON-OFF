# Python+MQTT Service: Auto Turn ON/OFF Device

Service to automatically turn OFF/Sleep and ON/WakeUp a device at given times, using MQTT messages.

This is a POC of a original implementation in Node-RED, now implemented as a coded Python service. 
It is intended to turn OFF (Sleep) my server at night (I know, servers should be 24/7 UP, but mine does nothing at night), 
and turn it ON (Wake Up) again at day.

Notice that the requirements are pretty simple and the implementation a bit too overkill. In this case, Node-RED might be a better choice... or as a middle-way, something Bash & Cron - powered.

## Features/Changelog

- 0.0.1
  - **Features**
    - Single OFF and ON time rules, executed all days at a certain time (HH:MM:SS Cron-like)
    - OFF/ON actions are sent as MQTT commands
    - The OFF;ON action can be single-disabled by sending a message to a certain topic (must be sent BEFORE the OFF/Sleep action is launched)

## Requirements

- Python >= 3.6
- Requirements listed in [requirements.txt](requirements.txt):
  - [paho-mqtt](https://pypi.org/project/paho-mqtt/)
  - [python-dotenv](https://pypi.org/project/python-dotenv/)
  - [dotenv-settings-handler](https://pypi.org/project/dotenv-settings-handler/)
  - [apscheduler](https://pypi.org/project/APScheduler/)
- Recommended deployment method: Docker + Python Autoclonable App image

## Settings

Settings must be loaded as environment variables or by using a `.env` file. The variable names and their description are the following:

- `IOT_BROKER`: MQTT broker host
- `IOT_PORT`: MQTT broker port
- `IOT_OFF_TOPIC`: MQTT topic where the OFF/Sleep command messages are sent to
- `IOT_ON_TOPIC`: MQTT topic where the ON/WakeUp command messages are sent to
- `IOT_OFF_PAYLOAD`: MQTT message/payload sent as the OFF/Sleep command
- `IOT_ON_PAYLOAD`: MQTT message/payload sent as the ON/WakeUp command
- `IOT_OFF_HOUR`: Time (with format `hour:minute:second`) at which the OFF/Sleep order is sent
- `IOT_ON_HOUR`: Time (with format `hour:minute:second`) at which the ON/WakeUp order is sent
- `IOT_SET_AUTO_TOPIC`: MQTT topic to switch ON/OFF the Auto Sleep feature of this service
- `IOT_SET_AUTO_ENABLE_PAYLOAD`: MQTT message/payload sent as the ON command for the IOT_SET_AUTO_TOPIC
- `IOT_SET_AUTO_DISABLE_PAYLOAD`: MQTT message/payload sent as the OFF command for the IOT_SET_AUTO_TOPIC

## Test

Included tests test for the timer and the timer disabler to work as expected, using pytest. A working MQTT broker is required.

```
pytest .
```
