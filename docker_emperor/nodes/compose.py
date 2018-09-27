import six
import os
from docker_emperor.commands import Command
from docker_emperor.nodes.environment import Environment
from docker_emperor.nodes.mounting import Mountings
from docker_emperor.nodes.service import Services
from docker_emperor.nodes.volume import Volumes
from docker_emperor.utils import yamp_dump, yaml


__all__ = ['Compose']

''' 
Compose stack Context + Machine 
Combine services & environment vars
'''

class Compose(dict):


    NODES = [
        'services', 
        'volumes', 
        'networks', 
        'version', 
        'configs', 
        'secrets', 
        'deploy'
    ]

    NOT_NODES = [
        'name', 
        'environment', 
        'commands', 
        'mounting'
    ]

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __repr__(self):
        return '<%s: %s>'.format(self.__class__.__name__, self.name) 

    def __getitem__(self, key): 
        return self.get(key)

    def __init__(self, root, docker_compose_bin="docker-compose"):

        self.root = root
        self.project = self.root.project  
        self.mounting = self.project.mounting
        self.name = self.mounting.docker_machine_name
        self.filename = os.path.join(self.root.root_path, 'docker-compose.%s.yml' % self.name)
        data = dict(self.project)
        for node_name, node in data.items():
            if node_name in Compose.NOT_NODES:
                data.pop(node_name)
        super(Compose, self).__init__(data)
        for default_name, default_class in [
            ('services', Services),
            ('volumes', Volumes),
        ]:
            self[default_name] = default_class(self[default_name])

        self.environment = self.project['environment'].copy()

        self['services'] < self.mounting['services'] 
        self['volumes'] < self.mounting['volumes'] 
        self.environment < self.mounting['environment'] 

        self.environment['DOCKER_EMPEROR_HOSTS'] = " ".join([
            host.strip() for host in self.mounting['hosts']    
        ])
        self.environment['DOCKER_EMPEROR_ENVIRONMENT']  = " ".join(self.environment.list)

        self.bin = "%s -f %s" % (docker_compose_bin, self.filename)
        #self.bin = "%s -f %s --project-directory=%s" % (path, self.filename, self.mounting['workdir'])
        # '--project-directory=.',

        for service in self['services']:

            service['environment'] < self.environment
            service['container_name'] = service.get('container_name', '%s.%s' % (self.name, service.name))
            if not 'image' in service and not 'build' in service:
                if os.path.isfile(os.path.join(self.root.root_path, service.name, 'Dockerfile')):
                    service['image'] =  '%s.%s' % (self.project.name, service.name)
                    service['build'] = service.name
                else:
                    service['image'] = service.name
            else:
                if 'image' in service:
                    if os.path.isfile(os.path.join(self.root.root_path, service['image'], 'Dockerfile')):
                        service_name = service['image']
                        service['image'] = '%s.%s' % (self.project.name, service_name)
                        service['build'] = service_name

            if not self.mounting.is_localhost:
                if 'volumes' in service:

                    new_volumes = []
                    for volume in service['volumes']:
                        # print(volume)

                        volume = volume.strip()
                        if volume.startswith('./'):
                            volume = self.mounting['workdir'] + volume[2:]
                            new_volumes.append(volume)
                        else:
                            new_volumes.append(volume)
                    service['volumes'] = new_volumes





        file = open(self.filename, 'wb')# = tempfile.NamedTemporaryFile(mode='w+b', bufsize=-1, suffix='.yml', prefix='docker-compose-', dir=None, delete=False)
        yml = yamp_dump(self)
        for name, value in self.environment:
            yml = yml.replace('${%s}' % (name), value)
        file.write(yml)
        file.close()

    def copy(self):
        return self.__class__(dict(self))
 
yaml.add_representer(Compose, lambda dumper, data: dumper.represent_dict(data))


Command.Compose = Compose