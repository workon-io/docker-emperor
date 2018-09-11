import docker_emperor.logger as logger

'''
or docker-machine ssh virtualbox -- tce-load -wi rsync
'''
def run(root, *args, **kwargs):

    logger.cmd('Removing all docker containers..')
    root.bash(
        'docker rm $(docker ps -a -q) -f',
        compose=root.compose,
        is_system=True
    )