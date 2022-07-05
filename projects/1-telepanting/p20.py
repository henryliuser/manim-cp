from manim import *
from core import *

class p20(Scene):
    def construct(self):
        N = 10
        A = Array( [1, 3, 5, 6, 8, 10, 14, 15, 25, 32] )
        A.mob.shift(DOWN)
        self.play( Create(A.mob) )

        # legend
        rect = lambda c : Rectangle(color=c, height=0.5,width=0.5, fill_color=c, fill_opacity=1)
        tex  = lambda t : Tex(t, font_size=24)
        leg_red   = rect(RED)   .to_edge(UP+LEFT)
        leg_gray  = rect(GRAY)  .next_to(leg_red, DOWN)
        leg_blue  = rect(BLUE)  .next_to(leg_gray, DOWN)
        leg_green = rect(GREEN) .next_to(leg_blue, DOWN)

        lab_red   = tex("definitely nope")   .next_to(leg_red,   RIGHT)
        lab_gray  = tex("still looking...")  .next_to(leg_gray,  RIGHT)
        lab_blue  = tex("insertion point!")  .next_to(leg_blue,  RIGHT)
        lab_green = tex("found it!")         .next_to(leg_green, RIGHT)
        legend = VGroup(leg_red, leg_gray, leg_blue, leg_green, lab_red, lab_gray, lab_blue, lab_green)
        self.play( FadeIn(legend), run_time=0.3 )

        # let's try searching for a few elements naively, using linear search
        q = Tex()
        idx = Tex('i')
        queries = [6, 4, 15, 32, 7]
        for x in queries:
            RT = 0.1
            anim = [ A[i].anim_highlight(GRAY) for i in range(N) ]
            self.play( *anim, run_time=RT )

            q2 = Tex(f"q = {x}").center().to_edge(UP)
            anim  = [ Transform(q, q2) ]
            anim += [ Transform(idx, idx.copy().next_to(A(0), UP)) ] 
            self.play( *anim, run_time=RT )
            for i in range(N):
                anim = []
                if i: anim += [ idx.animate.next_to(A(i), UP) ]
                anim += [ A[i].anim_highlight(YELLOW) ]
                self.play( *anim, run_time=RT )
                if A.og[i] == x:
                    self.play( A[i].anim_highlight(GREEN, run_time=RT) )
                    self.wait(0.5)
                    break
                if A.og[i] > x:
                    self.play( A[i].anim_highlight(BLUE, run_time=RT) )
                    self.wait(0.5)
                    break
                self.play( A[i].anim_highlight(RED, run_time=RT) )


        # but because the array is sorted, when we compare some number, we know exactly
        # whether or not we need to look higher or lower. We can exploit this fact
        # to find elements more efficiently.
        self.wait(1)
        anim = [ A[i].anim_highlight(BLACK) for i in range(N) ]
        self.play( *anim, FadeOut(idx), run_time=0.2 )

        ldx, rdx = map(MathTex, 'LR')
        dx = [idx, ldx, rdx]
        for x in queries:
            RT = 0.6 if x == 6 else 0.3
            anim = [ A[i].anim_highlight(GRAY) for i in range(N) ]
            self.play( *anim, FadeOut(idx), run_time=0.2 )

            q2 = Tex(f"q = {x}").center().to_edge(UP)
            self.play( Transform(q, q2) )

            def found(i, col=GREEN):
                self.play( Transform(idx, idx.copy().next_to(A(i), UP)), run_time=RT )
                self.play( A[i].anim_highlight(col), run_time=RT )
                self.wait(0.5)

            l, r = 0, N
            anim  = [ ldx.next_to(A(0), DOWN) ]
            anim += [ rdx.next_to(A(-1),DOWN) ]
            self.play( *map(FadeIn, anim), run_time=RT )

            def showLR():
                anim = []
                a,b = l, min(r, N-1)
                off = 0 if a != b else 0.2
                anim += [ Transform(ldx, ldx.copy().next_to(A(a), DOWN).shift(off*LEFT))  ]
                anim += [ Transform(rdx, rdx.copy().next_to(A(b), DOWN).shift(off*RIGHT)) ]
                return anim

            while l < r:
                # move idx
                m = (l+r) >> 1
                if l == 0 and r == N:
                    idx.next_to(A(m), UP)
                    anim = [ FadeIn(idx, run_time=RT) ]
                else: anim = [ Transform(idx, idx.copy().next_to(A(m), UP), run_time=RT) ]
                self.play( *showLR(), *anim, run_time=RT )

                # split search space
                if A.og[m] >= x: r = m
                else : l = m+1

                # animate search space
                self.play( A[m].anim_highlight(YELLOW, rate_func=flash, run_time=2*RT) )
                anim = []
                for i in range(N):
                    if i < l or i > r:
                        anim += [ A[i].anim_highlight(RED) ]
                self.play( *anim, run_time=RT )
            else:
                if l < N and A.og[l] == x:
                    found(l)
                elif l < N:
                    found(l, BLUE)
                else:
                    self.play( A[l].anim_highlight(RED), run_time=RT )

            self.play( *showLR(), run_time=RT )
            self.wait(0.5)
            self.play( *map(FadeOut, dx), run_time=RT )


        self.play( FadeOut(legend), FadeOut(A.mob), FadeOut(q), run_time=0.3 )

        self.wait(3)

