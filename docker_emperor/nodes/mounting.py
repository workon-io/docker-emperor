import six
from docker_emperor.commands import Command
from docker_emperor.nodes.environment import Environment
from docker_emperor.nodes.service import Services
from docker_emperor.nodes.command import Commands
from docker_emperor.nodes.volume import Volumes
from docker_emperor.utils import setdefaultdict, combine, memoized_property, memoized, OrderedDict


__all__ = ['Mountings', 'Mounting']



class Mountings(dict):

    DEFAULT = {
        'localhost': {}
    }

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __init__(self, project, data):
        self.project = project
        super(Mountings, self).__init__(OrderedDict(setdefaultdict(data)))
        if self:
            for key, val in self.items():
                self[key] = Mounting(self.project, key, val)
        else:
            self['localhost'] = Mounting(self.project, 'localhost')

    def __iter__(self):
        for key, val in self.items():
            yield val

    def __repr__(self): 
        return ", ".join(str(c) for c in self)

    def __getitem__(self, i):
        if isinstance(i, int):
            return [c for c in self][i]
        else:
            return self.get(i, None)


class Mounting(dict):

    COMMANDS = [
    ]
    LOCAL_MACHINE_WARNING = 'You are already on a local machine'

    class Drivers(object):
        LOCALHOST = 'localhost'
        GENERIC_LOCALHOST = 'generic --generic-ip-address localhost'  

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __init__(self, project, name, data=dict(), docker_machine_bin="docker-machine"):
        self.project = project
        self.name = name
        self.docker_machine_name = '%s.%s' % (self.project.name, self.name)
        self.docker_machine_bin = docker_machine_bin
        super(Mounting, self).__init__(setdefaultdict(data))
        for default_name, default_class in [
            ('environment', Environment),
            ('services', Services),
            ('commands', Commands),
            ('volumes', Volumes),
        ]:
            self[default_name] = default_class(self[default_name])
        
        if not isinstance(self['driver'], six.string_types): 
            self['driver'] = Mounting.Drivers.LOCALHOST
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
        cmd = Command(self.docker_machine_bin, *args, **kwargs)
        cmd.run()
        return cmd

    def get_machine_hosts(self): 
        hosts = [] 
        for host in self['hosts']: 
            hosts.append(self.apply_env(host))    
        return hosts

    def get_machine_driver(self):      
        return self.apply_env(self['driver'])

    def apply_env(self, s):
        for k, v in self['environment']:
            s = s.replace('${%s}' % (k, ), v)
        return s

    @property
    def is_localhost(self):
        return self['driver'] == Mounting.Drivers.LOCALHOST

    @property
    def is_generic(self):
        return self['driver'].startswith('generic')

    @property
    def exists(self):
        cmd = self._run("ls", "--filter", "NAME=" + self.docker_machine_name, "--format", "{{.Name}}", machine=self, tty=False)
        for line in cmd.lines:
            if line == self.docker_machine_name:return True
        return False

    @property
    def docker_env(self):
        n = '__docker_env'
        if not hasattr(self, n):
            if self.is_localhost:
                env = []
            else:
                cmd = self.bash('env', self.docker_machine_name)
                starts = 'export '
                env = [line.lstrip(starts) for line in cmd.lines if line.startswith(starts)]
            setattr(self, n, env)
        return getattr(self, n)

    def start(self):
        if self.is_localhost:
            if not self.is_running:
                self.bash('start', self.docker_machine_name, sys=True).run().log()  
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
            return self.bash('status', self.docker_machine_name).out
    
    @property
    def ip(self):
        if self.is_localhost:
            return '0.0.0.0'
        else:
            return self.bash('ip', self.docker_machine_name, log=False, machine=self).out.strip()

    @property
    def pwd(self):
        return self.bash('ssh', self.docker_machine_name, 'pwd', log=False, machine=self).out.strip()

    @property
    def inspect(self):
        return self.bash('inspect', self.docker_machine_name, machine=self, tty=False).out

    @property
    def active(self):
        return self.bash('active', machine=self, tty=False).out

    def remove(self):
        return self.bash('rm', self.docker_machine_name, machine=self)

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

Command.Mounting = Mounting