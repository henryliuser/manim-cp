from common import *
from core import *
from manim import *

class p23b(Scene):
    def construct(self):
        listing = CodeBlock(
            code=src_py,
            tab_width=4,
            background_stroke_width=1,
            background_stroke_color=WHITE,
            insert_line_no=True,
            style="monokai",
            font="Monaco",
            font_size=15,
            line_spacing=1.05,
            language="py",
        ).center().to_edge(LEFT)
        self.play( Create(listing) )

        for i in range( len(listing.lines) ):
            self.play( Indicate(listing[i]) )

        # arw = Arrow().set_angle(PI)
        # arw.pt = arw.get_center()
        # for i in range( len(lines)-1 ):
        #     if height( lines[i] ) < 1e-2: continue
        #     self.play( Peek(getBoundingBox(lines[i])) )
        #     arw.pt[:2] = listing(i)
        #     self.play( arw.animate.next_to(arw.pt, RIGHT) )

        self.wait(3)


src_py = """
from bisect import *

def solve(N, X, Y, S):
    cost = 0
    dp = [0] * N
    ps = [0] * (N+1)  # prefix sum
    for i in range(N):
        enter = X[i]
        exit = Y[i]
        j = bisect(X, exit)  # binary search
        dist = enter - exit      
        penalty = ps[i] - ps[j]  
        dp[i] = penalty + dist
        ps[i+1] = ps[i] + dp[i]
        if S[i] == 1:            
            cost += dp[i] 

    end = X[-1] + 1
    return cost + end
    # O(N log N)
"""