from manager import TaskManager
from task import Status
import re

status_map = {
    "todo": Status.TODO,
    "in-progress": Status.WIP,
    "done": Status.DONE,
}


def help():
    print('add "<description>"')
    print('update <task-id> "<description>"')
    print("delete <task-id>")
    print("mark-in-progress <task-id>")
    print("mark-done <task-id>")
    print("list <optional status: todo, in-progress, done>")
    print("quit\n")


def parse_input(option: str) -> tuple[str, ...]:
    option = option.strip()
    if option == "list" or option == "help" or option == "quit":
        return (option,)
    elif match := re.fullmatch(r"add \"(.*?)\"", option):
        return ("add", match.group(1))
    elif match := re.fullmatch(r"update ([1-9][0-9]*?) \"(.*?)\"", option):
        return ("update", match.group(1), match.group(2))
    elif match := re.fullmatch(r"delete ([1-9][0-9]*?)", option):
        return ("delete", match.group(1))
    elif match := re.fullmatch(r"mark-in-progress ([1-9][0-9]*?)", option):
        return ("mark-in-progress", match.group(1))
    elif match := re.fullmatch(r"mark-done ([1-9][0-9]*?)", option):
        return ("mark-done", match.group(1))
    elif match := re.fullmatch(r"list (.+.*?)", option):
        return ("list", match.group(1))

    return ("",)


def list_by_status(tm: TaskManager, status: str) -> None:
    if status:
        value = status_map.get(status.lower())
        if value is None:
            print("Invalid status code.")
            return
        task_list = tm.read_tasks()
        filtered_tasks = [t for t in task_list if t.status == value]
        for t in filtered_tasks:
            print(t)


def main():
    task_manager = TaskManager()
    print("Welcome. Type help for info")
    while True:
        option = parse_input(input("task-cli "))
        match option:
            case ("add", description):
                if description.strip() == "":
                    print("Description cannot be empty.")
                else:
                    task_manager.add_task(option[1])
            case ("update", _, _):
                try:
                    task_manager.update_task(int(option[1]), option[2])
                except ValueError:
                    print("Invalid id.")
            case ("delete", _):
                try:
                    task_manager.delete_task(int(option[1]))
                except ValueError:
                    print("Invalid id.")
            case ("mark-in-progress", _):
                try:
                    task_manager.update_task(int(option[1]), status=Status.WIP)
                except ValueError:
                    print("Invalid id.")
            case ("mark-done", _):
                try:
                    task_manager.update_task(int(option[1]), status=Status.DONE)
                except ValueError:
                    print("Invalid id.")
            case ("list",):
                for t in task_manager.read_tasks():
                    print(t)
            case ("list", _):
                list_by_status(task_manager, option[1])
            case ("help",):
                help()
            case ("quit",):
                print("Goodbye.")
                break
            case _:
                print("Invalid option!")
                continue


if __name__ == "__main__":
    main()
