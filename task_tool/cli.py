import argparse
import sys

from .execute import parse_command_type, execute_task
from .collector import collect_tasks_from_project


def cmd_help():
    pass


def main():
    parser = argparse.ArgumentParser(prog="tt", add_help=True)
    parser.add_argument("-p", "--project-file",
                        help="pyproject.toml file to use",
                        default="pyproject.toml")
    parser.add_argument("task", help="Task name to run")

    args = parser.parse_args()

    tasks = collect_tasks_from_project(args.project_file)

    if args.task not in tasks.keys():
        print(f'Task {args.task} not found.')
        sys.exit(1)

    task_data = tasks[args.task]
    task = parse_command_type(task_data)
    result = execute_task(task)

    result.check_returncode()
    sys.exit(result.returncode)
