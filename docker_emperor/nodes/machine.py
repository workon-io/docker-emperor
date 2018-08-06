import os
import six
import collections
from docker_emperor.commands import Command
from docker_emperor.nodes.environment import Environment
from docker_emperor.nodes.service import Services
from docker_emperor.nodes.command import Commands
from docker_emperor.utils import setdefaultdict, OrderedDict
import docker_emperor.logger as logger


__all__ = ['Machines', 'Machine']


# DRIVERS

# Amazon Web Services
# Microsoft Azure
# Digital Ocean
# Exoscale
# Google Compute Engine
# Generic
# Microsoft Hyper-V
# OpenStack
# Rackspace
# IBM Softlayer
# Oracle VirtualBox
# VMware vCloud Air
# VMware Fusion
# VMware vSphere
# VMware Workstation (unofficial plugin, not supported by Docker)
# Grid 5000 (unofficial plugin, not supported by Docker)


class Machines(dict):

    DEFAULT = {
        'localhost': {}
    }

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __init__(self, data):
        super(self.__class__, self).__init__(setdefaultdict(data))
        if self:
            for key, val in self.items():
                self[key] = Machine(key, val)
        else:
            self['localhost'] = Machine('localhost')
    
    def __iter__(self):
        for key, val in self.items():
            yield val
            
    def __repr__(self): 
        return ", ".join(str(m) for m in self)

    def __getitem__(self, i): 
        if isinstance(i, int):
            return [c for c in self][i]
        else:
            return self.get(i, None)


class Machine(dict):

    COMMANDS = [
        'ssh'
    ]
    LOCAL_MACHINE_WARNING = 'You are already on a local machine'

    class Drivers(object):
        LOCALHOST = 'localhost'
        GENERIC_LOCALHOST = 'generic --generic-ip-address localhost'  

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)   

    def __init__(self, name, data={}, bin="docker-machine"):
        self.key = name
        self.name = name
        self.bin = bin
        super(Machine, self).__init__(setdefaultdict(data))
        for default_name, default_class in [
            ('environment', Environment),
            ('services', Services),
            ('commands', Commands),
        ]:
            self[default_name] = default_class(self[default_name])

        if not isinstance(self['driver'], six.string_types): 
            self['driver'] = Machine.Drivers.LOCALHOST
        if not isinstance(self['hosts'], list): 
            self['hosts'] = []
        if not isinstance(self['files'], list): 
            self['files'] = []
        if not isinstance(self['workdir'], six.string_types): 
            self['workdir'] = '/home/docker/'


    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)

    def __getitem__(self, key): 
        return self.get(key)

    def bash(self, *args, **kwargs):        
        cmd = Command(self.bin, *args, **kwargs)
        cmd.run()
        return cmd

    @property
    def is_localhost(self):
        return self['driver'] == Machine.Drivers.LOCALHOST

    @property
    def is_generic(self):
        return self['driver'].startswith('generic')

    @property
    def exists(self):
        cmd = self._run("ls", "--filter", "NAME=" + self.name, "--format", "{{.Name}}", machine=self, tty=False)
        for line in cmd.lines:
            if line == self.name:return True
        return False

    @property
    def docker_env(self):
        n = '__docker_env'
        if not hasattr(self, n):
            if self.is_localhost:
                env = []
            else:
                cmd = self.bash('env', self.name)
                starts = 'export '
                env = [line.lstrip(starts) for line in cmd.lines if line.startswith(starts)]
            setattr(self, n, env)
        return getattr(self, n)

    def start(self):
        if self.is_localhost:
            if not self.is_running:
                self.bash('start', self.name, sys=True).run().log()  
        return self.is_running

    @property
    def is_running(self):
        return self.status == 'Running'

    @property
    def is_startable(self):
        return not self.is_localhost and not self.is_generic
    
    
    @property
    def status(self):
        if self.is_localhost:
            return 'Running'
        else:
            return self.bash('status', self.name).out
    
    @property
    def ip(self):
        if self.is_localhost:
            return '0.0.0.0'
        else:
            return self.bash('ip', self.name, log=False, machine=self).out.strip()

    @property
    def pwd(self):
        return self.bash('ssh', self.name, 'pwd', log=False, machine=self).out.strip()

    @property
    def inspect(self):
        return self.bash('inspect', self.name, machine=self, tty=False).out

    @property
    def active(self):
        return self.bash('active', machine=self, tty=False).out

    def remove(self):
        return self.bash('rm', self.name, machine=self)

# active
# config
# create
# env
# help
# inspect
# ip
# kill
# ls
# mount
# provision
# regenerate-certs
# restart
# rm
# scp
# ssh
# start
# stop
# upgrade
# url

Command.Machine = Machine