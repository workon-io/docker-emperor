import six
import yaml
import uuid
try:
        # for python newer than 2.7
    from collections import OrderedDict
except ImportError:
        # use backport from pypi
    from ordereddict import OrderedDict
try:
    from yaml import CLoader as YamlLoader, CDumper as YamlDumper
except ImportError:
    from yaml import Loader as YamlLoader, Dumper as YamlDumper

_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG
dict_representer = lambda self, data: self.represent_mapping('tag:yaml.org,2002:map', data.items())
dict_constructor = lambda loader, node: OrderedDict(loader.construct_pairs(node))
YamlDumper.add_representer(OrderedDict, dict_representer) 
YamlLoader.add_constructor(_mapping_tag, dict_constructor)


__all__ = ['setdefaultdict', 'memoized_property', 'memoized', 'yamp_load', 'yamp_dump', 'yaml', 'OrderedDict' ]


def yamp_dump(data):
    return yaml.dump(data, Dumper=YamlDumper, default_flow_style=False, indent=4)

def yamp_load(content):
    return yaml.load(content, Loader=YamlLoader)


def setdefaultdict(_dict, name=None, default={}, ordered=False):
    if name:
        value = _dict.setdefault(name, default)
    else:
        value = _dict
    if not isinstance(value, dict): 
        if name:
            value = _dict[name] = default
        else:
            value = default
    if ordered:
        value = OrderedDict(value)
    return value


        
class memoized_property(object):


    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.__get = fget
        self.__set = fset
        self.__del = fdel
        self.__doc__ = doc
        self.___uuid = str(uuid.uuid1())
    
    def __get__(self, inst, cls=None): 
        if not hasattr(inst, self.___uuid):
            setattr(inst, self.___uuid, self.__get(inst))
        return getattr(inst, self.___uuid)


class memoized(object):

    def __init__(self, fct):
        self.___fct = fct
        self.___uuid = str(uuid.uuid1())

    def __get__(self, inst, cls=None):
        self.___inst = inst
        return self

    def __call__(self, inst, *args, **kwargs):        
        if not hasattr(inst, self.___uuid):
            setattr(inst, self.___uuid, self.___fct(inst, *args, **kwargs))
        return getattr(inst, self.___uuid)


def combine(elm1, elm2, *args):

    # elm1 is merge into elm2 with elm1 as the priority
    # elm2 < elm1

    # None - None
    if elm1 is None and elm2 is None:
        return None

    # None - str
    elif elm1 is None and isinstance(elm2, six.string_types):
        elm1 = elm2

    # None - dict
    elif elm1 is None and isinstance(elm2, dict):
        elm1 = elm2
        combine(elm1, elm2)

    # None - List
    elif elm1 is None and isinstance(elm2, list):
        elm1 = elm2
        combine(elm1, elm2)

    # Dict - Dict
    elif isinstance(elm1, dict) and isinstance(elm2, dict):
        for key2, val2 in elm2.items():
            val1 = elm1.get(key2, val2)
            elm1[key2] = combine(val1, val2)
            # if val1 is not None:
            #     elm1[key2] = val1


    # List - List
    elif isinstance(elm1, list) and isinstance(elm2, list):
        elm1 = list(set(elm2 + elm1))

    # List - None
    elif isinstance(elm1, list) and elm2 is None:
        for ind1, val1 in enumerate(elm1):
            elm1[ind1] = combine(ind1, None)

    # if isinstance(elm1, six.string_types) and elm1 in as_shortcuts:
    #     elm1 = as_shortcuts[elm1]

    if args:
        return combine(elm1, **args)
    else:
        return elm1
