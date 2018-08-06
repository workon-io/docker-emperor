import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    root.run_command('machine:start', internal=True)
    root.bash(
        root.compose.bin,
        'exec', 
        *args,
        mounting=root.mounting,
        is_system=True
    )