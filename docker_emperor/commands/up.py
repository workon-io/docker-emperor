import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    root.run_command('machine:start', internal=True)

    if '--set-hosts' in args:
        root.run_command('hosts:set', internal=True)
        args = filter(lambda s:s != '--set-hosts', args)
    else:
        logger.cmd('Hosts mapping ignored.')

    logger.cmd('Up project <b>%s</b>' % (root.compose.name, ))
    cmd = root.bash(
        root.compose.bin,
        'up',
        *args,
        compose=root.compose,
        is_system=True
    )
    if cmd.is_success:
        logger.success('<b>%s</b> is up.' % (root.compose.name, ))

    if root.mounting['hosts']:
        for host in root.mounting['hosts']:
            logger.success('Project is accessible by http://%s.' % (host, ))

