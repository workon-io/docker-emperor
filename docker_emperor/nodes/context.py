import six
from docker_emperor.nodes.environment import Environment
from docker_emperor.nodes.service import Services
from docker_emperor.nodes.command import Commands
from docker_emperor.utils import setdefaultdict, combine, memoized_property, memoized, OrderedDict


__all__ = ['Contexts', 'Context']



class Contexts(dict):

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __init__(self, data):
        super(Contexts, self).__init__(OrderedDict(setdefaultdict(data)))
        for key, val in self.items():
            self[key] = Context(key, val)
        # else:
        #     self['default'] = Context('default')

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


class Context(dict):

    COMMANDS = [
    ]

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __init__(self, name, data=dict()):
        self.name = name
        super(Context, self).__init__(setdefaultdict(data))
        for default_name, default_class in [
            ('environment', Environment),
            ('services', Services),
            ('commands', Commands),
        ]:
            self[default_name] = default_class(self[default_name])
        
    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)

    def __getitem__(self, key): 
        return self.get(key)
