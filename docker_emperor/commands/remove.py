import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    
    name = args[0].strip() if args else None
    if name:
        args = list(args)
        args.pop(0)
        mounting = root.project['mounting'].get(name)
        if mounting:
            logger.success(u'Prepare mounting <b>%s</b> to be created.' % mounting.name)
        else:
            logger.error(u'Mounting <b>%s</b> unknow.' % name)
            exit(1)
    else:
        mounting = root.mounting
        
    if not mounting.is_localhost:

        logger.cmd('Create machine <b>%s</b>' % (mounting.docker_machine_name, ))
        logger.cmd('With driver <b>%s</b>' % (mounting.get_machine_driver(), ))
        cmd = root.bash(
            mounting.docker_machine_bin, 
            'rm',       
            mounting.docker_machine_name,#root.compose.name,
            *args,
            is_system=True
        )
    else:
        logger.warning(mounting.LOCAL_MACHINE_WARNING)