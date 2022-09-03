from core import *
from common import *

# source code
cells_py = """
for r in range(N):        # O(N)
    for c in range(N):    # O(N)
        # use grid[r][c]  # O(1)
"""

cows_py = """
for i in range(N-1):            # O(N)
    for j in range(i+1, N):     # O(N)
        # use cows[i], cows[j]  # O(1)
"""

# helpers
center    = lambda a,b : VGroup(a,b).get_center()
color     = lambda o,col,**kw : o.anim_highlight(col, **kw)

def make_indices(A):
    idxs, cows = [], []
    make_num = lambda c,x : StyleText(f"{x}", color=BLACK, bold=1, font_size=24).move_to(c)
    # make_num = lambda c,x : Tex(f"{x}").move_to(c)
    for _,_,c in A.all_cells():
        if is_cow(c):
            x = len(idxs)
            i = make_num(c.mob, x)
            idxs += [i]
            cows += [c]
    return idxs, cows


# constants
N         = 7
CODE_SF   = 0.7
TOP_MID   = Dot().to_edge(UP, buff=0)
TOP_LEFT  = Dot().to_corner(UP+LEFT, buff=0)
TOP_RIGHT = Dot().to_corner(UP+RIGHT, buff=0)
MID_MID   = Dot()
MID_LEFT  = Dot().to_edge(LEFT, buff=0)
MID_RIGHT = Dot().to_edge(RIGHT, buff=0)
BOT_MID   = Dot().to_edge(DOWN, buff=0)
BOT_LEFT  = Dot().to_edge(DOWN+LEFT, buff=0)
BOT_RIGHT = Dot().to_edge(DOWN+RIGHT, buff=0)

class p27(Scene):
    def construct(self):
        code0 = CodeBlock(
            code=cells_py,
            tab_width=4,
            background_stroke_width=1,
            background_stroke_color=WHITE,
            insert_line_no=True,
            style="monokai",
            font="Monaco",
            font_size=13,
            line_spacing=1.2,
            language="py",
        ).scale(CODE_SF).move_to( center(TOP_MID, TOP_LEFT) ).to_edge(UP)
    
        code1 = CodeBlock(
            code=cows_py,
            tab_width=4,
            background_stroke_width=1,
            background_stroke_color=WHITE,
            insert_line_no=True,
            style="monokai",
            font="Monaco",
            font_size=13,
            line_spacing=1.2,
            language="py",
        ).scale(CODE_SF).move_to( center(TOP_MID, TOP_RIGHT) ).to_edge(UP)

        split = Rectangle(height=50, width=0.02, fill_opacity=1, fill_color=WHITE)
        self.play( FadeIn(split) )

        # so we have an N x N grid
        cows = [ (0,0), (2,6), (1,3), (3,2), (6,5), (4,4), (5,1) ]
        grid = make_grid(cows, scale=0.6)
        arr = make_grid([(0,i) for i in range(N)], scale=0.6)
        pos = center(MID_MID, MID_LEFT) + 1/4 * DOWN
        self.play( Create(grid.mob.move_to(pos)) )


        # we can loop through all the cells in the grid and try to do something with each cell
        self.play( Write(code0) )
        for _,_,c in grid.all_cells():
            self.play( color(c, GOLD, rate_func=flash), run_time=1/16 )
            
        self.wait()
        
        # or alternatively, we can loop on unique pairs of Cows and try something from that angle
        self.play( Write(code1) )
        
        pos = center(MID_MID, MID_RIGHT) + 1/4 * DOWN
        self.play( Create(arr.mob.move_to(pos)) )
        for i in range(N-1):
            for j in range(i+1,N):
                a  = arr[0][i]
                b  = arr[0][j]
                ca = color(a, PINK, rate_func=there_and_back)
                cb = color(b, BLUE, rate_func=there_and_back)
                self.play( ca, cb, run_time=1/5 )

        # let's consider the grid method first.
        self.play( ScaleInPlace(code0, 1.2, rate_func=flash) )
        for _,_,c in grid.all_cells():
            col = GOLD if is_cow(c) else RED
            rt  = 1/2  if is_cow(c) else 1/8
            self.play( color(c, col, rate_func=flash), run_time=rt )

        # that leads us back to the pairs approach.
        self.play( *FadeOutMany(split, code0) )
        self.play( code1.animate.center().to_edge(UP) )
        self.play( ScaleInPlace(code1, 1.2, rate_func=flash) )

        self.wait(2)

        anims = []
        for _,_,c in grid.all_cells() + arr.all_cells():
            if is_cow(c):
                c.mobs.val.save_state()
                anims += [ c.mobs.val.animate.set_opacity(0.35) ]
        self.play( *anims ) 

        idxs0 = make_indices(grid)
        idxs1 = make_indices(arr)
        self.play( *map(Write, idxs0+idxs1) )

        for i,j in all_pairs(N):
            

        self.wait()
