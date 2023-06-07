from enum import Enum

class LogLevel(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3

class Log():
    def __init__(self, level):
        self.level = level


    def log(self, level, message):

