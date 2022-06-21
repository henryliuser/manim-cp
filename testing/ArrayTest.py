import sys
ROOTS = ['/Users/henryliu/Desktop/manim-cp/', '/Users/samuelbrashears/PycharmProjects/manim-cp/']
for R in ROOTS: sys.path += [R, R+'core']
from core  import *
from manim import *

class TestArray(Scene):
    def construct(self):
        A = Array( [1,2,3,5,7,8,3] )
        self.play( Create(A) )
        self.wait(3)

# env PYTHONPATH="/Users/henryliu/Desktop/manim-cp/" manim -pql testing/ArrayTest.py