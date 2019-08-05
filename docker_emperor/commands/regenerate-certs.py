from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    
    Command(
        root.mounting.docker_machine_bin, 
        'regenerate-certs', 
        root.mounting.docker_machine_name,
        is_system=True
    )