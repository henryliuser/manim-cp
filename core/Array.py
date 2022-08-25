from manim import *
from core import *
from copy import deepcopy
from core.utils import *


class Array(ABWComponent):
    class Element(ABWComponent):
        def __init__(self, **kwargs):
            props = {
                "outline_color": DARKER_GRAY,
                "value_color": WHITE,
                "color": "#005400",
                "height": 1,
                "width": 1,
                "stroke_width": 5,
                "value": 0,
                "scale": 1,
            }
            my = self.props = Namespace(props, kwargs)
            my.height *= my.scale
            my.width *= my.scale
            my.stroke_width *= my.scale
            s = my.height - my.stroke_width / 100
            mobs = {
                "fill":
                    Rectangle(height=s, width=s,
                              stroke_width=0, color=my.color,
                              fill_opacity=1),
                "border":
                    Rectangle(height=my.height, width=my.width)
                .set_stroke(my.outline_color, my.stroke_width, 1),
            }
            if isinstance(my.value, int):
                mobs["tex"] = Tex(my.value).scale(my.scale)
            elif my.value is not None:
                mobs["val"] = my.value.scale(my.scale)
            super().__init__(my, mobs, kwargs)

        def anim_set_val(self, val):
            self.props.value = val
            tf = Tex(str(val)).move_to(self.mobs.tex)
            res = Transform(self.mobs.tex, tf)
            return res

        def anim_highlight(self, col, **kwargs):
            f = self.mobs.fill
            self.props.cell_color = col
            return FadeToColor(f, col, **kwargs)

    def __init__(self, A, scale=1, **kwargs):
        if scale == 0:
            scale = 6 / len(A)
        props = {
            "N": len(A),
            "arr": [],
        }
        self.og = A
        my = self.props = Namespace(props, kwargs)
        my.arr = [Array.Element(value=x, scale=scale, **kwargs) for x in A]
        # align the cells next to each other
        mobs = {i: self(i) for i in range(my.N)}
        for i in range(1, my.N):
            self(i).next_to(self(i-1), RIGHT, buff=0)

        super().__init__(my, mobs, kwargs)
        self.mob.center()

    def append(self, x):
        if isinstance(x, Array.Element):
            self.og += [x.props.value]
            return self.props.arr.append(x)

        self.og += [x]
        e = Array.Element(value=x)
        self.props.arr += [e]

    def __iadd__(self, x):
        self.append(x)

    def __call__(self, i):  # exposes the i-th Array.Element.mob
        return self.props.arr[i].mob

    def __getitem__(self, i):  # exposes the i-th Array.Element
        if isinstance(i, slice):
            start = i.start if i.start != None else 0
            stop = i.stop if i.stop != None else self.props.N
            step = i.step if i.step != None else 1
            ele, mob = [], VGroup()
            for j in range(start, stop, step):
                e = deepcopy(self[j])
                ele += [e]
                mob.add(e.mob)
            return ele, mob

        return self.props.arr[i]
