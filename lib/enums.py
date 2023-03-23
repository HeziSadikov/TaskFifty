from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Status(Enum):
    TODO = 1
    DONE = 2


class Column(Enum):
    TITLE = 1
    DESCRIPTION = 2
    DEADLINE = 3
    PRIORITY = 4
    STATUS = 5
