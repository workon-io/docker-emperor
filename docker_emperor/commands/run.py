import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    logger.cmd('Run project <b>%s</b>' % (root.compose.name, ))
    root.run_command('machine:start', internal=True)
    cmd = root.bash(
        root.compose.bin,
        'run',
        *args,
        mounting=root.mounting,
        is_system=True
    )
    if cmd.is_success:
        logger.success('<b>%s</b> is started.' % (root.compose.name, ))