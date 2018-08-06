import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    logger.cmd('Rebuild <b>%s</b>' % (root.project.compose.name, ))
    root.project.machine.start()
    cmd = root.bash(
        root.project.compose.bin, 
        '--no-cache',
        'build',
        *args, 
        mounting=root.mounting,
        is_system=True
    )
    if cmd.is_success:
        logger.success('<b>%s</b> rebuilt.' % (root.project.compose.name, ))
