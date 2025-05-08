from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class Status(Enum):
    TODO = 1
    WIP = 2
    DONE = 3


TASK_FIELDS = {"id", "description", "status", "createdAt", "updatedAt"}


@dataclass(repr=True)
class Task:
    id: int
    description: str
    status: Status
    createdAt: datetime
    updatedAt: datetime

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status.value,
            "createdAt": self.createdAt.isoformat(),
            "updatedAt": self.updatedAt.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<Task - ID: {self.id}, Description: {self.description}, Status: {self.status.name}, Created: {self.createdAt.isoformat()}, Updated: {self.updatedAt.isoformat()}>"

    def __str__(self) -> str:
        return f"Task - ID: {self.id}, Description: {self.description}, Status: {self.status.name}, Created: {self.createdAt.isoformat()}, Updated: {self.updatedAt.isoformat()}"

    @staticmethod
    def to_task(dict: dict) -> "Task | None":
        if not all(key in TASK_FIELDS for key in dict.keys()):
            print("Dictionary cannot be converted to task.")
            return None

        try:
            return Task(
                id=int(dict["id"]),
                description=dict["description"],
                status=Status(dict["status"]),
                createdAt=datetime.fromisoformat(dict["createdAt"]),
                updatedAt=datetime.fromisoformat(dict["updatedAt"]),
            )
        except Exception as e:
            print(f"Failed to convert dictionary to Task: {e}")
            return None
