from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):
    
    Command(
        root.machine.bin, 
        'regenerate-certs', 
        root.machine.name,
        is_system=True
    )