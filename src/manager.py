import json
from task import Task, Status
from pathlib import Path
from datetime import datetime

TASKS = "tasks"
DEFAULT_DICT = {TASKS: []}


class TaskManager:
    def __init__(self) -> None:
        self.__path = Path(__file__).parent
        self.__file = self.__path / "tasks.json"

        if not self.__file.exists():
            print("Creating file...")
            with open(self.__file, "xt", encoding="utf-8") as file:
                json.dump(DEFAULT_DICT, file, indent=4)

    def _generate_id(self) -> int:
        tasks = self.read_tasks()
        if not tasks:
            return 1
        return max(task.id for task in tasks) + 1

    def __read_file(self) -> dict:
        try:
            with open(self.__file, "rt", encoding="utf-8") as file:
                data = json.loads(file.read())
        except json.JSONDecodeError:
            print(f"Warning: JSON file {self.__file} may be corrupted.")
            data = DEFAULT_DICT

        return data

    def add_task(self, desc: str) -> None:
        task: Task = Task(
            self._generate_id(),
            desc,
            Status.TODO,
            datetime.now(),
            datetime.now(),
        )

        data = self.__read_file()

        tasks = data.get(TASKS, [])
        if not isinstance(tasks, list):
            print("Warning: Malformed task list. Resetting task list.")
            tasks = []

        if any(t["id"] == task.id for t in tasks):
            print(f"Task with id {task.id} already exists.")
            return

        tasks.append(task.to_dict())
        data[TASKS] = tasks

        try:
            with open(self.__file, "wt", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
                print(f"Successfully added task {task.id}")
        except Exception as e:
            print(f"Error writing the JSON file: {e}")

    def read_tasks(self) -> list[Task]:
        data = self.__read_file()
        tasks_data: list[dict] = data.get(TASKS, [])
        if not isinstance(tasks_data, list):
            print("Warning: Malformed task list. Resetting task list.")
            tasks_data = []
        task_list = []
        for t in tasks_data:
            if (task := Task.to_task(t)) is not None:
                task_list.append(task)
        return task_list

    def update_task(self, id: int, description: str = "", status: Status | None = None) -> None:
        data = self.__read_file()
        tasks: list[dict] = data.get(TASKS, [])
        if not isinstance(tasks, list):
            print("Warning: Malformed task list.")
            return

        if not any(isinstance(t.get("id"), int) and t["id"] == id for t in tasks):
            print(f"Task {id} does not exist.")
            return

        for t in tasks:
            if t["id"] == id:
                t["description"] = description if description else t["description"]
                t["status"] = status.value if status else t["status"]
                t["updatedAt"] = datetime.now().isoformat()
                break
        data[TASKS] = tasks
        try:
            with open(self.__file, "wt", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
                print(f"Successfully updated task {id}")
        except Exception as e:
            print(f"Error writing the JSON file: {e}")

    def delete_task(self, id: int) -> None:
        data = self.__read_file()
        tasks: list[dict] = data.get(TASKS, [])
        if not isinstance(tasks, list):
            print("Warning: Malformed task list.")
            return

        if not any(isinstance(t.get("id"), int) and t["id"] == id for t in tasks):
            print(f"Task {id} does not exist.")
            return
        updated_tasks = [t for t in tasks if not (isinstance(t.get("id"), int) and t["id"] == id)]
        data[TASKS] = updated_tasks

        try:
            with open(self.__file, "wt", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
                print(f"Successfully deleted task {id}")
        except Exception as e:
            print(f"Error writing the JSON file: {e}")
