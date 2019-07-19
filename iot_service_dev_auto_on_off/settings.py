
# # Installed # #
from dotenv_settings_handler import BaseSettingsHandler
from dotenv import load_dotenv

__all__ = ("settings",)


class MySettings(BaseSettingsHandler):
    broker: str
    port = 1883
    off_topic: str
    off_payload = "OFF"
    on_topic: str
    on_payload = "ON"
    on_job_id = "ON Job"
    off_job_id = "OFF Job"
    on_hour: str
    off_hour: str
    set_auto_topic: str
    set_auto_enable_payload = "ON"
    set_auto_disable_payload = "OFF"

    class Config:
        env_prefix = "IOT_"


load_dotenv()  # Provisional for development only
settings = MySettings()
