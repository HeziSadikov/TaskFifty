from enum import Enum, auto


class Priority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2


class Status(Enum):
    TODO = 0
    DONE = 1
    LATE = 2
