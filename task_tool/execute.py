import shlex
from abc import ABC, abstractmethod, ABCMeta
from dataclasses import dataclass
from pathlib import Path
import subprocess
import sys
from subprocess import CompletedProcess


class ExecutableCommandBuilder(ABC, metaclass=ABCMeta):
    @abstractmethod
    def build_executable_command(self) -> str: ...

    @classmethod
    @abstractmethod
    def check_string(cls, string: str) -> bool: ...


@dataclass
class PythonScript(ExecutableCommandBuilder):
    script: Path

    def build_executable_command(self) -> str:
        return f'{sys.executable} {self.script}'

    @classmethod
    def check_string(cls, string: str) -> bool:
        path = Path(string)
        return path.exists()


@dataclass
class PythonModul(ExecutableCommandBuilder):
    module: str
    func: str

    def build_executable_command(self) -> str:
        return f'{sys.executable} -c "from {self.module} import {self.func}; {self.func}()"'

    @classmethod
    def check_string(cls, string: str) -> bool:
        if ":" in string:
            return True
        return False

@dataclass
class ExternalCommand(ExecutableCommandBuilder):
    cmd: str
    args: str | list[str]

    def format_args(self):
        if type(self.args) is list:
            return " ".join(self.args)
        return self.args

    def build_executable_command(self) -> str:
        return f'{self.cmd} {self.format_args()}'

    @classmethod
    def check_string(cls, string: str) -> bool:
        cmd = shlex.split(string, comments=False, posix=True)
        if cmd and len(cmd) >= 2:
            return True
        return False


def parse_command_type(data: str | dict[str, str]) -> ExecutableCommandBuilder:
    if type(data) is str:
        if PythonScript.check_string(data):
            return PythonScript(script=Path(data))
        elif PythonModul.check_string(data):
            parts = data.split(":", 1)
            return PythonModul(module=parts[0], func=parts[1])
        elif ExternalCommand.check_string(data):
            parts = shlex.split(data, comments=False, posix=True)
            return ExternalCommand(cmd=parts[0], args=parts[1:])
    elif type(data) is dict:
        if {"script"} <= data.keys():
            return PythonScript(**data)
        elif {"module", "func"} <= data.keys():
            return PythonModul(**data)
        elif {"cmd", "args"} <= data.keys():
            return ExternalCommand(**data)
        else:
            raise ValueError("data must be str or dict.")

    else:
        raise ValueError("data must be str or dict.")


def execute_task(cmd: ExecutableCommandBuilder) -> CompletedProcess[bytes]:
    result = subprocess.run(args=cmd.build_executable_command(),
                            shell=False,
                            stdout=sys.stdout,
                            stderr=sys.stderr,
                            stdin=sys.stdin)
    return result
