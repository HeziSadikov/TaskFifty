from datetime import datetime
import pytz
import dateutil.tz
from lib.enums import Priority, Status


def get_prompt(field, prompt):
    while True:
        user_input = input(prompt).strip()
        valid_input = validate_prompt(field, user_input)

        if not user_input:
            print(f"\nThe {field} can't be empty!\n")
            continue
        elif valid_input == None:
            continue
        else:
            return valid_input


def validate_prompt(field, user_input):
    if field in ["title", "description", "answer"]:
        return user_input

    elif field == "deadline":
        return validate_deadline(user_input)

    elif field == "priority":
        return validate_enum(user_input, Priority)

    elif field == "status":
        return validate_enum(user_input, Status)

    else:
        print(f"{field} is not a valid field.")
        return None


def validate_deadline(user_input):
    today = datetime.now()
    local_timezone = dateutil.tz.tzlocal()

    try:
        input_datetime = datetime.strptime(user_input, "%H:%M %d-%m-%y")

        if today > input_datetime:
            print("\nThe deadline must be in the future!")
            return None

        input_datetime = input_datetime.replace(tzinfo=local_timezone)
        utc_datetime = input_datetime.astimezone(pytz.utc)

        return utc_datetime.strftime("%Y-%m-%d %H:%M:%S")

    except ValueError:
        print("\nInvalid format, please try again.")
        return None


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
