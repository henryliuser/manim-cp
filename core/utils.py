from manim import *
from core.aliases import *
from core.cursed import *
import inspect

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
        return self.__dict__.values().__iter__()

class ABWScene(Scene):
    rt_scale = 1
    def play(*args, **kwargs):
        rt  = kwargs.pop("run_time", 1) * ABWScene.rt_scale
        for anim in args:
            if hasattr(anim, "run_time"):
                anim.run_time *= ABWScene.rt_scale
        Scene.play( *args, run_time=rt, **kwargs)

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

def Peek(mob, duration=1):
    return FadeIn(mob, rate_func=flash, run_time=duration)

def getCorners(mob : Mobject):
    return mob.get_corner(DOWN+LEFT), \
           mob.get_corner(UP+RIGHT)

def getBoundingBox(mob : Mobject, opacity=0.5):
    bl, tr = getCorners(mob)
    dim = tr - bl
    mid = midpoint(bl, tr)
    return Rectangle(
        fill_opacity=opacity,
        fill_color=PINK,
        color=RED,
        width=dim[0],
        height=dim[1],
        z_index=1000,
    ).move_to(mid)

def width(mob : Mobject):
    bl, tr = getCorners(mob)
    return (tr-bl)[0]

def height(mob : Mobject):
    bl, tr = getCorners(mob)
    return (tr-bl)[1]

def intersectingArea(A,B,C,D,E,F,G,H):
    return max(min(C,G)-max(A,E), 0)*max(min(D,H)-max(B,F), 0)

# use dbug() the same way you'd use print
class DEBUG(Exception): pass
def dbug(*args, **kwargs):
    res = map(repr, args)
    sep = kwargs.pop('sep', ', ')
    end = kwargs.pop('end', '\n')
    raise DEBUG(sep.join(res) + end)

class CodeBlock(Code):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.lines = [None] + self.code.lines[0]


    # @return y-coord of the i-th line of code
    def __call__(self, i):
        line = self.lines[i]
        xc = line.get_corner(UP+RIGHT)[0]
        if i == 0: return xc, line.get_center()[1]
        bl, tr = getCorners(line)
        if (tr-bl)[1] < 1e-2: raise ValueError("empty line")
        for j in range(i+1, len(self.lines)):
            if height( self.lines[j] ) > 1e-2:
                break
        nxtl = self.lines[j]
        b0 = [ x for y in getCorners(nxtl) for x in y[:2] ]
        b1 = [ x for y in getCorners(line) for x in y[:2] ]

        if intersectingArea(*b0, *b1) < 1e-3:
            return xc, line.get_center()[1]

        return nxtl.get_corner(UP+RIGHT), nxtl.get_corner(UP+RIGHT)[1]

    def __getitem__(self, i):
        return self.lines[i]

def all_vmobs_in(group, exclude=set(), pred=lambda o : True):
    if    isinstance(group, Scene):   it = group.mobjects
    elif  isinstance(group, Mobject): it = group.submobjects
    elif  isinstance(group, Proxy):   it = group.__dict__.values()
    else: it = group.__iter__() 

    ok = lambda o : o != None and isinstance(o, VMobject) and (o not in exclude)    
    return [o for o in it if ok(o) and pred(o)]

def ScaleAndMove(mob, scale_factor, target=None):
    if target is None:
        target = mob.target
    temp_mob = mob.copy()
    temp_mob.move_to(target).scale(scale_factor)
    return Transform(mob, temp_mob)

def Move(mob, target):
    temp_mob = mob.copy()
    temp_mob.move_to(target)
    return Transform(mob, temp_mob)

FadeInMany  = lambda *o : map(FadeIn, o)
FadeOutMany = lambda *o : map(FadeOut, o)

def all_pairs(N):
    res = []
    for i in range(N-1):
        for j in range(i+1, N):
            res += [ (i,j) ]
    return res

Hori = lambda length : Rectangle(width=length, height=0.02, fill_opacity=1, fill_color=WHITE)
Vert = lambda length : Rectangle(width=0.02, height=length, fill_opacity=1, fill_color=WHITE)

# align x to y by dirs
def align_corner(x, y, *dirs):
    for d in dirs:
        x.align_to(y, d)
    return x 


center    = lambda a,b : VGroup(a,b).get_center()
TOP_MID   = Dot().to_edge(UP, buff=0)
TOP_LEFT  = Dot().to_corner(UP+LEFT, buff=0)
TOP_RIGHT = Dot().to_corner(UP+RIGHT, buff=0)
MID_MID   = Dot()
MID_LEFT  = Dot().to_edge(LEFT, buff=0)
MID_RIGHT = Dot().to_edge(RIGHT, buff=0)
BOT_MID   = Dot().to_edge(DOWN, buff=0)
BOT_LEFT  = Dot().to_edge(DOWN+LEFT, buff=0)
BOT_RIGHT = Dot().to_edge(DOWN+RIGHT, buff=0)

def Fade(mob, start=None, end=None):
    def FadeInTo(mob, start, end):
        length = 1/(end - start)
        a = 0-length*start
        b = a + length
        rf = squish_rate_func(linear, a, b)
        return FadeIn(mob, rate_func=rf)
    def FadeOutTo(mob, opacity):
        new_mob = mob.copy()
        new_mob.fade(1-opacity)
        return Transform(mob, new_mob)
    if start < end:
        return FadeInTo(mob, start, end)
    else:
        return FadeOutTo(mob, end/start)
