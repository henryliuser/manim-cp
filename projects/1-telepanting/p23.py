from common import *
from core import *
from manim import *

ftc = lambda o : Indicate(o)

class p23(Scene):
    def construct(self):
        py = CodeBlock(
            code=src_py,
            tab_width=4,
            background_stroke_width=1,
            background_stroke_color=WHITE,
            insert_line_no=True,
            style="monokai",
            font="Monaco",
            font_size=15,
            line_spacing=1,
            language="py",
        ).center().to_edge(LEFT)

        cpp = CodeBlock(
            code=src_cpp,
            tab_width=4,
            background_stroke_width=1,
            background_stroke_color=WHITE,
            insert_line_no=True,
            style="monokai",
            font="Monaco",
            font_size=12,
            line_spacing=1.0,
            language="cpp",
        ).center().to_edge(RIGHT)

        self.play( Create(py), Create(cpp) )

        # First, let's initialize an integer `cost`, representing
        # the total amount of *penalty time* we've incurred.
        anim = [ py[3], cpp[7] ]
        self.play( *map(ftc, anim) )

        # # Let's also make the auxiliary array `ps`, representing the prefix sum of `dp`.
        # # Note that we don't actually need to make the `dp` array itself, since we can already
        # # extract its contents from `ps`. Also, notice that we are actually building the prefix
        # # sum as we go, instead of all up front. This is necessary because we need the previous
        # # values to compute the next one, and this totally works because we only ever need prefix sums
        # # from the values behind us.
        # anim = [ py[4], cpp[8] ]
        # self.play( *map(ftc, anim) )
        #
        # # now, let's loop through the portals 1 by 1 and try to compute their
        # # return trip times (or formally, let's find dp_i).
        # anim = [ py[5], cpp[9] ]
        # self.play( *map(ftc, anim) )
        #
        # # we'll grab the enter and exit coords of the current portal
        # anim = [ *py[6:8], *cpp[10:12] ]
        # self.play( *map(ftc, anim) )
        #
        # # and then binary search for the index j, of the leftmost entrance that comes after our exit
        # anim = [ py[9], *cpp[12:14] ]
        # self.play( *map(ftc, anim) )
        #
        # # once we have that, we can compute our return trip time, dp_i = distance + penalty
        # anim = [ py[11], cpp[16] ]
        # self.play( *map(ftc, anim) )
        #
        # # where distance is the coordinate difference between enter and exit,
        # # and penalty is the subarray sum of the dp values from j to i, or in other words ps[i] - ps[j]
        # anim = [ *py[9:11], *cpp[14:16] ]
        # self.play( *map(ftc, anim) )
        #
        # # finally, we'll update the prefix sum with our newly computed dp value
        # anim = [ py[12], cpp[17] ]
        # self.play( *map(ftc, anim) )
        #
        # # and if the initial state of the current portal was *open*, then
        # # let's add that to our total cost
        # anim = [ *py[13:15], *cpp[18:20] ]
        # self.play( *map(ftc, anim) )
        #
        # # our final answer is just going to be the cost we've gathered so far,
        # # plus the total distance to the end, which is just the final entrance coord + 1
        # anim = [ *py[16:18], *cpp[21:23] ]
        # self.play( *map(ftc, anim) )


        # waste of time    vvvvv
        # arw = Arrow().set_angle(PI)
        # arw.pt = arw.get_center()
        # for i in range( len(lines)-1 ):
        #     if height( lines[i] ) < 1e-2: continue
        #     self.play( Peek(getBoundingBox(lines[i])) )
        #     arw.pt[:2] = code_py(i)
        #     self.play( arw.animate.next_to(arw.pt, RIGHT) )


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

src_cpp = """
#include <bits/stdc++.h>
using namespace std;

int N;
vector<int> X, Y, S;

int solve() {
    int cost = 0;
    vector<int> ps(N+1);
    for (int i = 0; i < N; ++i) {
        int enter = X[i];
        int exit  = Y[i];
        auto it = lower_bound(begin(X), end(X), exit);
        int j = it - begin(X);
        int dist = enter - exit;
        int penalty = ps[i] - ps[j];
        int dp_i = penalty + dist;
        ps[i+1] = ps[i] + dp_i;
        if (S[i] == 1)
            cost += dp_i;
    }
    int end = X.back() + 1;
    return cost + end;
}
"""