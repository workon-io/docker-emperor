import os
import copy
from docker_emperor.utils import setdefaultdict, yaml


__all__ = ['Volumes', 'Volume']



class Volumes(dict):

    def __new__(cls, data, *args, **kwargs):
        return dict.__new__(cls, data, *args, **kwargs)

    def __init__(self, data, *args):
        super(Volumes, self).__init__(setdefaultdict(data, ordered=True))
        for key ,val in self.items():
            self[key] = Volume(key, val)
        for arg in args:
            self < arg

    def __gt__(self, inst):
        if not isinstance(inst, self.__class__): return self
        return inst < self

    def __lt__(self, inst):
        if not isinstance(inst, self.__class__): return self
        for key, val in inst.items():
            if not key in self:
                self[key] = val.copy()
            else:
                self[key] < val
        return self

    def __iter__(self):
        for name, service in self.items():
            yield service

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, super(dict, self).__repr__())


yaml.add_representer(Volumes, lambda dumper, data: dumper.represent_dict(data))


class Volume(dict):


    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __init__(self, name, data, *args):
        self.name = name
        super(self.__class__, self).__init__(setdefaultdict(data))
        for arg in args:
            self < arg

    def __getitem__(self, key): 
        return self.get(key)

    def __gt__(self, inst):
        if not isinstance(inst, self.__class__): return self
        return inst < self

    def __lt__(self, inst):
        if not isinstance(inst, self.__class__): return self
        for key, val in inst.items():
            if not key in self:
                self[key] = copy.deepcopy(val)
            else:
                if isinstance(self[key], dict) and isinstance(val, dict):
                    self[key].update(val)
                elif isinstance(self[key], list) and isinstance(val, list):
                    self[key] = list(set(self[key] + copy.deepcopy(val)))

        return self

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.name)
       
    def copy(self):
        return self.__class__(self.name, dict(self))
    


yaml.add_representer(Volume, lambda dumper, data: dumper.represent_dict(data))