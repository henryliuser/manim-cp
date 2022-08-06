from core import *
from manim import *
from common import *

# Add sample case (first line, then ant, then portals, then states, then show progression)
class p16(Scene):
    def construct(self):
        ax = NumberLine(
            x_range=[0, 9],
            length=10,
            color=BLUE,
            include_numbers=True,
            line_to_number_buff=MED_LARGE_BUFF,
        )

        N = 4
        ant = Ant(ax=ax)
        X = Array( [3, 6, 7, 8] )
        Y = Array( [2, 5, 4, 1] )
        S = Array( [0, 1, 0, 1] )

        s1 = VGroup(ant.mob, ax)
        coords = [ *zip(X.og,Y.og,S.og) ]
        portals = createPortals(coords, ax)

        self.play(Create(ax))
        self.play(Create(ant.mob))
        self.add_foreground_mobject(ant.mob)

        mp = portal_map(portals)
        self.play( *[FadeIn(p.mob) for p in portals] )
        s1.add( *[p.mob for p in portals] )


        s2 = s1.copy().scale(0.8).shift(2.5*UP)
        self.play( Transform(s1, s2) )

        X.label = Mono("X = ").center().to_edge(LEFT).shift(0.6*UP)
        X.rlab = Tex("$X_i$ = entrance position of $i^{th}$ portal", font_size=DEFAULT_FONT_SIZE-5).to_edge(RIGHT).shift(0.6*UP)
        Y.label = Mono("Y = ").center().to_edge(LEFT).shift(0.6*DOWN)
        Y.rlab = Tex("$Y_i$ = exit position of $i^{th}$ portal", font_size=DEFAULT_FONT_SIZE-5).to_edge(RIGHT).shift(0.6*DOWN)
        S.label = Mono("S = ").center().to_edge(LEFT).shift(1.8*DOWN)
        S.rlab = Tex("$S_i$ = initial state of $i^{th}$ portal", font_size=DEFAULT_FONT_SIZE-5).to_edge(RIGHT).shift(1.8*DOWN)
        self.play( *[Write(o.label) for o in (X,Y,S) ] )


        for o in [X,Y,S]:
            o.mob.next_to(o.label, RIGHT)

        self.play( *[Create(o.mob) for o in (X,Y,S) ] )

        xidx, yidx = {}, {}
        for i in range(10):
            if i not in mp: continue
            pobj = mp[i][0]
            if len(pobj) > 1:
                pobj = pobj[0]
                d = Dot(point=pobj.get_center())
                j = len(xidx)
                idx = Tex(f"X[{j}]", font_size=30).next_to(d, 2*UP)
                xidx[j] = idx
            else:
                pobj = pobj[0]
                d = Dot(point=pobj.get_center())
                for j in range(N):
                    if Y.og[j] == i: break
                idx = Tex(f"Y[{j}]", font_size=30).next_to(d, 2*UP)
                yidx[j] = idx


        for A in [X,Y,S]:
            self.play( Write(A.rlab), run_time=0.5 )
            for i in range(N):
                # portal object : {entrance, exit}
                pobj = mp[ A.og[i] ] if A != S else mp[ X.og[i] ]
                high = A[i].anim_highlight(LIGHT_BROWN, rate_func=flash)
                f = lambda o : ScaleInPlace(o, scale_factor=1.75, rate_func=flash)
                indi = [ *map(f, pobj[0]) ]
                self.play( *indi, high )
            self.play( Unwrite(A.rlab), run_time=0.5 )

        self.wait(3)

        dp = Array( ['?'] * N )
        dp.mob.to_edge( RIGHT )
        dp.label = Mono("dp = ").next_to(dp.mob, LEFT)
        self.play( Write(dp.label), Create(dp.mob) )

        self.wait()



        # ignore below for now

        #############
        ## BEAT 17 ##
        #############

        # for the sake of computing dp, we can pretend that all of the portals are open.
        # as we've shown, the initial state doesn't end up mattering until the final calculation.
        # this will help us better visualize it.
        anim = []
        for i in [3,7]:
            _, pobj = mp[i]
            anim += [ pobj.toggle() ]
        self.play( *anim )
        
        fade = []
        for o in [X,Y,S]:
            fade += [o.mob, o.label]
        
        dpv = VGroup( dp.mob, dp.label )
        target = dpv.copy().center().to_edge(DOWN).shift(0.5*UP)
        self.play( dpv.animate.move_to(target), *map(FadeOut, fade) )
        self.wait()

        # we know that, regardless of the portal configuration *between*
