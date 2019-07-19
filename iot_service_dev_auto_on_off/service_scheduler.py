"""Create and Start the APScheduler Scheduler.
Schedule the Actions using APScheduler.
"""

# # Native # #
import atexit

# # Installed # #
from paho.mqtt.client import Client
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# # Package # #
from .actions import turn_on, turn_off
from .settings import settings

__all__ = ("scheduler", "schedule_turn_on", "schedule_turn_off")

scheduler = BackgroundScheduler()
atexit.register(scheduler.shutdown)
scheduler.start()


def schedule_turn_on(when: dict, client: Client):
    """Add a new Job to the Scheduler for the Turn ON action."""
    trigger = CronTrigger(**when)
    scheduler.add_job(
        func=turn_on,
        trigger=trigger,
        args=(client,),
        id=settings.on_job_id,
        name=settings.on_job_id
    )


def schedule_turn_off(when: dict, client: Client):
    """Add a new Job to the Scheduler for the Turn OFF action."""
    trigger = CronTrigger(**when)
    scheduler.add_job(
        func=turn_off,
        trigger=trigger,
        args=(client,),
        id=settings.off_job_id,
        name=settings.off_job_id
    )
