from datetime import datetime
import pytz
import dateutil.tz


def get_prompt(field, prompt):
    while True:
        user_input = input(prompt).strip()
        valid_input = valid_prompt(field, user_input)

        if not user_input:
            print(f"\nThe {field} can't be empty!\n")
            continue
        elif not valid_input:
            continue
        else:
            return valid_input


def valid_prompt(field, user_input):
    if field in ["title", "description", "answer"]:
        return user_input

    elif field == "deadline":
        today = datetime.now()
        local_timezone = dateutil.tz.tzlocal()
        try:
            input_datetime = datetime.strptime(user_input, "%H:%M %d-%m-%y")

            if today > input_datetime:
                print("\nThe deadline must be in the future!")
                return None

            input_datetime = input_datetime.replace(tzinfo=local_timezone)
            utc_datetime_object = input_datetime.astimezone(pytz.utc)

            return utc_datetime_object.strftime("%Y-%m-%d %H:%M:%S")

        except ValueError:
            print("\nInvalid format, please try again.")
            return None

    elif field == "priority":
        user_input = user_input.upper()
        if user_input not in ["HIGH", "MEDIUM", "LOW"]:
            print(
                "\nPriority can only be: High, Medium or Low.\n" + "Please try again.\n"
            )
            return None
        else:
            return user_input

    elif field == "status":
        user_input = user_input.upper()
        if user_input not in ["TODO", "DONE"]:
            print("\nYou can only choose to mark a task as DONE/TODO\n")
            return None
        return user_input
