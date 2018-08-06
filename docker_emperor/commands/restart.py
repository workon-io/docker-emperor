import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    cmd = root.bash(
        root.compose.bin,
        'restart',
        *args,
        mounting=root.mounting,
        is_system=True
    )
    if cmd.is_success:
        logger.success('<b>%s</b> is restarted.' % (root.compose.name, ))
