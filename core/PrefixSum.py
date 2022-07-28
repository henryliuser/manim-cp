from core import *
from manim import *

db = 0
# [l,r] inclusive query bounds, 0-indexed
def anim_psum_query1(scene:Scene, l:int, r:int, A:Array, PS:Array, **kwargs):
    global db
    if r < l: return
    top  = kwargs.pop('anim_pos', UP)
    SF   = kwargs.pop('scale_factor', 1)
    arc  = kwargs.pop("show_arc", False)
    tf   = kwargs.pop("send_to", lambda x : None)

    anim = []
    if arc:
        lp = A(l).get_center() + 0.6*UP + 0.2*LEFT
        rp = A(r).get_center() + 0.6*UP + 0.2*RIGHT
        arc = ArcBetweenPoints(start=lp, end=rp, angle= -PI/2)
        anim += [ Create(arc, rate_func=flash) ]

    Y = LIGHT_BROWN
    val   = lambda X,i   : X[i].props.val
    light = lambda X,i,c : X[i].anim_highlight(c, run_time=1.5) 
    bazzz = lambda X,i,c : X[i].anim_highlight(c, run_time=1.5, rate_func=flash)

    anim += [ light(A,j,Y) for j in range(l,r+1) ]
    scene.play( *anim ) 
    anim  = [ bazzz(PS, r+1, Y), bazzz(PS, l, Y) ]
    scene.play( *anim ) 
    anim = [ light(A,j,BLACK) for j in range(l,r+1) ]
    scene.play( *anim )

    eb, mb = A[:r+1]
    es, ms = A[:l]
    

    anim = [ mb.animate.shift(3*UP) ]
    if es: anim += [ ms.animate.shift(2*UP) ]
    scene.play( *anim )


    if es:
        slice = Rectangle(color=RED, fill_opacity=1, fill_color=RED, height=3, width=0.02)
        mid = midpoint( es[-1].mob.get_center(), eb[l].mob.get_center() )
        slice.move_to(mid)
        anim = [ Peek(slice, 1.3) ]
        for i in range(l):
            anim += [ *map(FadeOut, [es[i].mob, eb[i].mob]) ]
        scene.play( *anim )

    anim  = [ FadeOut(eb[i].mob) for i in range(l, r+1) ]
    anim += [ light(PS,i,BLACK) for i in range(len(PS.props.arr)) ]
    anim += [ light(A, i,BLACK) for i in range(len(A.props.arr))  ]
    scene.play( *anim )


def anim_psum_query2():
    pass

