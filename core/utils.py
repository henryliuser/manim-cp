from manim import *
class Props:
    def __init__(self, namespace, toRegister):
        for k,v in namespace.items():
            if k in toRegister:
                self.__dict__[k] = v

class Namespace:
    def __init__(self, default, kwargs):
        to_pop = []  # consume the kwargs we use
        for k,v in default.items():
            if k in kwargs:
                self.__dict__[k] = kwargs[k]
                to_pop += [k]
            else:
                self.__dict__[k] = v
        for k in to_pop:
            kwargs.pop(k)
    def __iter__(self):
        return self.__dict__.items().__iter__()

# class ABWComponent:
#     def __init__(self, props, mobs, kwargs):
#         self.props = Namespace(eval(props.strip()), kwargs)
#         for k,v in self.props: exec(f"{k} = {repr(v)}")
#         self.mobs = Namespace(eval(mobs.strip()), kwargs)
#         self.mob = VGroup()
#         self.mob.add( *self.mobs.__dict__.values() )

class ABWComponent:
    def __init__(self, props, mobs, kwargs):
        self.props = props
        self.mobs = Namespace(mobs, kwargs)
        self.mob = VGroup()
        self.mob.add( *self.mobs.__dict__.values() )
