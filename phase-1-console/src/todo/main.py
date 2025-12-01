"""Main entry point for the Todo application.

This module contains the main loop and menu dispatch logic.
"""

from todo.manager import TaskManager
from todo.ui import (
    display_welcome_message,
    display_menu,
    get_menu_choice,
    display_goodbye_message,
    display_error_message,
    display_no_tasks_message,
    format_task_list,
    format_empty_list_message,
    prompt_for_title,
    prompt_for_description,
    display_task_created_message,
    prompt_for_task_id,
    display_toggle_message,
    prompt_for_new_title,
    prompt_for_new_description,
    display_update_success_message,
    prompt_delete_confirmation,
    display_delete_success_message,
    display_delete_cancelled_message,
)


def handle_view_tasks(manager: TaskManager) -> None:
    """Handle the view all tasks menu option.

    Args:
        manager: The TaskManager instance.
    """
    tasks = manager.get_all_tasks()
    if not tasks:
        print(format_empty_list_message())
    else:
        print(format_task_list(tasks))


def handle_add_task(manager: TaskManager) -> None:
    """Handle the add new task menu option.

    Args:
        manager: The TaskManager instance.
    """
    while True:
        title = prompt_for_title()
        try:
            description = prompt_for_description()
            task = manager.add_task(title, description)
            print(display_task_created_message(task))
            break
        except ValueError as e:
            print(display_error_message(str(e)))


def handle_toggle_complete(manager: TaskManager) -> None:
    """Handle the mark complete/incomplete menu option.

    Args:
        manager: The TaskManager instance.
    """
    if not manager.has_tasks():
        print(display_no_tasks_message())
        return

    task_id_str = prompt_for_task_id()
    try:
        task_id = int(task_id_str)
        task = manager.toggle_complete(task_id)
        print(display_toggle_message(task))
    except ValueError:
        print(display_error_message("Please enter a valid task ID (number)"))
    except KeyError as e:
        print(display_error_message(str(e).strip('"').strip("'")))


def handle_update_task(manager: TaskManager) -> None:
    """Handle the update task menu option.

    Args:
        manager: The TaskManager instance.
    """
    if not manager.has_tasks():
        print(display_no_tasks_message())
        return

    task_id_str = prompt_for_task_id()
    try:
        task_id = int(task_id_str)
        task = manager.get_task(task_id)

        # Get new values (empty = keep current)
        new_title = prompt_for_new_title(task.title)
        new_description = prompt_for_new_description(task.description)

        # Only update if values provided
        title_to_update = new_title if new_title.strip() else None
        desc_to_update = new_description if new_description.strip() else None

        task = manager.update_task(task_id, title_to_update, desc_to_update)
        print(display_update_success_message(task))

    except ValueError as e:
        if "valid task ID" in str(e).lower():
            print(display_error_message("Please enter a valid task ID (number)"))
        else:
            print(display_error_message(str(e)))
    except KeyError as e:
        print(display_error_message(str(e).strip('"').strip("'")))


def handle_delete_task(manager: TaskManager) -> None:
    """Handle the delete task menu option.

    Args:
        manager: The TaskManager instance.
    """
    if not manager.has_tasks():
        print(display_no_tasks_message())
        return

    task_id_str = prompt_for_task_id()
    try:
        task_id = int(task_id_str)
        task = manager.get_task(task_id)

        # Ask for confirmation
        response = prompt_delete_confirmation(task)
        if response.lower() == "y":
            manager.delete_task(task_id)
            print(display_delete_success_message())
        else:
            print(display_delete_cancelled_message())

    except ValueError:
        print(display_error_message("Please enter a valid task ID (number)"))
    except KeyError as e:
        print(display_error_message(str(e).strip('"').strip("'")))


def main() -> None:
    """Main entry point for the Todo application.

    Runs the main loop, displaying menu and dispatching to handlers.
    """
    manager = TaskManager()

    print(display_welcome_message())

    try:
        while True:
            display_menu()
            choice = get_menu_choice()

            if choice == 1:
                handle_view_tasks(manager)
            elif choice == 2:
                handle_add_task(manager)
            elif choice == 3:
                handle_toggle_complete(manager)
            elif choice == 4:
                handle_update_task(manager)
            elif choice == 5:
                handle_delete_task(manager)
            elif choice == 6:
                print(display_goodbye_message())
                break

    except KeyboardInterrupt:
        print("\n\nInterrupted. Goodbye!")


if __name__ == "__main__":
    main()
