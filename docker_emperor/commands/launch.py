import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    logger.cmd('Run project <b>%s</b>' % (root.compose.name, ))
    root.run_command('machine:start', internal=True)
    root.run_command('down', internal=True)
    root.run_command('up', *args, internal=True)