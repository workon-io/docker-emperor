import os
import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    logger.cmd('Down project <b>%s</b>' % (root.compose.name, ))
    cmd = root.bash(
        root.compose.bin,
        'down',
        '--remove-orphans',
        mounting=root.mounting,
        is_system=True
    )
    if cmd.is_success:
        logger.success('<b>%s</b> is down.' % (root.compose.name, ))