from core import *
from manim import *

def anim_bisect(scene:Scene, A:Array, x:int, idxName:str, start=-1, end=-1, RT=0.3, scale_factor=1, labs=None, ax=None):
    N = len(A.og)
    idx = MathTex(idxName)
    ldx, rdx = map(MathTex, 'LR')
    dx = [idx, ldx, rdx]
    if labs: dx += [ lidx := MathTex(idxName) ]
    for d in dx: d.font_size=DEFAULT_FONT_SIZE*scale_factor

    if start == -1: start = 0
    if   end == -1:   end = N
    l, r = start, end
    
    gray = lambda i : A[i].anim_highlight(GRAY)
    red  = lambda i : A[i].anim_highlight(RED)
    anim = [ gray(i) for i in range(start, end) ]
    if anim: scene.play( *anim )

    def found(i, col=GREEN):
        scene.play( Transform(idx, idx.copy().next_to(A(i), UP)), run_time=RT )
        scene.play( A[i].anim_highlight(col), run_time=RT )
        scene.wait(0.5)

    
    anim  = [ ldx.next_to(A(0), DOWN) ]
    anim += [ rdx.next_to(A(-1),DOWN) ]
    scene.play( *map(FadeIn, anim), run_time=RT )

    def showLR():
        anim = []
        a,b = l, min(r, N-1)
        off = 0 if a != b else 0.2
        anim += [ Transform(ldx, ldx.copy().next_to(A(a), DOWN).shift(off*LEFT))  ]
        anim += [ Transform(rdx, rdx.copy().next_to(A(b), DOWN).shift(off*RIGHT)) ]
        return anim

    while l < r:
        # move idx
        m = (l+r) >> 1
        if l == 0 and r == N:
            idx.next_to(A(m), UP)
            if labs: lidx.next_to( labs[m].get_center(), 3.2*DOWN )
            anim = [ FadeIn(idx, run_time=RT) ]
        else:
            anim = [ Transform(idx, idx.copy().next_to(A(m), UP), run_time=RT) ]
            if labs: anim += [ Transform(lidx, lidx.copy().next_to(labs[m].get_center(), 3.2*DOWN), run_time=RT) ]
        scene.play( *showLR(), *anim, run_time=RT )

        # split search space
        if A.og[m] >= x: r = m
        else : l = m+1

        # animate search space
        scene.play( A[m].anim_highlight(YELLOW, rate_func=flash, run_time=2*RT) )
        anim = []
        for i in range(start, end):
            if i < l or i > r:
                anim += [ red(i) ]
        if anim: scene.play( *anim, run_time=RT )
    else:
        if l < N and A.og[l] == x:
            found(l)
        elif l < N:
            found(l, BLUE)
        else:
            scene.play( red(l), run_time=RT )

    scene.play( *showLR(), run_time=RT )
    scene.wait(0.5)
    reset = [ A[i].anim_highlight(BLACK) for i in range(N) ]
    scene.play( *reset, *map(FadeOut, dx), run_time=RT )
    
    return l


