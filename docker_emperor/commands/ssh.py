from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    mounting = root.mounting    
    if mounting.is_localhost:
        logger.warning(mounting.LOCAL_MACHINE_WARNING)
    else:
        cmd = root.bash(
            mounting.docker_machine_bin, 
            'ssh', 
            mounting.name,
            *args,
            is_system=True
        )
        if cmd.is_success:
            logger.success('')
