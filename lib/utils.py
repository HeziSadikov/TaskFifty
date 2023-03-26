from datetime import datetime

from lib.get_datetime import get_datetime
from lib.enums import get_enum
from services.db_service import db


def get_prompt(field, prompt=None):
    while True:
        if not (valid_input := validate_prompt(field, prompt)):
            print(f"\nInvalid {field}.")
            continue
        else:
            return valid_input


def validate_prompt(field, prompt):
    match field:
        case "title" | "description":
            return get_text(field, prompt)
        case "priority" | "status" | "column":
            return get_enum(field)
        case "deadline":
            return get_datetime("deadline")
        case "id":
            return validate_task_id(get_text(field, prompt))
        case _:
            print(f"{field} is not a valid field")
            return None


def get_text(field, prompt=None):
    if prompt is None:
        return input(f"\nPlease choose the {field}: ").strip()
    else:
        return input(prompt).strip()


def validate_task_id(user_input):
    from services.task_service import view_tasks

    try:
        user_input = int(user_input)
        result = db.cursor.execute("SELECT id FROM tasks WHERE id = ?", (user_input,))
        if result.fetchone() is not None:
            return user_input
    except ValueError:
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
