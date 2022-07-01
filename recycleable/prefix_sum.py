import sys
from manim import *
from core import *


# TODO: add indices

class PSumDemo(Scene):
    def construct(self):
        # prefix sums are a technique that allows us to quickly compute the
        # sum of any subarray in O(1), or constant time.
        # Because it's a general technique, I'll only give a brief summary here.
        title = StyleText("Prefix Sums", bold=1).to_edge(UP)
        self.play( Flash(title, 0.5) )

        # suppose we had the following integer array A of size N, in this case, 7
        N = 7
        A = Array( [1,3,2,7,9,5,4] )
        A.mob.shift(0.75*RIGHT)
        Alab = Mono("A = ").next_to(A.mob, LEFT)
        self.play( Create(A.mob), Write(Alab) )
        self.wait(2)

        # and we were tasked with answering Q queries, where each query
        # is a pair [L, R] representing an inclusive, contiguous range of indices.
        qmob = VGroup()
        qmobs = []
        queries = [ [2,4], [1,3], [5,5], [0,6] ]
        for l,r in queries:
            x = Mono(f"[{l},{r}]")
            qmobs += [x]
            qmob.add(x)
        qmob.arrange(DOWN).to_edge(LEFT, buff=0.7)
        qlab = Mono("queries")
        qlab.next_to(qmob, UP)
        self.play( Write(qlab) )
        self.play( Create(qmob) )

        # the answer to each query is the sum of the elements of A in that range,
        arw = Mono("->").next_to(A.mob, UP)
        func = Mono("answer(L,R)").next_to(arw, LEFT)
        ret = Mono("A[L] + ... + A[R]").next_to(arw, RIGHT)
        ret2 = Mono("sum( A[L:R] )").next_to(arw, RIGHT)
        anim = [arw, func, ret]
        for a in anim: self.play( Write(a), run_time=0.4 )
        self.wait(1)
        # or in other words, the sum of the specified subarray.
        self.play( Transform(ret, ret2) )
        self.wait(1)
        self.play( *map(FadeOut, anim) )

        # for example, consider the query [2,4]
        dot = Dot().next_to(qmobs[0], LEFT)
        self.play( Create(dot) )
        l,r = queries[0]
        t = Mono(f"queries[0] = [{l},{r}]").next_to(A.mob, UP)
        for i, (l,r) in enumerate(queries):
            t2 = Mono(f"queries[{i}] = [{l},{r}]").next_to(A.mob, UP)
            abc = Transform(t, t2) if i else Write(t)
            anim = [ abc ]
            if i: anim += [ dot.animate.next_to(qmobs[i], LEFT) ]
            self.play( *anim, run_time=0.6 )
            self.wait(1)
            anim = [ A[i].anim_highlight(LIGHT_BROWN) for i in range(l,r+1) ]
            self.play( *anim )
            self.wait(0.5)
            anim = [ A[i].anim_highlight(BLACK) for i in range(l,r+1) ]
            self.play( *anim )
            self.wait(0.3)
            ele,sub = A[l:r+1]
            self.play( sub.animate.shift(2*DOWN) )

            # the sum of the elements in this subarray is 2+7+9=18
            st = Tex(r"$\sum$").next_to(sub, LEFT)
            es = Tex(r"$=$").next_to(sub, RIGHT)
            eq = Tex(rf"$0$").next_to(es, RIGHT)
            self.play( *map(Write, [st,es,eq]) )

            cur = 0
            for i,e in enumerate(ele):
                anim = [e.anim_highlight(LIGHT_BROWN)]
                cur += e.props.value
                if i: anim += [ ele[i-1].anim_highlight(BLACK) ]
                eq2 = Tex(rf"${cur}$").next_to(es, RIGHT)
                anim += [ Transform(eq, eq2) ]
                self.play( *anim, run_time=0.4 )
            self.play( e.anim_highlight(BLACK), run_time=0.4 )

            self.play( Indicate(eq) )
            z = [eq, es, st, sub]
            self.play( *map(FadeOut, z) )

        # as you can see, this is not very efficient.
        # the time complexity of this solution is O(QN)
        # in the worst case, we have to loop through the entire array, for each query.

        # and that brings us to prefix sums.
        self.play( Create(title), FadeOut(t) )
        self.wait(1)

        # you may have noticed that with the naive solution from before,
        # we end up doing a lot of redundant computation.
        # we're adding up the same numbers over and over again, it's wasteful!

        ps = [0] * (N+1)
        for i in range(N):
            ps[i+1] = A[i].props.value + ps[i]

        # let's now create a new array called `ps`, short for prefix sums
        # we'll add this extra 0 at the beginning for convenience later.
        # at each index, let's store the sum of the entire prefix of the
        # original array A, up to but not including that index. formally,
        t = [Mono("ps[0] = 0"), Mono("ps[i] = sum( A[0:i) )")]

        PS = Array(ps[1:])
        zero = Array.Element(value=0)
        PS.mob.next_to(A.mob, DOWN, buff=0.5)
        PS.props.arr = [zero] + PS.props.arr
        zero.mob.next_to(PS.mob, LEFT, buff=0)
        PSlab = Tex("$ps = $").next_to(zero.mob, LEFT)
        self.play( Create(PS.mob), Create(zero.mob), Write(PSlab) )

        for i in range(N):
            anim = [ PS[i+1].anim_highlight(LIGHT_BROWN) ]
            anim += [ A[i].anim_highlight(LIGHT_BROWN) ]
            anim += [ PS[i].anim_highlight(BLACK) ]
            self.play( *anim, run_time=0.4 )
        self.wait(1)
        anim = [ A[i].anim_highlight(BLACK) for i in range(N) ]
        anim += [ PS[-1].anim_highlight(BLACK) ]
        self.play( *anim, run_time=0.4 )

        l,r = queries[0]
        self.play( *map(FadeOut, [title, PS.mob, zero.mob, PSlab]) )
        # arc = ArcBetweenPoints(UP,UP)
        # sumTex = Tex().move_to(arc)
        t = Mono(f"queries[0] = [{l},{r}]").center().to_edge(UP)
        target = Alab.copy().shift(1.5*DOWN)
        target2 = target.copy().shift(1.2*DOWN)
        psr = Mono("ps[r] =").move_to(target).align_to(target, RIGHT)
        psl = Mono("-ps[l-1] =").move_to(target2).align_to(target2, RIGHT)

        self.play( Write(psr), Write(psl) )

        # TODO: dot index on queries
        # TODO: VGroup(psr, psl) -> 'ps[r] - ps[l-1]' =
        # TODO: red slice line into fade out
        for i, (l,r) in enumerate(queries):
            t2 = Mono(f"queries[{i}] = [{l},{r}]").move_to(t)
            abc = Transform(t, t2) if i else Write(t)
            # tl, tr = map(Tex, "LR")
            lp = A(l).get_center() + 0.6*UP + 0.2*LEFT
            rp = A(r).get_center() + 0.6*UP + 0.2*RIGHT
            arc = ArcBetweenPoints(start=lp, end=rp, angle= -PI/2)

            anim = [
                A[j].anim_highlight(LIGHT_BROWN,
                  run_time=1.5,
                  rate_func=there_and_back_with_pause)
                for j in range(l,r+1)
            ]

            # tl.next_to(A[l].mob, UP)
            # tr.next_to(A[r].mob, UP)
            # self.play( *map(Create, [tl,tr]) )
            self.play( Create(arc), *anim )
            self.play( FadeOut(arc) )
            eb, mb = A[:r+1]
            es, ms = A[:l]

            anim = [ mb.animate.next_to(target, RIGHT), abc ]
            if es: anim += [ ms.animate.next_to(target2, RIGHT) ]
            self.play( *anim )

            if es:
                slice = Rectangle(color=RED, fill_opacity=1, fill_color=RED, height=3, width=0.02)
                mid = midpoint( es[-1].mob.get_center(), eb[l].mob.get_center() )
                slice.move_to(mid)
                anim = [ Flash(slice, 1.3) ]
                for i in range(l):
                    anim += [ *map(FadeOut, [es[i].mob, eb[i].mob]) ]
                self.play( *anim )

            anim  = [ FadeOut(eb[i].mob) for i in range(l, r+1) ]
            self.play( *anim )

            # lc = A[l].mob.get_center() + 0.6*UP + 0.2*LEFT
            # rc = A[r].mob.get_center() + 0.6*UP + 0.2*RIGHT
            # arc2 = ArcBetweenPoints(start=lc, end=rc, angle= -PI/2)
            # sumTex2 = Tex("$\sum$").next_to(arc2, UP)
            # self.play( Transform(arc, arc2), abc, Transform(sumTex, sumTex2) )  # add dot arc thing later

        self.wait(3)