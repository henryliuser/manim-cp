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
    for row,col,c in A.all_cells():
        if is_cow(c):
            x = len(idxs)
            i = make_num(c.mob, x)
            idxs += [i]
            cows += [ (row,col,c) ]
    return idxs, cows


# constants
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
        cows = [ (0,1), (1,3), (2,7), (3,2), (4,6), (5,0), (6,5), (7,4) ]
        N = len(cows)
        grid = make_grid(cows, scale=0.6)
        grid.make_axes()
        arr = make_grid( [(0,i) for i in range(N)], scale=0.6 )
        pos = center(MID_MID, MID_LEFT) + 1/2 * DOWN
        self.play( Create(grid.mob.move_to(pos)) )


        # we can loop through all the cells in the grid and try to do something with each cell
        self.play( Write(code0) )
        for _,_,c in grid.all_cells():
            self.play( color(c, GOLD, rate_func=flash), run_time=1/16 )
            
        self.wait()
        
        # or alternatively, we can loop on unique pairs of Cows and try something from that angle
        self.play( Write(code1) )
        
        pos = center(MID_MID, MID_RIGHT) + 1/2 * DOWN
        self.play( Create(arr.mob.move_to(pos)) )
        for i in range(N-1):
            for j in range(i+1,N):
                a  = arr[0][i]
                b  = arr[0][j]
                ca = color(a, PINK, rate_func=flash)
                cb = color(b, BLUE, rate_func=flash)
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

        idxs0, cows0 = make_indices(grid)
        idxs1, cows1 = make_indices(arr)
        self.play( *map(Write, idxs0+idxs1) )

        # ===============================================
        def demo(i, j, rt=1/5, hijack=None):
            a,(r1,c1,b) = idxs0[i], cows0[i]
            c,(r2,c2,d) = idxs0[j], cows0[j]
            e,(__,__,f) = idxs1[i], cows1[i]
            g,(__,__,h) = idxs1[j], cows1[j]

            cb = color(b, PINK)
            cd = color(d, BLUE)
            cf = color(f, PINK)
            ch = color(h, BLUE)
            reset = [ color(u, "#005400") for u in (b,d,f,h) ]
            # todo: transform tb,bb
            tb = align_corner( Hori(4.8), grid[r1](0), UP, LEFT )
            bb = align_corner( Hori(4.8), grid[r2](0), DOWN, LEFT )
            self.play( cb,cd,cf,ch, run_time=rt )
            self.wait(1/5)
            self.play( *FadeInMany(tb,bb), run_time=rt )
            self.wait(1/5)
            if hijack: exec( inline(hijack) )
            self.play( *FadeOutMany(tb,bb), *reset, run_time=rt )
        
        def extensions():
            # with this construction in place...
            # TODO: partial fade the stuff not within the bounds
            if c1 > c2: c1,c2 = c2,c1
            lb = align_corner( Vert(4.8), grid[0](c1), UP, LEFT )
            rb = align_corner( Vert(4.8), grid[0](c2), UP, RIGHT )
            self.play( *FadeInMany(lb,rb), run_time=rt )
            self.wait()

            # TODO: highlight the cows
            self.play( align_corner(lb.animate, grid[0](c1-1), UP, LEFT)  )
            self.play( align_corner(rb.animate, grid[0](c2+1), UP, RIGHT) )
            self.wait()
            self.play( align_corner(lb.animate, grid[0](c1-3), UP, LEFT)  )
            self.play( align_corner(rb.animate, grid[0](c2+2), UP, RIGHT) )
            self.wait()

            # graphically then, we need to count the number of cows
            # in these two regions. 
            reset  = [ align_corner(lb.animate, grid[0](c1), UP, LEFT)  ]
            reset += [ align_corner(rb.animate, grid[0](c2), UP, RIGHT) ]
            self.play( *reset )

            anims, re = [], []
            for c in grid.rect_cells(1,0,6,2) + grid.rect_cells(1,6,6,7):
                anims += [ color(c, ORANGE) ]
                re    += [ color(c, "#005400") ]
            self.play( *anims )
            self.play( *re )

            # counting them manually will take O(N^2) time
            anims, re = [], []
            for c in grid.rect_cells(1,0,6,2) + grid.rect_cells(1,6,6,7):
                self.play( color(c, ORANGE, run_time=1/15) )
                re    += [ color(c, "#005400") ]
            self.play( *re )

            # using maps will let us conut in O(N) time
            re = []
            for y in [ *range(c1-1, -1, -1), *range(c2+1, 8) ]:
                anim = [] 
                for x in range(1,7):
                    cell = grid[x][y]
                    anim += [ color(cell, ORANGE) ]
                    re   += [ color(cell, "#005400") ]
                self.play( *anim )
            self.play( *re )
            
            self.play( *FadeOutMany(lb,rb) )
        # ===============================================

        cow_pairs = all_pairs(N)
        for i,j in cow_pairs:
            demo(i,j)

        self.wait()
        i,j = cow_pairs[11]
        demo(i, j, 2/3, extensions)
        self.wait()
