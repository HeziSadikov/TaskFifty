from datetime import datetime
import dateutil.tz
import pytz
from lib.enums import Priority, Status, Column
from services.db_service import db


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
    if field in ["title", "description"]:
        return user_input

    elif field == "deadline":
        return validate_deadline(user_input)

    elif field == "priority":
        return validate_enum(user_input, Priority)

    elif field == "status":
        return validate_enum(user_input, Status)

    elif field == "task id":
        return validate_task_id(user_input)

    elif field == "column":
        return validate_enum(user_input, Column)

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

        return utc_datetime.timestamp()

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


def validate_task_id(user_input):
    from services.task_service import view_tasks

    try:
        result = db.cursor.execute(
            "SELECT * FROM tasks WHERE id = ?", (int(user_input),)
        )

        if result.fetchone() is None:
            raise ValueError

        return int(user_input)

    except ValueError:
        print("\nInvalid id.")
        view_tasks()
        return None


def update_status_if_late():
    from services.task_service import update_cell

    # only look at tasks that are in TODO status
    # if today > deadline, change status to LATE

    today = datetime.now().timestamp()

    results = db.cursor.execute(
        f"""
        SELECT id FROM tasks 
        WHERE status = 1 
        AND deadline < {today}"""
    )

    if rows := results.fetchall():
        for row in rows:
            update_cell(row[0], "status", 3)
