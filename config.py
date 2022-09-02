import os
import json

class Config:
    def __init__(self):
        self.__config = {
            'is_running': True,
            'key_code': dict(exit_key=0x23, toggle_key=0x2D),
            'settings': {
                'overlay': {
                  'updating': True,
                  'title': 'CW',
                  'delay': 0
                },
                'crosshair': {
                    'enabled': True,
                    'lineWidth': .1,
                    'color': [1, 1, 1],
                    'length': 10
                }
            }
        }

    def set_running(self, value: bool) -> None:
        self.__config["is_running"] = value

    def is_running(self) -> bool:
        return self.__config["is_running"]

    def get_exit_key(self) -> int:
        return self.__config["key_code"]["exit_key"]

    def get_toggle_key(self) -> int:
        return self.__config["key_code"]["toggle_key"]

    def offsets(self) -> dict:
        return self.__config["offset"]

    def settings(self) -> dict:
        return self.__config["settings"]

    def save(self) -> None:
        with open("config.json", "w") as f:
            json.dump(self.__config, f, indent=4)

    def load(self) -> None:
        if not os.path.exists("config.json"):
            return
        with open("config.json", "r") as f:
            self.__config = json.load(f)


if __name__ == '__main__':
    config = Config()
