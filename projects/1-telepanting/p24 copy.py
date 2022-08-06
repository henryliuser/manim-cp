from manim import *
from common import *
from core import *

class p24(Scene):  # TODO: change to ABWScene
    def construct(self):
        # ABWScene.rt_scale = 1e-5  # adjust me
        py = CodeBlock(
            code=src_py,
            tab_width=4,
            background_stroke_width=1,
            background_stroke_color=WHITE,
            insert_line_no=True,
            style="monokai",
            font="Monaco",
            font_size=13,
            line_spacing=1.2,
            language="py",
        ).to_corner(LEFT+DOWN, buff=0.75)

        ax = NumberLine(
            x_range=[0, 22],
            length=10,
            color=BLUE,
            z_index=-3,
            stroke_width=3
        )
        ant = Ant(ax=ax)
        N = 7
        X = [4, 7,10,13,15,19,21]
        Y = [1, 3, 2, 8,12, 5,11]
        S = [1, 1, 0, 1, 0, 0, 1]
        portals = createPortalsFrom(X,Y,S,ax)
        pobjs = [p.mob for p in portals]
        self.add(ax, ant.mob)
        self.add_foreground_mobject(ant.mob)
        fs = 80
        a = Tex('Newbie: ', font_size=fs, color=GRAY)
        a2 = Tex('1,000,000 years', font_size=fs,  color=WHITE)
        b = Tex('Grandmaster: ', font_size=fs,  color='#DB3024')
        b2 = Tex('2 seconds', font_size=fs,  color=WHITE)
        VGroup(a, a2).arrange(buff=.6).center().shift(1.3*DOWN)
        a2.shift(DOWN*.05)
        b.align_to(a, LEFT).shift(DOWN*2.4)
        b2.align_to(a2, RIGHT).shift(DOWN*2.4)
        self.add(a,b,a2,b2)
        self.add( *[p.mob for p in portals] )
        portal_arcs(self, portals)
        self.wait(2)

src_py = """
from bisect import *

def solve(N, X, Y, S):
    ans = 0
    ps = [0] * (N+1)
    for i in range(N):
        dist = X[i] - Y[i]
        j = bisect(X, Y[i])
        cost = ps[i] - ps[j]
        dp_i = cost + dist
        ps[i+1] = ps[i] + dp_i
        ans += S[i] * dp_i

    end = X[-1] + 1
    return ans + end

"""
