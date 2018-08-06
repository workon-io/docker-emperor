import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger

'''
or docker-machine ssh virtualbox -- tce-load -wi rsync
'''
def run(root, *args, **kwargs):
    
    for sys in ['system', 'network', 'volume']:
        root.bash(
            root.docker_path,
            sys,
            'prune',
            mounting=root.mounting,
            is_system=True
        )