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
        cmd = root.bash(
            mounting.docker_machine_bin, 
            'create', 
            '--driver',
            mounting.get_machine_driver(),        
            mounting.name,
            *args,
            is_system=True
        )
    else:
        logger.warning(mounting.LOCAL_MACHINE_WARNING)