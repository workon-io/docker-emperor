import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    logger.cmd('Build <b>%s</b>' % (root.project.compose.name, ))
    root.run_command('machine:start', internal=True)

    cmd = root.bash(
        root.project.compose.bin, 
        'build',
        *args, 
        mounting=root.mounting,
        is_system=True
    )
    if cmd.is_success:
        logger.success('<b>%s</b> built.' % (root.project.compose.name, ))
