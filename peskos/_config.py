from functools import lru_cache
import json
import os


days_of_week = {
    1: "monday",
    2: "tuesday",
    3: "wednesday",
    4: "thursday",
    5: "friday",
    6: "saturday",
    7: "sunday",
}
config_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    "config.json"
)


@lru_cache(maxsize=1)
def get_config():
    with open(config_path, "r", encoding="utf8") as config:
        data = json.load(config)
    return data
