from manim import *
from core import *
from copy import deepcopy

class Grid(ABWComponent):
    def __init__(self, A, scale=0, **kwargs):
        if scale == 0:
            scale = 4 / len(A)
        props = {
            "ny": len(A[0]),
            "nx": len(A),
            "arr": [Array(x, scale=scale) for x in A],
            "scale": scale,
        }
        self.og = A
        my = self.props = Namespace(props, kwargs)
        mobs =  {i:self(i) for i in range(my.nx)}
        for i in range(1, my.nx):
            self(i).next_to(self(i-1), DOWN, buff=0)
        super().__init__(my, mobs, kwargs)
        self.mob.center()

    def make_axes(self):
        my = self.props
        x_axis = []
        y_axis = []
        for i in range(my.ny):
            y_axis.append(Integer(i))
            y_axis[-1].move_to(my.arr[0][i].mob)
            y_axis[-1].shift(UP*my.arr[0][0].props.height*.75)
            y_axis[-1].scale(my.scale)

        for i in range(my.nx):
            x_axis.append(Integer(i))
            x_axis[-1].move_to(my.arr[i][0].mob)
            x_axis[-1].shift(LEFT*my.arr[0][0].props.height*.75)
            x_axis[-1].scale(my.scale)

        ms = self.mobs

        ms.x_axis = VGroup(*x_axis)
        ms.y_axis = VGroup(*y_axis)
        ms.axes = VGroup(ms.y_axis, ms.x_axis)
        self.mob.add(ms.x_axis)
        self.mob.add(ms.y_axis)
        self.mob.add(ms.axes)

        my.y_axis = y_axis
        my.x_axis = x_axis

        return self.mobs.axes



    def sub_grid(self, x1, y1, x2, y2):
        a = self[x1][y1]
        b = self[x2][y2]

        if a is b:
            temp = a.mob
        else:
            temp = VGroup(a.mob, b.mob)

        h = a.props.width*(abs(x1-x2) + 1)
        w = a.props.height*(abs(y1-y2) + 1)
        c = Rectangle(width=w,height=h,
                      stroke_width=a.props.stroke_width, color=YELLOW)
        c.move_to(temp.get_center())
        return c

    def cells_in_rect(self, x1, y1, x2, y2):
        res = []
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                res.append((x, y, self[x][y]))
        return res

    def highlight_region(self, x1, y1, x2, y2, color=BLACK):
        cells = []
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                cells.append(self[x][y])
        return [c.anim_highlight(color) for c in cells]

    def remove_highlights(self):
        coords = (0, 0, self.props.nx - 1, self.props.ny - 1)
        return self.highlight_region(*coords, color=BLACK)

    def append(self, x):
        if isinstance(x, Array):
            self.og += [x.props.value]
            return self.props.arr.append(x)

        self.og += [x]
        e = Array(x)
        self.props.arr += [e]

    def __iadd__(self, x):
        self.append(x)

    def __call__(self, i):
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