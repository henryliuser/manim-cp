from manim import *
from core import *
from copy import deepcopy

class Grid(ABWComponent):
    def __init__(self, A, scale=0, **kwargs):
        if scale == 0:
            scale = 6 / len(A)
        props = {
            "ny": len(A[0]),
            "nx": len(A),
            "arr": [Array(x, scale=scale) for x in A]
        }
        self.og = A
        my = self.props = Namespace(props, kwargs)
        mobs =  {i:self(i) for i in range(my.nx)}
        for i in range(1, my.nx):
            self(i).next_to(self(i-1), DOWN, buff=0)
        super().__init__(my, mobs, kwargs)
        self.mob.center()

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