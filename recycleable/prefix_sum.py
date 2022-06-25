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
        flash(self, title, 0.5)

        # suppose we had the following integer array A of size N, in this case, 7
        N = 7
        A = Array( [1,3,2,7,9,5,4] )
        A.mob.shift(0.75*RIGHT)
        Alab = Tex("$A = $").next_to(A.mob, LEFT)
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
        self.play( Create(title) )
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
        zero.mob.next_to(PS.mob, LEFT, buff=0)
        # PS.mob.add(zero.mob)
        PSlab = Tex("$ps = $").next_to(zero.mob, LEFT)
        self.play( Create(PS.mob), Create(zero.mob), Write(PSlab) )



        self.wait(3)