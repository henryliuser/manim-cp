import sys
ROOTS = ['/Users/henryliu/Desktop/manim-cp/', '/Users/samuelbrashears/PycharmProjects/manim-cp/']
for R in ROOTS: sys.path += [R, R+'core']
from manim import *
from core import *

class PSumDemo(Scene):
    def construct(self):
        # prefix sums are a technique that allows us to quickly compute the
        # sum of any subarray in O(1), or constant time.
        # Because it's a general technique, I'll only give a brief summary here.

        # suppose we had the following integer array A of size N, in this case, 7
        N = 7
        A = Array( [1,3,2,7,9,5,4] )
        A.center()
        self.play( Create(A) )
        self.wait(2)

        # and we were tasked with answering Q queries,
        # where each query is a pair [L, R] representing an inclusive, contiguous range
        # of indices. The answer to each query is the sum of the elements of A in that range.
        t = Tex("queries[0] = [2,4]")
        t.shift(UP)
        self.play( Write(t), run_time=0.6 )
        self.wait(2)

        # for example, consider the query [2,4].
        anim = []
        for i in range(2, 5):
            mate = A.backgrounds[i].animate
            anim += [ mate.set_fill(LIGHT_ORANGE, 0.7) ]
        self.play( *anim, run_time=0.6 )
        self.wait(1)

        # the sum of the elements in this range is as follows:
        # 2 + 7 + 9 = 18
        math = Tex("2 + 7 + 9 = 18")
        math.shift(DOWN)
        mp = math.copy()
        mp.shift(DOWN)
        self.play( Write(math) )
        self.play( Write(mp) )


        self.wait(5)





