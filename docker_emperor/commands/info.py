import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    logger.cmd('Active mounting <b>%s</b>' % (root.project.compose.name, ))