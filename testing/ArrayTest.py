from manim import *
from core  import *


class TestArray(Scene):
    def construct(self):
        A = Array( [1,2,3,5,7,8,3] )
        A.mob.center()
        self.play( Create(A.mob) )
        self.play( A[2].anim_set_val(5) )
        self.wait(1)
        self.play( A[2].anim_set_val(8) )
        self.wait(1)
        self.play( A[2].anim_set_val(1), A[1].anim_set_val(0) )
        self.wait(1)
        anim = [ A[i].anim_highlight(LIGHT_BROWN) for i in range(3) ]
        self.play( *anim )
        self.wait(1)
        ele, mob = A[1:4]
        self.play( mob.animate.shift(2*DOWN) )
        self.wait(3)

# env PYTHONPATH="/Users/henryliu/Desktop/manim-cp/" manim -pql testing/ArrayTest.py