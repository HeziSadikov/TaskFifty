from datetime import datetime
import re

import dateutil.tz
import pytz


def get_datetime(date_kind):
    while True:
        print("\nPlease enter a valid time & date in the future:")
        hour = get_datetime_part("hour")
        minute = get_datetime_part("minute")
        day = get_datetime_part("day")
        month = get_datetime_part("month")
        year = get_datetime_part("year")

        user_input = f"{hour}:{minute} {day}-{month}-{year}"

        try:
            local_datetime_obj = datetime.strptime(user_input, "%H:%M %d-%m-%Y")
        except ValueError:
            print("\nInvalid date time, please try again.\n")
            continue

        if date_kind == "deadline" and not validate_deadline(local_datetime_obj):
            continue

        local_timezone = dateutil.tz.tzlocal()
        local_datetime_obj = local_datetime_obj.replace(tzinfo=local_timezone)
        utc_datetime = local_datetime_obj.astimezone(pytz.utc)

        return utc_datetime.timestamp()


def get_datetime_part(datetime_part):
    range = {
        "hour": {"pattern": r"^(2[0-3]|[0-1]?[0-9])$", "str": "0 and 23"},
        "minute": {"pattern": r"^([0-5]?[0-9])$", "str": "0 and 59"},
        "day": {"pattern": r"^(31|[0-2]?[0-9])$", "str": "0 and 31"},
        "month": {"pattern": r"^(1[0-2]|0?[0-9])$", "str": "0 and 12"},
        "year": {"pattern": r"^((?:19|20)[0-9][0-9])$", "str": "1900 and 2099"},
    }
    while True:
        try:
            part = input(f"{datetime_part.title()}: ").strip()
            if matches := re.search(range[datetime_part]["pattern"], part):
                pass
            else:
                raise ValueError
            return part
        except ValueError:
            print(
                f"""\nThe {datetime_part} must be an integer between {range[datetime_part]["str"]}.\n"""
            )


def validate_deadline(input_datetime):
    now = datetime.now()

    if now > input_datetime:
        print("\nThe deadline must be in the future!")
        return False

    return True
