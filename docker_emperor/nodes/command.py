from docker_emperor.utils import setdefaultdict


__all__ = ['Commands', 'CustomCommand']


class Commands(dict):

    def __new__(cls, *args, **kwargs):
        return dict.__new__(cls, *args, **kwargs)

    def __init__(self, data):
        super(self.__class__, self).__init__(setdefaultdict(data))
        for key, val in self.items(): 
            if isinstance(val, list):
                self[key] = CustomCommand_list(key, val)
            else:
                self[key] = CustomCommand_str(key, val)


    def __gt__(self, inst):
        if not isinstance(inst, self.__class__): return self
        return inst < self

    def __lt__(self, inst):
        if not isinstance(inst, self.__class__): return self
        for name, inst in inst.items(): 
            if not name in self:
                self[name] = inst.copy()
            else:
                self[name] < inst
        return self

    def __iter__(self):
        for name, inst in self.items(): 
            yield inst

    def __repr__(self):
        return '<{}> \r\n\t - {}'.format(self.__class__.__name__, "\r\n\t - ".join([repr(a) for a in self ]))

    def copy(self):
        return self.__class__(dict(self))


class CustomCommand():

    def __gt__(self, inst):
        if not isinstance(inst, self.__class__): return self
        return inst < self

    def __lt__(self, inst):
        if not isinstance(inst, self.__class__): return self
        # self.__init__(self.name, combine(inst, self))
        return self

    def __repr__(self):
        return '{}: {}'.format(self.name, self.data)

    def copy(self):
        return self#.__class__(self.name, self.data)


class CustomCommand_str(CustomCommand, str):

    def __new__(cls, value, *args, **kwargs):
        return str.__new__(cls, value)

    def __init__(self, name, data, *args, **kwargs):
        self.name = name
        self.data = data
        super(CustomCommand_str, self).__init__(data)

    @property
    def commands(self):
        return [self.data]


class CustomCommand_list(CustomCommand, list):

    def __new__(cls, value, *args, **kwargs):
        return list.__new__(cls, value, *args)

    def __init__(self, name, data, *args, **kwargs):
        self.name = name
        self.data = data
        super(CustomCommand_list, self).__init__(data)

    @property
    def commands(self):
        return self.data