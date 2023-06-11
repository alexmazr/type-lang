from enum import Enum


class LogLevel(Enum):
    DEBUG = 1
    WARNING = 2


level = LogLevel.WARNING


class Log():
    def error(self, message):
        raise SystemExit(f"ERROR: {message}")

    def warning(self, message):
        global level
        if level.value <= LogLevel.WARNING.value:
            print(f"WARNING: {message}")

    def debug(self, message):
        global level
        if level.value <= LogLevel.DEBUG.value:
            print(message)
