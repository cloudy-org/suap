# uv run scripts/docker_build.py

import os
import suap

os.system(
    f"docker buildx build -t devgoldy/suap:{suap.__version__} ."
)

os.system(
    "docker buildx build -t devgoldy/suap:latest ."
)