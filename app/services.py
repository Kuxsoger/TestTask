from collections import OrderedDict
from functools import cache

import yaml

from app.config import builds_path, tasks_path
from app.exceptions import (
    EmptyFileError,
    ItemNotFoundError,
    WrongFileFormatError,
    WrongItemFormatError,
)
from app.utils import load_yaml_file


class TasksService:
    __tasks = {}

    @classmethod
    def load_tasks(cls):
        try:
            tasks = load_yaml_file(tasks_path)["tasks"]
            for task in tasks:
                cls.__tasks[task["name"]] = task["dependencies"]
        except (KeyError, TypeError):
            raise WrongItemFormatError("Some tasks have wrong format")
        except yaml.YAMLError as exc:
            raise WrongFileFormatError(f"Error in tasks yaml file: {exc}")

        if not cls.__tasks:
            raise EmptyFileError("Tasks yaml file doesn't have any tasks")

    @classmethod
    def get_tasks(cls) -> dict[str, list[str]]:
        if not cls.__tasks:
            cls.load_tasks()
        return cls.__tasks

    @classmethod
    def get_task(cls, task_name: str) -> list[str]:
        task = cls.get_tasks().get(task_name)
        if task is None:
            raise ItemNotFoundError("Task not found")
        return task

    @classmethod
    @cache
    def get_task_dependencies(cls, task_name: str) -> OrderedDict[str, None]:
        task_dependencies = cls.get_task(task_name)
        if not task_dependencies:
            return OrderedDict.fromkeys([task_name])

        dependencies = OrderedDict()
        for task_dependency in task_dependencies:
            dependencies.update(cls.get_task_dependencies(task_dependency))

        dependencies[task_name] = None
        return dependencies


class BuildsService:
    __builds = {}

    @classmethod
    def load_builds(cls) -> None:
        try:
            builds = load_yaml_file(builds_path)["builds"]
            for build in builds:
                cls.__builds[build["name"]] = build["tasks"]
        except (KeyError, TypeError):
            raise WrongItemFormatError("Some builds have wrong format")
        except yaml.YAMLError as exc:
            raise WrongFileFormatError(f"Error in builds yaml file: {exc}")

        if not cls.__builds:
            raise EmptyFileError("Builds yaml file doesn't have any builds")

    @classmethod
    def get_builds(cls) -> dict[str, list[str]]:
        if not cls.__builds:
            cls.load_builds()
        return cls.__builds

    @classmethod
    def get_build(cls, build_name: str) -> list[str]:
        build = cls.get_builds().get(build_name)
        if build is None:
            raise ItemNotFoundError("Build not found")
        return build

    @classmethod
    def get_tasks_for_build(cls, build: list[str]) -> list[str]:
        # Since Python doesn't have implementation for ordered set
        # we will use OrderedDict as one
        result = OrderedDict()

        for task in build:
            result.update(TasksService.get_task_dependencies(task))

        return list(result.keys())
