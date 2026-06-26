import os
import sys
import suap
import subprocess

from typer import Exit

from ..docker import INSIDE_DOCKER

__all__ = ()

def docker_callback(value: bool):
    if INSIDE_DOCKER:
        initial_docker_args = [
            "docker",
            "run",
            "--rm",
            "--name",
            "suap-container",
            "-v",
            f"{os.getcwd()}:/suap-docker-cwd",
            f"devgoldy/suap:{suap.__version__}"
        ]

        raise Exit(
            subprocess.call(initial_docker_args + sys.argv[1:])
        )