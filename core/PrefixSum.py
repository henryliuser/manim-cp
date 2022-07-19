from core import *
from manim import *

# TODO: figure out all the moving parts
# TODO: show ant: have it progress, abstract entire open portals
# TODO: mark the dp values above the portals
# TODO: do psum anim with the dp labels

# [l,r] inclusive query bounds, 0-indexed
def anim_psum_query(scene:Scene, l:int, r:int, A:Array):
    lp = A(l).get_center() + 0.6*UP + 0.2*LEFT
    rp = A(r).get_center() + 0.6*UP + 0.2*RIGHT
    arc = ArcBetweenPoints(start=lp, end=rp, angle= -PI/2)
    anim = [
        A[j].anim_highlight(LIGHT_BROWN,
          run_time=1.5,
          rate_func=flash)
        for j in range(l,r+1)
    ]
    scene.play( Create(arc), *anim )
    scene.play( FadeOut(arc) )
    eb, mb = A[:r+1]
    es, ms = A[:l]
    anim = [ mb.animate.shift(DOWN) ]
    if es: anim += [ ms.animate.shift(DOWN) ]
    scene.play( *anim )

    # TODO: Transform(PS.Element, Subarray), into the correct place

    if es:
        slice = Rectangle(color=RED, fill_opacity=1, fill_color=RED, height=3, width=0.02)
        mid = midpoint( es[-1].mob.get_center(), eb[l].mob.get_center() )
        slice.move_to(mid)
        anim = [ Peek(slice, 1.3) ]
        for i in range(l):
            anim += [ *map(FadeOut, [es[i].mob, eb[i].mob]) ]
        scene.play( *anim )

    anim = [ FadeOut(eb[i].mob) for i in range(l, r+1) ]
    scene.play( *anim )

def anim_psum_query():
