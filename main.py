from services.db_service import db_instance, create_table_if_not_exists
from services.task_service import (
    view_tasks,
    add_task,
    delete_task,
    update_task,
    get_prompt,
)


def main():
    db_instance().connect()
    create_table_if_not_exists()
    view_tasks()
    action_selector()
    db_instance().close()


def action_selector():
    actions = {
        "1": {"label": "View tasks", "fn": view_tasks},
        "2": {"label": "Add a task", "fn": add_task},
        "3": {"label": "Delete a task", "fn": delete_task},
        "4": {"label": "Update a task", "fn": update_task},
    }

    while True:
        print("\nPlease choose the number of the desired action:\n")
        for k in actions:
            print(k, ". ", actions[k]["label"], sep="")

        selected_action = input("\nYour choice: ").strip()

        if selected_action in actions:
            actions[selected_action]["fn"]()
        else:
            print("\nInvalid selection.")
            continue

        while True:
            answer = get_prompt(
                "answer", "\nDo you wish to do anything else? (y/n) "
            ).lower()

            if answer == "y":
                break
            elif answer == "n":
                return
            else:
                print("\nInvalid answer")


if __name__ == "__main__":
    main()
