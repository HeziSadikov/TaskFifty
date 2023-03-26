from datetime import datetime

from lib.get_datetime import get_datetime
from lib.enums import get_enum
from services.db_service import db


def get_prompt(field, prompt=None):
    while True:
        if prompt is None:
            valid_input = validate_prompt(field)
        else:
            if not (user_input := input(prompt).strip()):
                print(f"\nThe {field} can't be empty!\n")
                continue
            valid_input = validate_prompt(field, user_input)

        if valid_input is None:
            continue
        else:
            return valid_input


def validate_prompt(field, user_input=None):
    match field:
        case "title" | "description":
            return user_input
        case "priority" | "status" | "column":
            return get_enum(field)
        case "deadline":
            return get_datetime("deadline")
        case "id":
            return validate_task_id(user_input)
        case _:
            print(f"{field} is not a valid field")
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
