import numpy as np
from manim import *

# props:
# ant
# portal:
# axis:

# class Monitor(Text):
#     def __init__(self, *args, **kwargs):
#         Text.__init__(args, kwargs)
#         self.t = 0
#         if 't' in kwargs: 
#             self.t = kwargs['t']

from random import randint as rng
class Portal:
    DDR = DEFAULT_DOT_RADIUS
    def __init__(my, x, y, ax):
        r, g, b = rng(0,255), rng(0,255), rng(0,255)
        col = rgb_to_color([r/255,g/255,b/255])
        my.enter = x
        my.leave = y
        my.mobs = [
            Dot(radius=1.5*Portal.DDR, point=ax.n2p(x), color=col),
            Dot(radius=1.5*Portal.DDR, point=ax.n2p(y), color=col),
        ]

def shiftLeft(axi, axf):
    pass

def shiftRight(axi, axf):
    pass

# def update(ax, newX):
#     l,r = ax.x_range
#     dx 
#     axf = NumberLine(
#         x_range = [newX]
#     )

"""
ok, idea is to have a like 20 
of these numberlines in the scene at once,
and only place the current one within frame?
then, for the later big scene, we zoom out and do a transformation
"""
class Test(Scene):
    def construct(self):
        ax = NumberLine(
            x_range = [0,10],
            length  = 11,
            color   = BLUE,
            include_numbers = True
        )
        ax.shift(2*DOWN)
        ax2 = NumberLine(
            x_range = [10,20],
            length  = 11,
            color   = BLUE,
            include_numbers = True
        )
        # ax2.shift(2*OUT)
        # raise ValueError(ax2.get_z())
        ant = Dot(point=ax.n2p(0), color=YELLOW)
        # x = ax.n2p(2) + [0,0,1]
        # raise ValueError(x)
        z2 = DecimalNumber(ax2.get_z(), num_decimal_places=2)
        za = DecimalNumber(ant.get_z(), num_decimal_places=2)
        always(za.next_to, ant, UP)
        z2.to_edge(UP)
        f_always(za.set_value, ant.get_z)
        f_always(z2.set_value, ax2.get_z)
        
        v = 9
        ax2.shift(2*DOWN + v*RIGHT)
        self.play( Create(ax), Create(ant), Create(za), Create(z2) )
        self.play( ant.animate.move_to(ax.n2p(6)) )
        
        ant.set_z_index(1)  # wtf ????
        ax2.set_z_index(0)
        tgt = ax.n2p(2)
        c = ax.get_center()
        
        self.play( 
            FadeOut(ax, shift=v*LEFT+2*LEFT),
            FadeIn(ax2),
            # ax2.animate.shift(v*LEFT),
            ax2.animate.move_to(c),
            ant.animate.move_to(tgt),
        )
        self.wait(2)



class Test2(MovingCameraScene):
    def construct(self):
        ax = NumberLine(
            x_range = [0,10],
            length  = 11,
            color   = BLUE,
            include_numbers = True
        )
        ax.shift(2*DOWN)
        ax2 = NumberLine(
            x_range = [0,30],
            length  = 31,
            color   = BLUE,
            include_numbers = True,
        )
        ax2.shift(2*DOWN)
        self.play( Create(ax) )
        self.play( 
            ReplacementTransform(ax, ax2),
            self.camera.frame.animate.set(width=45)
        )
        self.wait(3)



class Main(Scene):
    def construct(self):
        # setup
        title = Text('"Telepanting"')
        title.to_edge(UP)
        ax = NumberLine(
            x_range = [0,10],
            length  = 11,
            color   = BLUE,
            include_numbers = True
        )
        ax.shift(2*DOWN)
        ant = Dot(point=ax.n2p(0), color=YELLOW)

        t = 0
        t_tex, t_val = t_label = VGroup(
            Tex(r't = '),
            Integer(0)
        )
        t_label.arrange(RIGHT)

        def tick():
            nonlocal t 
            t += 1
            self.play(
                ApplyWave(t_tex, run_time=1),
                ApplyWave(t_val, run_time=1),
                t_val.animate.set_value(t),
                ant.animate.move_to( ax.n2p(t) ),
            )

        # intro
        self.play( FadeIn(title) )
        self.wait(1)
        self.play( FadeIn(ax), FadeOut(title), run_time=1 )
        self.wait(1)
        self.play( FadeIn(ant), run_time=1 )
        self.wait(2)

        # moving
        self.play( Write(t_label) )
        self.wait(2)  # each second, it crawls forward...
        for _ in range(5):
            tick()
            self.wait(1.5)
        self.wait(3)  # but to its surprise...

        portals = []
        # ddr = DEFAULT_DOT_RADIUS
        portals = [  ]
        portals += [ Portal(7,3,ax) ]
        portals += [ Portal(8,6,ax) ]
        portals += [ Portal(4,2,ax) ]
        for p in portals:
            self.play( *map(FadeIn, p.mobs), run_time=1 )
                
        

        
