from __future__ import annotations

import json, os

from typing import List

from owe_python_sdk import schema as owe_schema


class Task:
    def __init__(self, schema: dict):
        self.schema = owe_schema.BaseTask(**schema)

    def depends_on(self, task: Task, *tasks: List[Task], can_fail=False) -> None:
        dependencies = [task, *tasks]
        for dep in dependencies:
            if type(dep) != Task:
                raise TypeError(f"Task dependencies must be of type {self.__class__.__name__} | Recieved {type(dep)}")

            self.schema.depends_on.append(owe_schema.TaskDependency({
                "id": dep.id,
                "can_fail": can_fail
            }))

class Pipeline:
    def __init__(self, schema: dict):
        self.schema = owe_schema.BasePipeline(**schema)

    def add_task(self, task: Task, *tasks: List[Task]):
        new_tasks = [task, *tasks]
        for new_task in new_tasks:
            if type(new_task) != Task:
                raise TypeError(f"Task dependencies must be of type Task | Recieved {type(new_task)}")
            
            self.schema.tasks.append(new_task.schema)

    def submit(self):
        print(json.loads(json.dumps(self.schema.dict())))

    