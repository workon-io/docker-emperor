import docker_emperor.logger as logger

'''
or docker-machine ssh virtualbox -- tce-load -wi rsync
'''
def run(root, *args, **kwargs):
    root.bash(
        *args,
        # mounting=root.mounting,
        is_system=True
    )