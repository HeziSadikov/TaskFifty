from services.db_service import db_instance, create_table_if_not_exists
from services.task_service import (
    view_tasks,
    add_task,
    delete_task,
    update_task,
)


def main():
    db_instance().connect()
    create_table_if_not_exists()
    view_tasks()
    while True:
        action_selector()


def action_selector():
    actions = {
        "1": {"label": "View tasks", "fn": view_tasks},
        "2": {"label": "Add a task", "fn": add_task},
        "3": {"label": "Delete a task", "fn": delete_task},
        "4": {"label": "Update a task", "fn": update_task},
        "5": {"label": "EXIT", "fn": exit_fn},
    }

    selected_action = input(
        "\nPlease choose the number of the desired action:\n\n"
        + "\n".join(f"""{k}. {actions[k]["label"]}""" for k in actions)
        + "\n\nYour choice: ",
    )

    if selected_action in actions:
        actions[selected_action]["fn"]()
    else:
        print("\nInvalid selection.")


def exit_fn():
    db_instance().close()
    exit()


if __name__ == "__main__":
    main()
