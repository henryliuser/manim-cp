import sys
ROOT = '/Users/henryliu/Desktop/'
sys.path += [ROOT+'abw/core', ROOT+'abw']
from core  import *
from manim import *

class TestArray(Scene):
    def construct(self):
        A = Array( [1,2,3,5,7,8,3] )
        self.play( Create(A) )
        self.wait(3)