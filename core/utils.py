class Props:
    def __init__(self, namespace, toRegister):
        for k,v in namespace.items():
            if k in toRegister:
                self.__dict__[k] = v

def initWithDefaults(obj, default_map, **kwargs):
    for k,v in default_map:
        if k in kwargs:
            obj.__dict__[k] = kwargs[k]
        else:
            obj.__dict__[k] = v
