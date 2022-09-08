from core import *
from common import *

# helpers
stay_above = lambda dst : lambda o : o.next_to(dst, UP)

def color(o, col, **kwargs):
    return o.anim_highlight(col, **kwargs)

def add_highlight(mob, color, anims, reset, rt=1/2):
    a = mob.anim_highlight(color, run_time=rt)
    b = mob.anim_highlight(BLACK)
    anims.append(a)
    reset.append(b)

def reset_grid(grid):
    return [ color(c, BLACK) for _,_,c in grid.all_cells() ]

def showcase_subgrid(color, special, grid, scene):
    RT = 1/3
    def do_showcase(r1,c1,r2,c2):
        anim, reset = [], []
        # highlight subrectangle
        for i,j in unwrap_rect(r1,c1,r2,c2):
            add_highlight(grid[i][j], color, anim, reset, RT)

        # highlight corners
        scene.play(*anim)
        anim = []
        add_highlight(grid[r1][c1], special, anim, reset, RT)
        add_highlight(grid[r2][c2], special, anim, reset, RT)
        scene.play(*anim)
        scene.play(*reset)
    return do_showcase

def make_cover(grid, r1, c1, r2, c2, color, sf=0.5):
    dx, dy = r2-r1+1, c2-c1+1
    rect = Rectangle(height=dx, width=dy, fill_color=color, fill_opacity=0.6).scale(sf)
    top_left = grid[r1](c1)
    rect.align_to(top_left, LEFT)
    rect.align_to(top_left, UP)
    return rect


