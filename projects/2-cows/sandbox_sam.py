from telnetlib import DO
from manim import *
from core import *
from common import *

class sandbox_sam(Scene):
    def construct(self):



        
        c = Dot(radius=1)
        self.play(Fade(c, .25, .75))
        self.play(Fade(c, .75, .1))
        # e = Dot(radius=1).fade(0)
        # self.play(Transform(c, d))
        # self.play(Transform(c, e))
        # self.play(c.animate.fade(.5))
        # self.play(c.animate.fade(.5))
        # self.play(c.animate.fade(.5))

        # self.play(FadeInTo(c, 0, .25))
        # P(self)
        # self.play(FadeInTo(c, 0, 1))
        # self.play(FadeOutTo(c, 1, .5))
        # self.add(c)
        # P(self)
        # self.play(FadeInTo(c, .5, 1))
        # P(self)
