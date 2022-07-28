from manim import *
from common import *
from core import *
from core.PrefixSum import anim_psum_query1

# TODO: make the function grouping shit work
# TODO: either with function or with context manager, prefer latter
# TODO: `with Namespace(scene=self) as g1: `
# TODO: `    A, B, C = ...       `
# TODO:
# TODO: `g1.A  |  all_vmobs_in(g1)  |  ...`

# TODO: NAIL IT
# TODO: position elements
# TODO: highlight code snippets
# TODO: psum anim
# TODO: make clearer the conversion to dp_i then to ps[-1]
# TODO: ant fades, portal fades (fade all but pm[i])
# TODO: fix 0 shows up before 'ans = '

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
        self.play( FadeIn(ax), Create(ant.mob) )
        self.add_foreground_mobject(ant.mob)
        self.play( *[FadeIn(p.mob) for p in portals] )

        s1a = VGroup( *all_vmobs_in(self, exclude={py}) )
        s1b = s1a.copy().scale(0.75).to_corner(UP+RIGHT, buff=1)
        self.play( Transform(s1a, s1b) )
        self.play( Create(py) )

        SF = 0.6

        A = Array(X)
        A.mob.scale(SF)
        A.label = MathTex("X =").next_to(A.mob, LEFT)
        A.mob.add(A.label)
        A.mob.next_to(py, RIGHT, buff=1.5).shift(0.75*DOWN)

        DP = Array( [''] * N )
        DP.mob.scale(SF).move_to(A(0), LEFT).shift(.85*DOWN)
        DP.label = MathTex("dp =").next_to(DP.mob, LEFT)
        DP.mob.add(DP.label)

        PS = Array( [0] )
        PS.mob.scale(SF).move_to(A(0), LEFT).shift(1.7*DOWN+SF*LEFT)
        PS.label = MathTex("ps =").next_to(PS(0), LEFT)
        PS.mob.add(PS.label)

        self.play( Create(A.mob), Create(PS.mob), Create(DP.mob) )

        # solution
        ps = [0]

        # components
        i = 0  # portal index
        labs = [MathTex('0',font_size=1).move_to(p.mobs.entrance.get_center()+1/2*UP) for p in portals]  # portal dp labels
        pm = portal_map(portals)
        ans = Timer(label='ans = ')
        ans.mob.to_corner(UP+LEFT, buff=1).shift(0.75*RIGHT)

        # math terms
        dp_i = MathTex("dp_i")
        math_eq = MathTex("=").next_to(dp_i)
        dist_ul = Line(LEFT,ORIGIN).next_to(math_eq).shift(1/3*DOWN)
        math_pl = MathTex("+").next_to(dist_ul).set_y( dp_i.get_y() )
        cost_ul = Line(LEFT,ORIGIN).next_to(math_pl).shift(1/3*DOWN)
        dist_lab = MathTex("dist_i").next_to(dist_ul, DOWN)
        cost_lab = MathTex("cost_i").next_to(cost_ul, DOWN)
        eq = VGroup(dp_i, math_eq, dist_ul, math_pl, cost_ul).next_to(ax, 5*DOWN)

        # helpers
        def tf_hold(o):
            o.state = o.copy()
            return Transform(o, o.copy().scale(1.3).set_color(YELLOW))
        grab      = lambda i : (X[i], Y[i], S[i], i+1)
        tf_revert = lambda o : Transform(o, o.state)
        tf_hlight = lambda o : Indicate(o, scale_factor=1.2)
        tf_show   = lambda o : ScaleInPlace(o, 1.5, rate_func=flash)
        step = lambda rt,ind : simulate(self, ant, portals, ax, indi=ind, run_time=rt,
                                        steps=1, t=ans, start_pos=-1, light_sf=1.1)
        xshift = lambda dir : self.play(A.mob.animate.shift(0.5*dir),   
            run_time=0.3, rate_func=rate_functions.ease_out_sine )

        # main
        for pos in range(1, 23):
            if pos not in X:
                step(0.5, True)
                continue

            # at this point, we're about to enter a portal
            lab  = labs[i]
            labc = labs[i].copy()
            ent, p = pm[pos]
            pex = p.mobs.exit
            x,y,s,i = grab(i)

            # compute dist
            pl, pr = map(ax.n2p, [x,y])
            dist_line = Line(pl, pr, color=RED).scale(1.1)
            self.play( tf_hold(py[7]) )
            self.play( *map(FadeOut, all_vmobs_in(pobjs, exclude={p.mob})), FadeOut(ant.mob) )
            self.add_foreground_mobject(p.mob)
            dist_i = MathTex(f"{x-y}").next_to(math_eq).set_x( dist_ul.get_x() )
            self.play( Create(dist_line) )
            self.play( FadeIn(eq) )
            self.play( Transform(dist_line, dist_i) )
            self.play( *map(FadeIn, all_vmobs_in(pobjs, exclude={p.mob})), FadeIn(ant.mob) )
            self.play( tf_revert(py[7]) )
            self.remove_foreground_mobject(p.mob)
            self.add_foreground_mobject(ant.mob)

            # binary search
            self.play( tf_hold(py[8]) )  # highlight `bisect`
            xshift(UP)
            j = anim_bisect(self, A, y, 'j', start=0, end=i, RT=0.12, scale_factor=0.65, labs=labs)
            xshift(DOWN)
            self.play ( tf_revert(py[8]) )  # unhighlight

            # TODO: prefix sum
            self.play( tf_hold(py[9]) )
            left  = pex[0].get_center() + 1/5 * LEFT
            right = ent[0].get_center() + 1/5 * RIGHT
            rect  = Rectangle(width=right[0]-left[0]+0.05, height=1.4, fill_opacity=0.3, fill_color=PINK, color=RED)
            rect.move_to( VGroup(pex[0], ent[0]).get_center() )
            self.play( DrawBorderThenFill(rect, run_time=1.3) )
            cost = ps[i-1] - ps[j]
            cost_i = MathTex( str(cost) ).next_to(math_pl).set_x( cost_ul.get_x() )

            # lcpy = [l.copy().center() for l in labs[j:i-1]]
            # if not lcpy: lcpy = [ MathTex('0', font_size=36) ]
            # vgl = VGroup(*lcpy).arrange(RIGHT, buff=0.25).next_to(ax, 2*DOWN)
            # self.play( Transform(rect, vgl) )
            anim_psum_query1(self, i-1, j, DP, PS)
                # anim_pos=ax.get_center()+3*DOWN, 
                # scale_factor=SF
            # )

            self.play( FadeOut(rect) )
            self.play( tf_revert(py[9]) )

            # update 
            dpi = cost + x - y
            dp_lab = MathTex(str(dpi), font_size=36).move_to(lab)
            self.play( Transform(lab, dp_lab), Transform(labc, cost_i) )
            eqc = eq.copy().move_to(eq).add(labc, dist_line)
            dpi_eq  = MathTex(f"dp_i = {dpi}")
            dpi_fin = MathTex(f"{dpi}")
            self.play( Transform(eqc, dpi_eq) )
            self.play( Transform(eqc, dpi_fin) )
            DP[i-1].mobs.tex = dpi_fin.copy().move_to(DP(i-1)).scale(SF)
            PS.append(dpi + ps[-1])
            PS(-1).scale(SF).next_to( PS(-2), buff=0 )
            self.play( eqc.animate.move_to(DP(i-1)))
            vg = VGroup(DP[i-1].mobs.tex, PS(-1))
            self.play( Transform(eqc, vg), FadeOut(eq) )
            ps += [dpi]

            step(1/5, True)    # enter portal
            step(1/15, False)  # tp back
            while ant.props.pos != pos:  # sim until about to enter again
                to_enter = (ant.props.pos == pos-1)
                _rt = 1/5 if to_enter else 1/15
                step(_rt, to_enter)
            if i == 3: break

        self.wait(3)

        # for pos in range(1, 23):
        #     if pos == 1:
        #         t = simulate(self, ant, portals, ax, indi=True, run_time=.5, steps=1, start_pos=-1)
        #     else: simulate(self, ant, portals, ax, indi=True, run_time=.5, steps=1, start_pos=-1, t=t)
        #     if pos not in X:
        #         while ant.props.pos != pos:
        #             simulate(self, ant, portals, ax, indi=False, run_time=0.01,
        #              steps=1, t=t, start_pos=-1)
        #         continue
        #     x,y,s = X[i], Y[i], S[i]
        #     i += 1
        #     p = pm[x][1]
        #     pmobs = pm[x][0] + pm[y][0]
        #     self.bring_to_front(*pmobs)
        #     self.play( *map(tf_show, pmobs) )
        #     anim_bisect(self, A, y, 'j', RT=0.15, scale_factor=0.75)
        #     arc = p.show_arc(angle=-TAU/4, return_mob=True)
        #     self.play( Create(arc) )
        #     dist = MathTex(f"{x-y}").shift(UP+RIGHT)
        #     self.play( Transform(arc,dist) )
        #     self.play( Unwrite(arc) )
        #     # show dist line, transform into dist_i val
        #     # slice dp_labels and show psum anim, transform into cost_i val
        #     # merge Transform dist_i, cost_i, into new ps val
        #     # play/hold/revert the right lines of py
        #     # change src_py to reflect ps.append()
        #     # change src_py to reflect `cost`
        #
        # self.wait(3)


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
        ps.append( ps[i] + dp_i )
        ans += S[i] * dp_i
        
    end = X[-1] + 1
    return ans + end

"""
