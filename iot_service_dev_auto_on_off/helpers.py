"""Misc Helper functions"""

# # Native # #
from collections import OrderedDict

__all__ = ("hour_str_to_when_dict",)


def hour_str_to_when_dict(hour: str) -> dict:
    hour_split = hour.split(":")
    cron_keys = ("hour", "minute", "second")
    when = OrderedDict()
    for i, key in enumerate(cron_keys):
        try:
            value = int(hour_split[i])
        except StopIteration:
            value = 0
        when[key] = value
    return dict(when)
