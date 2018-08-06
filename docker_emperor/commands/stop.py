import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    root.run_command('machine:start', internal=True)
    cmd = root.bash(
        root.compose.bin,
        'stop',
        *args,
        mounting=root.mounting,
        is_system=True
    )
    if cmd.is_success:
        logger.success('<b>%s</b> is stopped.' % (root.compose.name, ))