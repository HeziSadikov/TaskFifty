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


def get_enum(enum):
    enums = {
        "priority": Priority,
        "status": Status,
        "column": Column,
    }

    if type(enum) == str:
        enum = enums[enum]

    while True:
        user_input = input(enum_prompt(enum))

        if (result := validate_enum(user_input, enum)) is not None:
            return result


def validate_enum(user_input, input_enum):
    try:
        return input_enum(int(user_input)).value
    except ValueError:
        pass

    try:
        return input_enum[user_input.upper()].value
    except KeyError:
        pass

    print("\nInvalid choice.")
    return None


def enum_prompt(enum):
    return (
        f"\nPlease choose a {enum.__name__.lower()}:\n\n"
        + "\n".join(f"{option.value}. {option.name.title()}" for option in enum)
        + "\n\nYour choice: "
    )
