from core import *
from manim import *
from common import *

class p18(MovingCameraScene):
    def construct(self):
        ax = NumberLine(
            x_range=[0, 8],
            length=10,
            color=BLUE,
            include_numbers=False,
            line_to_number_buff=MED_LARGE_BUFF,
            z_index=-5
        )
        self.bring_to_back(ax)

        ant = Ant(ax=ax, pos=7)
        P = Portal(x=8, y=0, open=1, ax=ax)
        p1 = Portal(x=3.5, y=2.25, open=1, ax=ax)
        p2 = Portal(x=4.75, y=2.75, open=1, ax=ax)
        p3 = Portal(x=5.75, y=4, open=1, ax=ax)
        pmobs = [p.mob for p in (p1,p2,p3)]


        equation = VGroup().shift(3*DOWN)
        def eq_add(*o : VMobject):
            equation.add(*o)
            self.play(equation.animate.set_x(0))


        # Suppose we're calculating the return trip time, or the dp value for portal i.
        dp_i = MathTex("dp_i = ").shift(3*DOWN)
        eq_add(dp_i)
        self.play( FadeIn(P.mob), Create(ant.mob), *map(FadeIn, pmobs) )

        anim = [ScaleInPlace(o, scale_factor=1.75, rate_func=hint) for o in P.mobs]
        self.play( *anim )

        # TODO: add X_i and Y_i label

        # let's first ignore the portals in the middle
        tf = lambda o : o.animate.set_opacity(0.3)
        self.play( *map(tf, pmobs) )
        self.wait(1)

        # No matter what, it's clear that on the return trip,
        # we will need to at least travel this yellow distance X[i] - Y[i]. Let's call this term dist
        brace = BraceBetweenPoints(ax.n2p(0), ax.n2p(8)).shift(0.5*DOWN)
        self.play( GrowFromCenter(brace), FadeToColor(ax,color=YELLOW) )
        dist = MathTex("dist_i = X_i - Y_i", color=YELLOW).next_to(brace, DOWN)
        self.play( Write(dist, run_time=0.75) )
        self.wait(1.5)
        tf = Transform(dist, MathTex("dist_i", color=YELLOW).next_to(equation, RIGHT))
        self.play( tf, ShrinkToCenter(brace) )
        eq_add(dist)
        self.wait(1)

        # Next, let's see how we can deal with the portals in the middle.
        # TODO: actually have portals in the middle
        # TODO: figure out how to do the starry thing
        # Let's first abstract away this messy cluster of interleaved portals as a single term:
        # we'll call it cost
        BB = BlackBox(self, height=2.5, width=6)
        self.play( GrowFromCenter(BB) )
        pent = MathTex("cost_i = \,\,?", color=PINK)
        self.add_foreground_mobject(pent)
        self.bring_to_front(pent)
        plus = MathTex("+").next_to(equation,RIGHT)
        self.play( Write(pent, run_time=1.7) )
        self.wait(1)

        # TODO: continuously center the VGroup of labels at the bottom
        pent2 = MathTex("cost_i",color=PINK).next_to(plus, RIGHT)
        # self.add_foreground_mobject(pent2)
        self.play( Transform(pent, pent2), Write(plus) )
        eq_add(plus, pent)

        # TODO: consider this zoom option
        # scene = VGroup(*[o for o in self.mobjects if isinstance(o, VMobject)])
        # self.play( ScaleInPlace(scene, scale_factor=3) )

        # TODO: if use this, do magic in post? with a separate scene?
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set_width(BB.width*1.05))

        tf = lambda o : o.animate.set_opacity(1)
        self.add_foreground_mobjects(*pmobs)
        self.play( *map(tf, pmobs), rate_func=rate_functions.ease_in_out_sine )

        # in terms of calculating how much time these middle portals will set us back
        # we've already done most of the heavy lifting!
        # recall that we're calculating dp_i. This means that, since
        # we've made it this far, the dp values for 0, all the way thru i-1
        # are already solved!

        # first of all, we can ignore the exit points of the portals.
        exits = [p.mobs.exit for p in (p1,p2,p3)]
        self.play( *map(Uncreate, exits) )
        self.wait(3)

        # in fact, even if the exits lay outside of the range of this black box, i.e.
        # to the left of Y_i, we can still ignore them, because we've already accounted
        # for them in our previous dp calculations.

        # next, we're absolutely sure that each of these portals are open, since they're
        # behind the ant, which we proved a while ago. We also already know each of their return
        # trip times, so we can effectively abstract away each of these entrances as a *flat*
        # penalty time!
        bbs = [BlackBox(self, height=1, width=1).move_to(p.mobs.entrance) for p in (p1,p2,p3)]
        labs = [MathTex(f"dp_{{i-{3-i}}}", font_size=24).move_to(bbs[i]) for i in range(3)]
        vg = [VGroup(bbs[i], labs[i]) for i in range(3)]
        self.play( *map(GrowFromCenter, bbs) )
        for l in labs: self.add_foreground_mobject(l)
        self.play( *map(Write, labs) )

        # we also don't care exactly where they are, just as long as they're caught in the middle
        # of our return trip, we'll have to pay the penalty time.
        for p in (p1,p2,p3):
            p.remove(self)
        mtp1, mtp2 = MathTex("+"), MathTex("+")
        boxes = VGroup(vg[0], mtp1, vg[1], mtp2, vg[2])
        self.play( Transform(boxes, boxes.copy().center().arrange(RIGHT)) )
        self.add_foreground_mobjects(mtp1, mtp2)
        self.play( Write(mtp1), Write(mtp2) )


        self.wait(2)
        self.play(Restore(self.camera.frame))
        self.wait(1)

        keep = {*equation.submobjects}
        self.play( *map(FadeOut, all_vmobs_in(self, exclude=keep)) )

        self.play( equation.animate.center().shift(UP) )
        self.play( equation.animate.arrange(RIGHT, buff=0.75))

        dist_mt = MathTex("X_i - Y_i", color=YELLOW).next_to(dp_i, RIGHT)
        plus2 = plus.copy().next_to(dist_mt, RIGHT)
        pent_mt = MathTex("\sum^{i-1}_{k=j} dp_k", color=PINK).next_to(plus2, RIGHT)
        labs = VGroup(dist_mt, pent_mt)
        tf = lambda o,mt : o.animate.move_to( mt.get_center()+1.2*UP )
        self.play( *map(Write, labs.submobjects),
                   Transform(plus, plus2),
                   tf(dist, dist_mt),
                   tf(pent, pent_mt)  )

        p = lambda o : isinstance(o, MathTex)
        mobs = VGroup( *all_vmobs_in(self, pred=p) )
        self.play(mobs.animate.center())

        where = Tex("where $j$ is the smallest index such that $X_j > Y_i$", font_size=20).shift(1.5*DOWN)
        self.play( Write(where) )


        self.wait(3)