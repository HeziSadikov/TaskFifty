from enum import Enum, auto


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Status(Enum):
    TODO = 1
    DONE = 2
