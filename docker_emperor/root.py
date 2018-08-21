import os
import sys
import yaml
import tempfile
import json
import collections
import six
import argparse
import subprocess
import imp
from pprint import pprint
from docker_emperor.commands import Command
from docker_emperor.nodes.project import Project
from docker_emperor.exceptions import DockerEmperorException
from docker_emperor.utils import setdefaultdict, combine, yamp_load
import docker_emperor.logger as logger


class Root():

    version = __import__('docker_emperor').__version__

    def __init__(self):
        self.module_root = os.path.dirname(os.path.abspath(__file__))
        self.bin_root = os.path.join(self.module_root, 'bin')        
        self.config_path = os.path.expanduser(os.path.join('~', ".docker-emperor"))
        try:
            self.config = json.load(open(self.config_path, 'rb'))
        except:
            self.config = {}
        self.docker_path = 'docker'
        self.logger = logger.Logger(self)
        self.current_mounting = None

    @property
    def root_path(self):
        return os.getcwd()
    
    
    @property  
    def projects(self):
        n = '__projects'
        if not hasattr(self, n):
            self.config['projects'] = setdefaultdict(self.config.setdefault('projects'))
            setattr(self, n, self.config['projects'])
        return getattr(self, n)

    @property   
    def project(self):
        n = '__project'
        if not hasattr(self, n):
            setattr(self, n, Project(self))
        return getattr(self, n)

    @property
    def mounting(self):
        return self.project.mounting

    @property
    def compose(self):
        return self.project.compose

    def entrypoint(self, cmd=None, *args):
        try:
            args = list(args)
            if cmd:
                self.run_command(cmd, *args)
                self.save_config()
            else:
                logger.info('docker-emperor version {}'.format(self.version))

        except DockerEmperorException as e:
            logger.error(e)

    def run_command(self, name, *args, **kwargs):

        internal = kwargs.pop('internal', False)

        if args and args[-1][0] == '@':
            self.current_mounting = args[-1][1:]
            args = args[0:-1]

        if '--verbose' in args:
            Command.verbose = 1

        try:
            module_name = name.replace(':', '.')
            mod = __import__('docker_emperor.commands.{}'.format(module_name), globals(), locals(), ['run'], 0)
            return mod.run(self, *args, **kwargs)

        except ImportError as e:
            if internal:
                raise ImportError(e)
            else:
                if not self.project.run_command(name, *args, **kwargs):
                    logger.error('Unknown command %s' % name)
            return False

    def bash(self, *args, **kwargs):        
        cmd = Command(*args, **kwargs)
        cmd.run()
        return cmd

    def save_config(self):
        if self.config:
            file = open(self.config_path, 'wb')
            file.write(json.dumps(self.config, indent=4) )
            file.close()

    


# import readline

# def completer(text, state):
#     options = [i for i in commands if i.startswith(text)]
#     if state < len(options):
#         return options[state]
#     else:
#         return None

# readline.parse_and_bind("tab: complete")
# readline.set_completer(completer)

def entrypoint():
    try:
        argsparser = argparse.ArgumentParser(description='Docker emperor orchestrator') 
        argsparser.add_argument('args', nargs=argparse.REMAINDER, action="store") 
        Root().entrypoint(*argsparser.parse_args().args)
    except KeyboardInterrupt:
        logger.warning('Keyboard interrupt, exiting.')
        exit(0)

if __name__ == "__main__": entrypoint()








# # @property
# # def machine(self):
# #     attr = '_machine'
# #     if not hasattr(self, attr): setattr(self, attr, self.machines.select(self.machine_name))
# #     return getattr(self, attr)


# def _run(self, *args):
#     return Command(self, self.compose_path, *args, env=self.machine.docker_env)


# def cmd_start(self, *args):
#     self.cmd_prune()
#     self.compose("down --remove-orphans")
#     self.compose("up", *args)

# def cmd_startd(self, *args):
#     self.cmd_start('-d', *args)

# def cmd_logs(self, *args):
#     self.compose('logs', '-f', *args)


# def cmd_run(self, *args):
#     self.compose('run', *args)

# def cmd_exec(self, *args):
#     self.compose('exec', *args)

# def cmd_sethost(self, host):
#     bin_path = os.path.join(self.module_root, 'bin')
#     self.cmd("docker run -t -i -v {bin_path}/sethost:/bin/sethost -v /etc/hosts:/etc/hosthosts -v /etc/hosts.bak:/etc/hosthosts.bak busybox sh /bin/sethost 0.0.0.0 {}".format(host))

# def cmd_prune(self):
#     self.cmd("docker network prune -f")
#     self.cmd("docker system prune -f")
#     self.cmd("docker volume prune -f")


# def cmd(self, *args):
#     cmd = " ".join(args).strip()
#     self.log_info('> {}'.format(cmd))
#     try:
#         output = subprocess.check_output(cmd.split())
#         print(output.strip())
#     except Exception as e:
#         raise DockerEmperorException()#"error: " + str(e))#, sys.exc_info())


# def log_info(self, message):
#     print('{}{}{}{}'.format(C.YELLOW, C.LYELLOW, message, C.ENDC))

# def log_success(self, message):
#     print('{}{}{}{}'.format(C.GREEN, C.LGREEN, message, C.ENDC))

# def log_error(self, message):
#     print('{}{}{}{}'.format(C.ERROR, C.LERROR, message, C.ENDC))


