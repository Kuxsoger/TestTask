from unittest.mock import patch

import pytest

from app.exceptions import ItemNotFoundError, WrongItemFormatError
from app.services import BuildsService, TasksService
from tests.utils import load_yaml_file


@pytest.fixture
def mock_builds():
    builds = {}
    for build in load_yaml_file("builds.yaml")["builds"]:
        builds[build["name"]] = build["tasks"]

    BuildsService._BuildsService__builds = builds


@pytest.fixture
def mock_tasks():
    tasks = {}
    for task in load_yaml_file("tasks.yaml")["tasks"]:
        tasks[task["name"]] = task["dependencies"]

    TasksService._TasksService__tasks = tasks


@pytest.fixture
def mock_builds_yaml_wrong_item_format():
    prev_builds = BuildsService._BuildsService__builds
    BuildsService._BuildsService__builds = {}

    with patch(
        "app.services.load_yaml_file",
        return_value=load_yaml_file("builds_wrong_format.yaml")
    ) as mock:
        yield mock

    BuildsService._BuildsService__builds = prev_builds


@pytest.fixture
def mock_tasks_yaml_wrong_item_format():
    prev_tasks = TasksService._TasksService__tasks
    TasksService._TasksService__tasks = {}

    with patch(
        "app.services.load_yaml_file",
        return_value=load_yaml_file("tasks_wrong_format.yaml")
    ) as mock:
        yield mock

    TasksService._TasksService__builds = prev_tasks


class TestTasksService:

    def test__get_task__task_not_found(self, mock_tasks):
        with pytest.raises(ItemNotFoundError) as exc_info:
            TasksService.get_task("Not existing task name")

        assert exc_info.value.args[0] == "Task not found"
        assert str(exc_info.value) == "Task not found"

    def test__get_builds__wrong_build_format(
        self, mock_tasks_yaml_wrong_item_format
    ):
        with pytest.raises(WrongItemFormatError) as exc_info:
            TasksService.get_tasks()

        assert exc_info.value.args[0] == "Some tasks have wrong format"
        assert str(exc_info.value) == "Some tasks have wrong format"


class TestBuildsService:

    @pytest.mark.parametrize(
        "build_name",
        [
            "test_build_1",
            "test_build_2",
            "test_build_3",
            "test_build_4",
        ]
    )
    def test__get_tasks_for_build(
        self, build_name, mock_builds, mock_tasks
    ):
        expected_result = load_yaml_file("expected.yaml")["builds"][build_name]

        build = BuildsService.get_build(build_name)
        result = BuildsService.get_tasks_for_build(build)

        assert result == expected_result

    def test__get_build__build_not_found(self, mock_builds):
        with pytest.raises(ItemNotFoundError) as exc_info:
            BuildsService.get_build("Not existing build name")

        assert exc_info.value.args[0] == "Build not found"
        assert str(exc_info.value) == "Build not found"

    def test__get_builds__wrong_build_format(
        self, mock_builds_yaml_wrong_item_format
    ):
        with pytest.raises(WrongItemFormatError) as exc_info:
            BuildsService.get_builds()

        assert exc_info.value.args[0] == "Some builds have wrong format"
        assert str(exc_info.value) == "Some builds have wrong format"
