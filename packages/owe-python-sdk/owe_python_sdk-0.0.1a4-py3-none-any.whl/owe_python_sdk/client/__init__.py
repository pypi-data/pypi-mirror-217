from __future__ import annotations
from typing import List

from owe_python_sdk import schema as owe_schema


class Task:
    def __init__(self, schema: dict):
        self.schema = owe_schema.BaseTask(**schema)

    def depends_on(self, task: Task, *tasks: List[Task]) -> None:
        dependencies = [task, *tasks]
        for dep in dependencies:
            if type(dep) != self.__class__.__name__:
                raise TypeError(f"Task dependencies must be of type {self.__class__.__name__} | Recieved {type(dep)}")

        self.schema.depends_on += dependencies

class Pipeline:
    def __init__(self, schema: dict):
        self.schmea = owe_schema.BasePipeline(**schema)

    def add_task(self, task: Task, *tasks: List[Task]):
        new_tasks = [task, *tasks]
        for new_task in new_tasks:
            if type(new_task) != self.__class__.__name__:
                raise TypeError(f"Task dependencies must be of type Task | Recieved {type(new_task)}")

        self.schema.tasks += new_tasks

    def submit(self):
        print(self.schmea.dict())

    