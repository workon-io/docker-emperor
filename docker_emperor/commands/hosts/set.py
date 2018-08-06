import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger


def run(root, *args, **kwargs):

    root.run_command('machine:start', internal=True)

    mounting = root.mounting
    hosts = mounting.get_machine_hosts()
    if hosts:
        
        for host in hosts:

            ip_address = '0.0.0.0'
            logger.cmd('Set host <b>%s</b> mapped at %s in /etc/hosts.' % (host, ip_address))
            cmd = root.bash(
                "docker", 
                "run", 
                "-t", 
                "-i" ,
                "-v", "%s/managehosts:/bin/managehosts" % root.bin_root,
                "-v", "/etc/hosts:/etc/host_hosts",
                "-v", "/etc/hosts.bak:/etc/host_hosts.bak",
                "busybox",
                "sh", 
                "/bin/managehosts" ,
                "add %s %s %s" % (host, ip_address, root.project.name),
                mounting=mounting,
                is_system=True
            )

            if cmd.is_success:
                logger.success('Host <b>%s</b> has been set.' % (host, ))