class p34(MovingCameraScene):
    def construct(self):
        # Constants
        N = M = 7
        mat = [
            [3, 19,11,14,15, 3,12],
            [16,10,11, 6, 2,12, 4],
            [ 6, 1,15, 5,17, 8, 2],
            [17,10,11, 5, 3, 6, 7],
            [19,12, 2, 3, 1,13,16],
            [ 5,18,14, 9, 2,10, 4],
            [19, 1,13,15, 7, 2,16],
        ]
        examples = [
            (2,3, 6,5),
            (1,2, 5,4),
            (4,5, 5,5),
            (0,2, 3,6),
        ]

        # the goal is to take a rectangular N x M matrix A of numbers, 
        # and answer sub-rectangle sum queries. 
        # (with no updates; the elements never change) 
        @cluster
        def A():
            grid = Grid(mat, outline_color=BLUE, color=BLACK, scale=0.5)
            mob = grid.mob
            anim = mob.animate
            label = Tex("$A$").add_updater( stay_above(mob) )
            self.play( Create(mob), Write(label) )
            
        self.wait()

        # we've already established that each sub-rectangle can be defined by 2 points 
        # or 4 coordinates, so we’re looking to be able to answer queries in the form of 
        # rectSum(r1, c1, r2, c2)
        self.play( A.anim.to_edge(LEFT, buff=2) )

        query_label = Tex("rectSum(r1, c1, r2, c2)").to_edge(RIGHT, buff=1.5)
        self.play( Write(query_label) )
        self.wait()
        self.play( FadeOut(query_label) )
        self.wait()

        
        # the naive implementation sums up the elements manually for each query,
        # resulting in a time complexity of O(QNM) for Q queries
        for rect in examples:
            cur = 0
            funcl = Tex(f"rectSum({  ','.join(map(str, rect))  })")
            arrow = Mono("->")
            resul = Tex("0")
            label = VGroup(funcl, arrow, resul).arrange().to_edge(RIGHT, buff=1.5)
            self.play( Write(label), run_time=1/3 )
            reset = []
            update = lambda x : Transform( resul, Tex(x).next_to(arrow) )

            (r1, c1), (r2, c2) = rect[:2], rect[2:]
            top_left = A.grid[r1][c1].anim_highlight(GOLD, rate_func=flash)
            bot_rigt = A.grid[r2][c2].anim_highlight(GOLD, rate_func=flash)
            self.play( top_left, bot_rigt )
            self.wait(0.5)
            for i,j in unwrap_rect(*rect):
                anim = []
                add_highlight( A.grid[i][j], EMERALD, anim, reset )
                cur += mat[i][j]
                anim += [ update(cur) ]
                self.play(*anim, run_time=1/10)
            self.play( FadeOut(label), *reset )
        
        self.wait() 

        # Now, imagine we had magical matrix ps
        @cluster
        def PS():
            ps = [ [0]*(N+1) for _ in range(M+1) ]
            for i,j in unwrap_rect(1,1,N,M):
                ps[i][j] = mat[i-1][j-1] + ps[i-1][j] + ps[i][j-1] - ps[i-1][j-1]
            grid = Grid(ps, outline_color=BLUE, color=BLACK, scale=0.5)
            mob = grid.mob.align_to(A.mob, DOWN).align_to(A.mob, RIGHT).to_edge(RIGHT, buff=2)
            anim = mob.animate

            group = VGroup( *grid.rect_mobs(1,1,N,M) )

            self.play( Create(group) )
            group = VGroup( *grid.rect_mobs(0,0,0,M), *grid.rect_mobs(1,0,N,0) )
            # TODO: partial fade the ghost cells
            label = Tex("$ps$").add_updater( stay_above(mob) )
            self.play( Create(group), Write(label) )
            group.save_state()
            self.play( Transform(group, group.copy().fade(0.5)) )
            
        # where ps[i][j] contains rectSum(0,0,i,j)
        reset = []
        for i,j in unwrap_rect(1,1,N,M):
            anims = []
            B = PS.grid
            anims += [ color(B[i][j], PINK) ]
            for x,y,cell in B.all_cells():
                col = EMERALD if (0 < x <= i and 0 < y <= j) else BLACK        
                anims += [ color(A.grid[x-1][y-1], col) ]

            anims += reset
            self.play( *anims, run_time=1/10 )
            reset = [ color(B[i][j], BLACK) ]

        off = 1.5*DOWN
        self.play( *reset_grid(A.grid) )
        self.play( A.anim.shift(off+LEFT), PS.anim.shift(off+RIGHT) )
        # self.camera.frame.save_state()
        # w = self.camera.frame.width
        # self.play(self.camera.frame.animate.set_width(w*1.2))
        self.wait( 0.5 )

        @sub_scene
        def formula():
            label   = Tex("rectSum(r1,c1,r2,c2)")
            eq      = Tex("$=$")
            full    = Mono("ps[r2][c2]")
            abov    = Mono("ps[r1-1][c2]")
            left    = Mono("ps[r2][c1-1]")
            smol    = Mono("ps[r1-1][c1-1]")
            terms   = VGroup( full, abov, left, smol ).arrange(DOWN)
            abov.align_to(full, LEFT)
            left.align_to(full, LEFT)
            smol.align_to(full, LEFT)
            sign    = [
                        Tex(""), 
                        Tex("$-$").next_to(abov, LEFT), 
                        Tex("$-$").next_to(left, LEFT), 
                        Tex("$+$").next_to(smol, LEFT),
                    ]
            terms.add(*sign)
            other   = VGroup( label, eq )
            mob     = VGroup( label, eq, terms ).arrange().scale(3/4).to_corner(UP+RIGHT)

            def step():
                yield FadeInMany(full)
                yield FadeInMany(abov, sign[1])
                yield FadeInMany(left, sign[2])
                yield FadeInMany(smol, sign[3])

        # With this construction in place, let’s explore how we can reformulate
        # the sum of an arbitrary subrectangle (r1, c1, r2, c2) in terms of ps.
        rect = examples[1]
        r1,c1,r2,c2 = rect
        self.play( Write(formula.other) )
        
        # the desired subrectangle sum is this blue region
        self.play( *[color(c, MY_BLUE) for c in A.grid.rect_cells(*rect)] )

        full = make_cover(A.grid, 0,0,r2,c2, EMERALD)
        left = make_cover(A.grid, 0,0,r2,c1-1,  PINK)
        abov = make_cover(A.grid, 0,0,r1-1,c2,  PINK)
        smol = make_cover(A.grid, 0,0,r1-1,c1-1, EMERALD)
        thing     = [ full, abov, left, smol ]
        og_things = VGroup( *[o.copy() for o in thing] )
        things    = VGroup( *[o.copy() for o in thing] ).scale(0.4).arrange().center().to_corner(UP+LEFT, buff=1)

        # of course, we'll need the sum of the whole rectangle, 
        # so we might as well start with this full chunk right here, which
        # we can represent as ps[r2][c2]
        hl = color(PS.grid[r2+1][c2+1], EMERALD)
        self.play( hl, FadeIn(full), *next(formula) )

        # now, we've overcounted a bunch. 
        anims, reset = [], []
        def add_rect_color(grid, color, *rect):
            for i,j in unwrap_rect(*rect):
                add_highlight(grid[i][j], color, anims, reset)

        add_rect_color( A.grid, DARK_BROWN, 0,0,r1-1,c2 )  # abov
        add_rect_color( A.grid, DARK_BROWN, 0,0,r2,c1-1 )  # left
        add_rect_color( A.grid,   EMERALD,  r1,c1,r2,c2 )
        # Namely, this brown region right here
        self.play( Transform(full, things[0]), *anims )
        self.wait(2)

        # So, let's try to shave some of those regions off, starting with this top region here.
        # Since we want to get rid of it, we can subtract the sum of this top section, or ps[r1-1][c2].
        hl = color( PS.grid[r1][c2+1], RED )
        self.play( hl, FadeIn(abov), *next(formula) )
        
        anims, reset = [], []
        add_rect_color( A.grid,  BLACK, 0,0,r1-1,c2 )
        self.play( Transform(abov, things[1]), *anims )
        self.wait()
        
        # now here's what we've got.
        # we want to subtract this section on the left as well, so lets chop off a ps[r2][c-1]
        hl = color( PS.grid[r2+1][c1], RED )
        self.play( hl, FadeIn(left), *next(formula) )
        self.wait()

        anims = []
        add_rect_color( A.grid,  BLACK, 0,0,r2,c1-1 )
        add_rect_color( A.grid,  RED, 0,0,r1-1,c1-1 )
        self.play( Transform(left, things[2]), *anims )
        self.wait()

        # finally, we’re left with the following, with this red part having 
        # been double subtracted. Conveniently, it’s already connected to 
        # the origin at (0,0) so we can express its sum as a single term: ps[r1-1][c1-1]
        hl = color( PS.grid[r1][c1], EMERALD )
        self.play( hl, FadeIn(smol), *next(formula) )
        anims = []
        add_rect_color( A.grid,  BLACK, 0,0,r1-1,c1-1 )
        self.play( Transform(smol, things[3]), *anims )
        self.wait()

        self.play( *reset_grid(A.grid), *reset_grid(PS.grid) )


        covers = VGroup(*thing)
        fade = [ A.mob, A.label, PS.mob, PS.label, covers ]
        self.play( *map(FadeOut, fade) )

        # This gives us a general O(1) formula that works for any subrectangle:
        # rectSum(r1,c1,r2,c2) -> ps[r2][c2] - ps[r1-1][c2] - ps[r2][c1-1] + ps[r1-1][c1-1]
        # (where indexing ps out of bounds returns 0)
        f = formula.mob.copy().scale(1.3).center()
        self.play( Transform(formula.mob, f) )
        self.wait()
        self.play( formula.mob.animate.scale(0.7).to_edge(RIGHT) )
        self.wait()

        VGroup(A.mob, og_things).center().to_edge(LEFT, buff=1.75)
        self.play( FadeIn(A.mob), FadeIn(A.label) )

        self.bring_to_front(covers)
        self.play( FadeIn(covers.center().to_edge(UP)) )
        self.play( Transform( covers, og_things ) )
        self.play( FadeOut(covers), *[color(c, MY_BLUE) for c in A.grid.rect_cells(*rect)] )
        self.wait()
        
        # okay great, so now let’s go back to how we construct that magic matrix ps.
        # If we’re clever about it, we can use dynamic programming to precompute the entire matrix in O(NM) time. 
        # again here, since it's pretty well-known, i'll just demonstrate the construction.
        self.play( FadeOut(formula.mob), FadeIn(PS.mob.center().to_edge(RIGHT,buff=1.75) ), FadeIn(PS.label) )

        anims = []
        for _,_,c in PS.grid.all_cells():
            anims += [ c.anim_set_val(0, sf=1/2) ]
        self.play( *anims ) 

        everything = VGroup( *all_vmobs_in(self) )
        self.play( FadeOut(everything) )
        
        @cluster
        def demo():
            get = lambda txt, edge : Tex(txt).to_edge(edge, buff=2)
            grid = Grid( [[0]*6, [0]*6, [0]*6], scale=1 )
            grid.mob.shift(DOWN)
            cover = Rectangle(color=BLUE).match_height(grid.mob).match_width(grid.mob).move_to(grid.mob)
            self.play( Create(cover) )
            a = Array.Element(value='?', color=BLACK, outline_color=BLUE)
            a.mob.align_to(cover,RIGHT).align_to(cover,DOWN)
            self.play( Create(a.mob) )

            @sub_scene
            def alg():
                label   = Mono("ps[i][j]")
                eq      = Tex("$=$")
                this    = Mono("A[i][j]")
                abov    = Mono("ps[i-1][j]")
                left    = Mono("ps[i][j-1]")
                smol    = Mono("ps[i-1][j-1]")
                terms   = VGroup(this, abov, left, smol).arrange(DOWN)
                for x in (abov, left, smol): x.align_to(this, LEFT)
                signs   = [
                    Mono("+").next_to(abov, LEFT),
                    Mono("+").next_to(left, LEFT),
                    Mono("-").next_to(smol, LEFT),
                ]
                VGroup(label, eq, VGroup(*signs, *terms)).arrange().center().to_edge(UP)
                self.play( Write(label), Write(eq) )

                def step():
                    yield FadeInMany(this)
                    yield FadeInMany(abov, signs[0])
                    yield FadeInMany(left, signs[1])
                    yield FadeInMany(smol, signs[2])

            rects  = [ make_cover(grid, 2,5,2,5,    GOLD, sf=1) ]
            rects += [ make_cover(grid, 0,0,1,5, EMERALD, sf=1) ]
            rects += [ make_cover(grid, 0,0,2,4, EMERALD, sf=1) ]
            rects += [ make_cover(grid, 0,0,1,4,     RED, sf=1) ]
            for i in range(4):
                self.play( *next(alg), Create(rects[i]) )
                self.wait()

        # TODO: make 2Dpsum generic utility,
        # TODO: query(r1,c1,r2,c2)
        # TODO: construct(A)

        self.wait(2)
        