from core import *
from common import *

class Induction(Scene):
    def construct(self):
        @cluster
        def proof():
            BUF = 1.2
            tex = lambda s : Tex(r"\raggedright " + s, font_size=26)
            fly = lambda s : StyleText(s, font_size=27, underline=True)
            sml = lambda s : Tex(r"\raggedright " + s, font_size=22)
            
            lab = fly("Claim:")
            txt = tex(r"All portal entrances to the left of \\the ant at any given time are OPEN!")
            txt.to_corner(LEFT+UP, buff=3/4)
            lab.next_to(txt, UP).align_to(txt, LEFT)
            claim = VGroup(lab, txt)

            lab = fly("Base Case:")
            mtx = Tex("$t = 0$", font_size=33)
            txt = tex("Trivially true, since no portals behind initially.")
            txt.next_to(claim, DOWN, buff=BUF).align_to(claim, LEFT)
            VGroup(lab, mtx).arrange().next_to(txt, UP).align_to(txt, LEFT)
            base = VGroup(lab, mtx, txt)
            
            lab = fly("Inductive Hypothesis (IH):")
            txt = tex("Assume all portal entrances to the left are open.")
            txt.next_to(base, DOWN, buff=2*BUF+0.4).align_to(claim, LEFT)
            lab.next_to(txt, UP).align_to(txt, LEFT)
            hyp = VGroup(lab, txt)

            lab = fly("Inductive Step:")
            txt = tex("Assume IH is true. Claim remains true if we cross:")
            st1 = sml(r"1. Closed entrance; it opens up behind us, all portals to our left still open.\\")
            st2 = sml(r"2. Open entrance; it sends us to the left. \\ \hspace{0.13in} Since IH was true, all portals to our left still open.")
            txt.next_to(hyp, DOWN, buff=BUF).align_to(claim, LEFT)
            lab.next_to(txt, UP).align_to(txt, LEFT)
            st1.next_to(txt, DOWN).align_to(txt, LEFT)
            st2.next_to(st1, DOWN).align_to(txt, LEFT)
            istep = VGroup(lab, txt, st1, st2)

            claim.to_corner(UP+LEFT, buff=3/4).shift(1/4*UP)
            base.next_to(claim, DOWN).align_to(claim, LEFT).shift(0.2*DOWN)
            hyp.to_corner(UP+RIGHT, buff=3/4).shift(1/3*DOWN)
            istep.center().shift(2.25*DOWN)
        
        @sub_scene
        def demo():
            def step():
                ax = NumberLine(
                    x_range=[0, 8],
                    length=30,
                    color=BLUE,
                ).shift(1/2*RIGHT)
                bx = NumberLine(
                    x_range=[0, 12],
                    length=10,
                    color=BLUE,
                )
                ant = Ant(ax=ax, pos=3)
                port = [Portal(x=5, y=4, open=0, ax=ax, color=BLUE)]
                self.play(FadeIn(ax))
                yield  # 1

                bb = BlackBox(self, width=5, height=1).to_edge(LEFT).shift(2*LEFT)
                self.play( Create(ant.mob), FadeIn(bb) )
                self.play( Indicate(proof.base, scale_factor=1.1) )
                yield  # 2

                def make_portal(i, c=[0], cols=[ RED, BLUE, PURPLE, GREEN ]):
                    o = Portal(x=i, y=0, open=1, ax=ax, color=cols[ c[0] ])
                    self.add_foreground_mobject(o.mob)
                    c[0] += 1
                    return Create(o.mob)
                
                self.play( Indicate(proof.hyp, scale_factor=1.1), make_portal(2.1), make_portal(2.3), make_portal(2.5), make_portal(2.7) )
                yield  # 3
                
                for p in port:
                    self.play(FadeIn(p.mob))
                # beat 11: [Show ant teleporting back, grow size of open portals or smth]
                coords = [(2, 1, 1), (4, 3, 1), (7, 6, 1), (9, 8, 1), (11, 5, 1)]
                portals = createPortals(coords, bx)
                self.bring_to_front(ant.mob)
                sim = lambda s : simulate(self, ant, port, ax, run_time=1, indi=False, t=-1, start_pos=3, steps=s)
                sim(3)
                self.play( Indicate(proof.st1, scale_factor=1.1) )
                yield  # 4

                sim(3)
                self.play( Indicate(proof.st2, scale_factor=1.1) )
                yield  # 5

        self.play( Write(proof.claim) )
        next(demo)  # 1
        self.wait()
        self.play( Write(proof.base) )   # show base case in parallel
        next(demo)  # 2
        self.wait()
        self.play( Write(proof.hyp) )    # show black box with some open portals
        next(demo)  # 3
        self.wait()
        self.play( Write(proof.lab), Write(proof.txt) )  # show p10 anim
        self.play( Write(proof.st1) )
        next(demo)  # 4
        self.wait()
        self.play( Write(proof.st2) )
        next(demo)  # 5
        self.wait()




