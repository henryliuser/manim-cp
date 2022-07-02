from manim import *
from core import *
from copy import deepcopy

# all ABW structures will optionally take a scene
class Array(ABWComponent):
    class Element(ABWComponent):
        def __init__(self, **kwargs):
            props = {
                "outline_color" : BLUE,
                "value_color"   : WHITE,
                "cell_color"    : BLACK,
                "height"        : 1,
                "width"         : 1,
                "stroke_width"  : 5,
                "value"         : 0,
            }
            my = self.props = Namespace(props, kwargs)
            mobs =  {
                "fill"   :
                    Rectangle(height=.98, width=0.98, color=my.cell_color)
                        .set_fill(my.cell_color, opacity=0.7),

                "border" :
                    Rectangle(height=my.height, width=my.width)
                        .set_stroke(BLUE, my.stroke_width, 1),

                "tex"    : Tex(my.value),
            }
            super().__init__(my, mobs, kwargs)

        def anim_set_val(self, val):
            self.props.value = val
            tf = Tex( str(val) ).move_to(self.mobs.tex)
            res = Transform(self.mobs.tex, tf)
            return res

        def anim_highlight(self, col, **kwargs):
            f = self.mobs.fill
            self.props.cell_color = col
            return FadeToColor(f, col, **kwargs)

    def __init__(self, A, **kwargs):
        props = {
            "N"   : len(A),
            "arr" : [ Array.Element(value=x) for x in A ],
        }
        self.og = A
        my = self.props = Namespace(props, kwargs)

        # align the cells next to each other
        mobs = { i:self(i) for i in range(my.N) }
        for i in range(1, my.N):
            self(i).next_to(self(i-1), RIGHT, buff=0)

        super().__init__(my, mobs, kwargs)
        self.mob.center()

    def __call__(self, i):  # exposes the i-th Array.Element.mob
        return self.props.arr[i].mob

    def __getitem__(self, i):  # exposes the i-th Array.Element
        if isinstance(i, slice):
            start = i.start if i.start != None else 0
            stop  = i.stop  if i.stop  != None else self.props.N
            step  = i.step  if i.step  != None else 1
            ele, mob = [], VGroup()
            for j in range(start, stop, step):
                e = deepcopy(self[j])
                ele += [e]
                mob.add(e.mob)
            return ele, mob

        return self.props.arr[i]