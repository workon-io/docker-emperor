from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    
    logger.cmd('Command aliases for <b>%s</b> : \r' % root.project.compose.name)
    for aliase in root.project['aliases']:
        logger.choice(' <b>%s</b>%s%s' % (aliase.name, ' '*(20-len(aliase.name)), aliase))

