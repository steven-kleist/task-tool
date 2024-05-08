# task-tool
Simple task tool for python integrating with pyproject.toml

## Usage

Add the following section(s) to your `pyproject.toml` file:

```toml
[tool.tt.tasks]
build = "./scripts/buil_project.py"
update = "my_project.utils:update"
"build:docker" = {cmd = "docker", args = ["build", "--build-arg", "APP_VERSION=$APP_VERSION", "."]}

[tool.tt.tasks.build]
script = "./scripts/test.py"

[tool.tt.tasks.update]
module = "my_project.utils"
func = "update"

[tool.tt.tasks."build:docker"]
cmd = "docker"
args = [
   "build",
   "--build-arg",
   "APP_VERSION=$APP_VERSION",
   "."
]

[tool.tt.tasks.release]
cmd = "utils\\release_maker.bat"
args = "--release-type=major"
```

Call your tasks like this:

```shell
(venv) PS C:\Dev\Repos\my-project> tt build ...script-args...
```

## Prepare
1. `python -m venv venv`
2. Activate venv
   - PWSH: `. .\venv\Scripts\Activate.ps1`
   - CMD: `.\venv\Scripts\activate.bat`
3. `python -m pip install -e .[dev]`
