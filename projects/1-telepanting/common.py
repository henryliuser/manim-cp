from manim import *
from core import *
from random import random
# prefix sum animation
def psumAnim(A):
    ps = [0]
    for x in A:
        ps += [x + ps[-1]]

    class Main(Scene):
        def construct(self):
            pass


class Portal(ABWComponent):
    rainbow = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    DDR = DEFAULT_DOT_RADIUS * 2
    i = 0

    def __init__(self, **kwargs):
        props = {
            "x": 1,
            "y": 0,
            "ax": None,
            "open": True,
            "color": Portal.rainbow[Portal.i],
        }
        my = self.props = Namespace(props, kwargs)
        r = Portal.DDR if my.open else 0.0001 * Portal.DDR
        mobs = {
            'entrance': Dot(radius=1.5 * Portal.DDR, point=my.ax.n2p(my.x), color=my.color),
            'exit': Dot(radius=.75 * Portal.DDR, point=my.ax.n2p(my.y), color=my.color),
            'opening': Dot(radius=r, point=my.ax.n2p(my.x), color=BLACK),
        }
        super().__init__(my, mobs, kwargs)
        if self.props.color == Portal.rainbow[Portal.i]:
            Portal.i = (Portal.i + 1) % len(Portal.rainbow)

    def toggle(self, run_time=1):
        p = self.props
        m = self.mobs
        p.open = not p.open
        if p.open:
            return ScaleInPlace(m.opening, 10000, run_time=run_time)
        else:
            return ScaleInPlace(m.opening, 0.0001, run_time=run_time)

    def show_arc(self, func=None):
        p = self.mobs
        arc = ArcBetweenPoints(start=p.entrance.get_center(),
                               end=p.exit.get_center(),
                               stroke_color=self.props.color,
                               z_index=-2)
        self.mobs.arc = arc
        if func is not None:
            return Create(arc, rate_func=func)
        return Create(arc)

    def show_arrow(self, func=None):
        s = self.mobs.arc.get_stroke_width()
        arrow = Circle(radius=0.015*s, color=self.props.color,
                       fill_opacity=1, fill_color=self.props.color,
                       z_index=-1)
        self.mobs.arrow = arrow
        if func is not None:
            return MoveAlongPath(self.mobs.arrow, self.mobs.arc, rate_func=func)
        return MoveAlongPath(self.mobs.arrow, self.mobs.arc)
        # self.mobs.arrow = arrow
        # return self.mobs.create_tip.arc()
        # p = self.mobs
        # arrow = ArcBetweenPoints(start=p.entrance.get_center(),
        #                      end=p.exit.get_center(),
        #                      stroke_color=self.props.color,
        #                      z_index=-1)
        # self.mobs.arrow = arrow
        # arrow.add_tip()
        # return FadeIn(arrow)

    def fade_arc(self):
        return FadeOut(self.mobs.arc)

    def fade_arrow(self):
        return FadeOut(self.mobs.arrow)


class Ant(ABWComponent):
    def __init__(self, **kwargs):
        props = {
            "pos": 0,
            "color": PURE_RED,
            "ax": None
        }
        my = self.props = Namespace(props, kwargs)
        DDR = DEFAULT_DOT_RADIUS
        mobs = {
            'dot': Dot(my.ax.n2p(my.pos), color=my.color, radius=DDR * 2.2),
            # 'label': Tex('A', font_size=22, color=invert_color(my.color)).move_to(my.ax.n2p(my.pos)),
            'eye': Dot(my.ax.n2p(my.pos) + UP * .02 + RIGHT * .075,
                       color=BLACK, radius=DDR * .5)
        }
        super().__init__(my, mobs, kwargs)
        self.mob.generate_target()

    def anim_pos(self, run_time=1):
        ax = self.props.ax
        pos = self.props.pos
        self.mob.target.move_to(ax.n2p(pos))
        return MoveToTarget(self.mob, run_time=run_time)

    def move(self, scene, portals, run_time=1):
        a = self.props
        a.pos += 1
        for portal in portals:
            p = portal.props
            if a.pos - 1 == p.x:
                if p.open:
                    a.pos = portal.props.y
                    scene.play(self.anim_pos(run_time=run_time/2),
                               portal.toggle(run_time=run_time/2))
                    return self.move(scene, portals, run_time=run_time)
                return [portal.toggle(run_time=run_time / 2),
                        self.anim_pos(run_time=run_time)]
        return [self.anim_pos(run_time=run_time)]


