import tomllib


def collect_tasks_from_project(project_file: str = "pyproject.toml") -> dict[str, str]:
    with open(project_file, "rb") as f:
        data = tomllib.load(f)
        return data['tool']['tt']['tasks']
