import os
import six
from docker_emperor.nodes.environment import Environment
from docker_emperor.nodes.mounting import Mountings
from docker_emperor.nodes.command import Commands
from docker_emperor.nodes.compose import Compose 
from docker_emperor.commands import Command 
from docker_emperor.exceptions import DockerEmperorException
from docker_emperor.utils import setdefaultdict,  yamp_load
import docker_emperor.logger as logger


__all__ = ['Project']


class Project(dict):

    FILES = ['docker-emperor.yml', 'docker-compose.yml']

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)

    def __getitem__(self, key): 
        return self.get(key)

    def __init__(self, root):
        self.root = root
        super(Project, self).__init__(self.get_yml_data())
        for default_name, default_class in [
            ('environment', Environment),
            ('commands', Commands),
        ]:
            self[default_name] = default_class(self[default_name])  

        self['mounting'] = Mountings(self, self['mounting'])

        self.config = setdefaultdict(root.projects, self.name, {})
        self.config['workdir'] = os.path.abspath(self.root.root_path)

    def get_yml_data(self):
        for file in self.FILES:
            filename = os.path.join(self.root.root_path, file)
            if os.path.isfile(filename):
                data = yamp_load(open(filename, 'rb').read())
                if not isinstance(data, dict):
                    raise DockerEmperorException('{} is not yml as dict'.format(os.path.basename(file)))
                return data
        raise DockerEmperorException('{} not found in {}'.format(" or ".join(self.FILES), self.root.root_path))

    @property
    def name(self): 
        n = '__name'
        if not hasattr(self, n):
            setattr(self, n, self.pop('name',  
                self.pop('project_name',                       # default 0
                    self['environment'].get('COMPOSE_PROJECT_NAME',    # default 1
                        os.environ.get('COMPOSE_PROJECT_NAME',      # default 2
                            os.path.basename(self.root.root_path)   # default 3
                        )
                    )
                )
            ))
        return getattr(self, n)

    ''' 
    Run custom project defined commands
    '''
    def run_command(self, name, *args):
        commands = self['commands']
        commands < self.mounting['commands'] 

        print(commands)
        if name in commands:                    
            command = commands[name]
            logger.cmd('Run custom command <b>%s</b>' % (command.name, ))
            for line in command.commands:
                if line == name:
                    logger.error('Comand loop error: <b>%s</b>' % (line, ))
                else:
                    # TODO: Improve with @mounting detection and Split by | and < or >
                    if self.root.current_mounting and line.split()[-1][0] != '@':
                        local_args = tuple(args) + ('@%s' % self.root.current_mounting,)
                    else:
                        local_args = tuple(args)

                    for name, value in self.compose.environment:
                        line = line.replace('${%s}' % (name), value)

                    logger.cmd('Run %s %s' % (line, " ".join(local_args)))
                    cmd_args = tuple(line.split()) + local_args
                    cmd = self.root.bash(
                        'docker-emperor',
                        *cmd_args,
                        compose=self.compose,
                        is_system=True
                    )
                    if not cmd.is_success:
                        break
            return True
        return False


    @property
    def compose(self): 
        n = '__compose'
        if not hasattr(self, n):
            setattr(self, n, Compose(self.root))
        return getattr(self, n)

    @property
    def mounting(self):
        n = '__mounting'
        if not hasattr(self, n):
            if not self.root.current_mounting:
                self.root.current_mounting = 'localhost'
            mounting = self['mounting'][self.root.current_mounting]
            if not mounting:
                self.root.run_command('mount', internal=True)
                return self.mounting
            else:
                setattr(self, n, mounting)
        return getattr(self, n)