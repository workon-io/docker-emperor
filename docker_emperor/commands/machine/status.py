import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    
    cmd = root.bash(
        root.machine.bin, 
        'status', 
        root.machine.name, 
        *args,
        sys=True
    )
    logger.info('Machine <b>%s</b> status: <b>%s</b>.' % (root.machine.name, cmd.out))
    return cmd.out