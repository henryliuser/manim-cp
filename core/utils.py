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
        self.mob = VGroup( *self.mobs.__dict__.values() )


class StyleText(MarkupText):
    def __init__(self, text, **kwargs):
        t = [r'<span', text, '</span>']
        mp = {
                 "bold" : 'font-weight="bold"',
            "underline" : 'underline="single"',
               "italic" : 'font-style="italic"',
        }
        for k,v in mp.items():
            if k not in kwargs: continue
            t[0] += f' {v} '
            kwargs.pop(k)
        t[0] += '>'
        super().__init__( ''.join(t) , **kwargs)

class Mono(MarkupText):
    def __init__(self, text, **kwargs):
        t = ['<span font_family="monaco" font-size="xx-small">', text, '</span>']
        super().__init__( ''.join(t), **kwargs )

def flash(scene, mob, duration):
    scene.play( Create(mob) )
    scene.wait(duration)
    scene.play( FadeOut(mob) )

