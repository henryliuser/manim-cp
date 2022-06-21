from manim import *

class Main(Scene):
    def construct(self):
        ti = Tex("123")
        tf = Tex("42")
        self.play( Write(ti) )
        self.wait(1)
        self.play( Transform(ti, tf) )
        self.wait(1)