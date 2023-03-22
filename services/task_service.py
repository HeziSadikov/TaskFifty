from services.db_service import db_instance
from prettytable import from_db_cursor
from lib.utils import get_prompt


def view_tasks():
    db_instance().cursor.execute(
        """SELECT
                id,
                title,
                description,
                strftime('%H:%M:%S, %d-%m-%Y', deadline, 'localtime') as deadline,
                CASE priority
                    WHEN 0 THEN 'LOW'
                    WHEN 1 THEN 'MEDIUM'
                    WHEN 2 THEN 'HIGH'
                    ELSE 'UNKNOWN'
                END AS priority,
                CASE status
                    WHEN 0 THEN 'TODO'
                    WHEN 1 THEN 'DONE'
                    WHEN 2 THEN 'LATE'
                    ELSE 'UNKNOWN'
                END AS status,
                strftime('%H:%M:%S, %d-%m-%Y', created, 'localtime') as created,
                strftime('%H:%M:%S, %d-%m-%Y', updated, 'localtime') as updated
            FROM tasks"""
    )
    pretty_formatted_table = from_db_cursor(db_instance().cursor)
    print("\n", pretty_formatted_table, sep="")


def add_task():
    title = get_prompt("title", "\nPlease choose a title: ")
    description = get_prompt("description", "\nPlease describe your task: ")
    deadline = get_prompt(
        "deadline",
        "\nPlease enter a date in the future,\n"
        + "formatted as follows:\nhh:mm dd-mm-yy\n",
    )
    priority = get_prompt("priority", "\nWhat's the priority? ")
    status = "TODO"

    try:
        db_instance().cursor.execute(
            """INSERT INTO tasks 
                    (title, description, deadline, priority, status, created, updated) 
                VALUES 
                    (?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                    """,
            (title, description, deadline, priority, status),
        )
    except:
        db_instance().conn.rollback()


def delete_task():
    while True:
        view_tasks()
        id_to_delete = input(
            "\nPlease type the id of the task you wish to delete: "
        ).strip()
        try:
            db_instance().cursor.execute("DELETE FROM tasks WHERE id = ?", id_to_delete)
            return
        except:
            db_instance().conn.rollback()


def update_task():
    allowed_columns = ["title", "description", "deadline", "priority", "status"]
    while True:
        view_tasks()

        id_to_update = input("\nPlease type the id of the task you wish to update: ")

        while True:
            column = input("In which column? ")
            if column not in allowed_columns:
                print("Invalid column, please try again.")
                continue
            break

        updated_column = get_prompt(column, f"Enter the new {column}: ")

        try:
            db_instance().cursor.execute(
                f"""UPDATE tasks
                        SET {column} = ?, updated = datetime('now')
                        WHERE id = ?;""",
                (updated_column, id_to_update),
            )
            return

        except:
            print("ERROR")
            db_instance().conn.rollback()
