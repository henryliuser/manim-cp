from manim import *
from common import *
from core import *

# TODO: make the function grouping shit work
# TODO: either with function or with context manager, prefer latter
# TODO: `with Namespace(scene=self) as g1: `
# TODO: `    A, B, C = ...       `
# TODO:
# TODO: `g1.A  |  all_vmobs_in(g1)  |  ...`
class p24(Scene):
    def construct(self):
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
        Y = [2, 3, 2, 8,12, 5,11]
        S = [1, 1, 0, 1, 0, 0, 1]
        portals = createPortalsFrom(X,Y,S,ax)
        self.play( FadeIn(ax), Create(ant.mob) )
        self.add_foreground_mobject(ant.mob)
        self.play( *[FadeIn(p.mob) for p in portals] )

        s1a = VGroup( *all_vmobs_in(self) )
        s1b = s1a.copy().scale(0.75).to_edge(UP, buff=1)
        self.play( Transform(s1a, s1b) )

        SF = 0.75

        A = Array(X)
        A.mob.scale(SF)
        A.label = MathTex("X =").next_to(A.mob, LEFT)
        A.mob.add(A.label)
        A.mob.to_corner(DOWN+LEFT, buff=1).shift(2*UP+0.25*RIGHT)
        PS = Array( [0] )
        PS.mob.scale(SF).move_to(A(0), LEFT).shift(1.5*DOWN+SF*LEFT)
        PS.label = MathTex("ps =").next_to(PS(0), LEFT)
        PS.mob.add(PS.label)

        self.play( Create(A.mob), Create(PS.mob) )



        # e = Array.Element(value=12)
        # e2 = e.mob.copy().scale(SF).next_to(PS(0), RIGHT, buff=0)
        # self.play( Transform(e.mob,e2) )
        # PS += [e]

        ans = MathTex("ans = 0").to_edge(LEFT).shift(2*UP)
        self.play( Write(ans) )
        def update_ans(x, cur=[0]):  # static var
            cur[0] += x
            nans = MathTex(f"ans = {cur[0]}").move_to(ans)
            return Transform(ans, nans)

        pm = portal_map(portals)
        tf_show = lambda o : ScaleInPlace(o, 1.5, rate_func=flash)
        for x,y,s in zip(X,Y,S):
            pmobs = pm[x][0] + pm[y][0]
            self.bring_to_front(*pmobs)
            self.play( *map(tf_show, pmobs) )
            anim_bisect(self, A, y, 'j', RT=0.15, scale_factor=0.75)
            self.play( update_ans(y) )
            break

        self.wait(3)










src_py = """
from bisect import *

def solve(N, X, Y, S):
    cost = 0
    ps = [0] * (N+1) 
    for i in range(N):
        enter = X[i]
        exit = Y[i]
        j = bisect(X, exit)
        dist = enter - exit      
        penalty = ps[i] - ps[j]  
        dp_i = penalty + dist
        ps[i+1] = ps[i] + dp_i
        if S[i] == 1:   
            cost += dp_i

    end = X[-1] + 1
    return cost + end

"""

class p24b(Scene):
    def construct(self):
        py = CodeBlock(
            code=src_py,
            tab_width=4,
            background_stroke_width=1,
            background_stroke_color=WHITE,
            insert_line_no=True,
            style="monokai",
            font="Monaco",
            font_size=12,
            line_spacing=1.2,
            language="py",
        ).to_edge(LEFT).shift(DOWN)

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
        Y = [2, 3, 2, 8,12, 5,11]
        S = [1, 1, 0, 1, 0, 0, 1]
        portals = createPortalsFrom(X,Y,S,ax)
        self.play( FadeIn(ax), Create(ant.mob) )
        self.add_foreground_mobject(ant.mob)
        self.play( *[FadeIn(p.mob) for p in portals] )

        s1a = VGroup( *all_vmobs_in(self, exclude={py}) )
        s1b = s1a.copy().scale(0.75).to_corner(UP+RIGHT, buff=1)
        self.play( Transform(s1a, s1b) )
        self.play( Create(py) )

        SF = 0.5

        A = Array(X)
        A.mob.scale(SF)
        A.label = MathTex("X =").next_to(A.mob, LEFT)
        A.mob.add(A.label)
        A.mob.to_edge(DOWN).next_to(py, RIGHT, buff=1.5)
        # A.mob.to_corner(DOWN+LEFT, buff=1).shift(2*UP+0.25*RIGHT)
        PS = Array( [0] )
        PS.mob.scale(SF).move_to(A(0), LEFT).shift(1.5*DOWN+SF*LEFT)
        PS.label = MathTex("ps =").next_to(PS(0), LEFT)
        PS.mob.add(PS.label)

        self.play( Create(A.mob), Create(PS.mob) )



        # e = Array.Element(value=12)
        # e2 = e.mob.copy().scale(SF).next_to(PS(0), RIGHT, buff=0)
        # self.play( Transform(e.mob,e2) )
        # PS += [e]

        ans = MathTex("ans = 0").to_edge(LEFT).shift(3*UP)
        self.play( Write(ans) )
        def update_ans(x, cur=[0]):  # static var
            cur[0] += x
            nans = MathTex(f"ans = {cur[0]}").move_to(ans)
            return Transform(ans, nans)

        pm = portal_map(portals)
        def tf_hold(o):
            o.state = o.copy()
            return Transform(o, o.copy().scale(1.1).set_color(YELLOW))
        tf_revert = lambda o : Transform(o, o.state)
        tf_hlight = lambda o : Indicate(o, scale_factor=1.1)
        tf_show   = lambda o : ScaleInPlace(o, 1.5, rate_func=flash)

        for x,y,s in zip(X,Y,S):
            pmobs = pm[x][0] + pm[y][0]
            self.bring_to_front(*pmobs)
            self.play( *map(tf_show, pmobs) )
            anim_bisect(self, A, y, 'j', RT=0.15, scale_factor=0.75)
            self.play( update_ans(y), *map(tf_hlight, py[x%15:x%15+2]) )
            # show dist line, transform into dist_i val
            # slice dp_labels and show psum anim, transform into cost_i val
            # merge Transform dist_i, cost_i, into new ps val
            # play/hold/revert the right lines of py
            # change src_py to reflect ps.append()
            # change src_py to reflect `cost`

        self.wait(3)