class Timer(ABWComponent):
    def __init__(self, **kwargs):
        props = {
            't': 0
        }
        my = self.props = Namespace(props, kwargs)
        mobs = {
            'text': Tex(r't = '),
            'val': Integer(my.t),
        }
        super().__init__(my, mobs, kwargs)
        self.mob.arrange(RIGHT)
        self.mob.shift(UP)
        m = self.mobs
        m.val.align_to(m.text)
        # m.val.target.move_

    def tick(self, run_time=1, rate_func=None):
        if rate_func is None:
            if run_time > .2:
                rate_func = squish_rate_func(smooth, .9, 1)
            else:
                rate_func = smooth
        m = self.mobs
        self.props.t += 1
        a = Integer(self.props.t)
        a.move_to(m.val)
        a.next_to(m.text)
        r = [FadeOut(m.val, run_time=run_time, rate_func=rate_func),
             FadeIn(a, run_time=run_time, rate_func=rate_func)]
        m.val = a
        return r

    def light(self, run_time=1):
        m = self.mobs
        return [Indicate(m.val, run_time=run_time),
                Indicate(m.text, run_time=run_time)]

    def fade(self):
        m = self.mobs
        return [FadeOut(m.val), FadeOut(m.text)]

    def reset(self, ant):
        m = self.mobs
        self.props.t = 0
        ant.props.pos = 0
        return [ant.anim_pos(),
                ApplyWave(m.text, run_time=1),
                ApplyWave(m.val, run_time=1),
                m.val.animate.set_value(self.props.t)]

def simulate(scene, ant, portals, ax, t=None,
             indi=True, run_time=.5, steps=1000,
             start_pos=0):
    if start_pos != -1:
        ant.props.pos = start_pos
        scene.play(ant.anim_pos())
    if t is None:
        t = Timer()
        scene.play(FadeIn(t.mob))
    for _ in range(steps):
        if ant.props.pos == ax.x_range[1]:
            break
        scene.play(*ant.move(scene, portals, run_time=run_time),
                  *t.tick(run_time=run_time))
        if indi:
            scene.play(*t.light(.1))
    return t

def portal_arcs(scene, portals, arrow=True):
    scene.play(*[x.show_arc() for x in portals])
    if arrow:
        scene.play(*[x.show_arrow() for x in portals])
    scene.bring_to_back(*[x.mobs.arc for x in portals])
    a = [x.fade_arc() for x in portals]
    if arrow:
        a += [x.fade_arrow() for x in portals]
    a += [Indicate(x.mobs.entrance, run_time=.0001) for x in portals]
    scene.play(*a)

def stagger_arcs(scene, portals, run_time=1, arrow=True):
    A = []
    for p in portals:
        c = random()*.5
        d = random()*.5 + .5
        f = squish_rate_func(smooth, c, d)
        A.append(p.show_arc(f))
    scene.play(*A, run_time=run_time)
    # B = []
    # for p in portals:
    #     c = random()*.5
    #     d = random()*.5 + .5
    #     f = squish_rate_func(smooth, c, d)
    #     B.append(p.show_arrow(f))
    # scene.play(*B, run_time=move_time)
    if arrow:
        scene.play(*[x.show_arrow() for x in portals])

    scene.bring_to_back(*[x.mobs.arc for x in portals])
    a = [x.fade_arc() for x in portals]
    if arrow:
        a += [x.fade_arrow() for x in portals]
    a += [Indicate(x.mobs.entrance, run_time=.0001) for x in portals]
    scene.play(*a)



def createPortals(tuples, ax):
    res = []
    for x, y, o in tuples:
        res.append(Portal(x=x, y=y, open=o, ax=ax))
    return res
