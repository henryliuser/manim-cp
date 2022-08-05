from manim import *
from core import *
from random import random
# class Portal(ABWComponent):
#     rainbow = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
#     DDR = DEFAULT_DOT_RADIUS * 2
#     i = 0
#
#     def __init__(self, **kwargs):
#         props = {
#             "x": 1,
#             "y": 0,
#             "ax": None,
#             "open": True,
#             "color": Portal.rainbow[Portal.i],
#         }
#         my = self.props = Namespace(props, kwargs)
#         r = Portal.DDR if my.open else 0.0001 * Portal.DDR
#         mobs = {
#             'entrance': Dot(radius=1.5 * Portal.DDR, point=my.ax.n2p(my.x), color=my.color),
#             'exit': Dot(radius=.75 * Portal.DDR, point=my.ax.n2p(my.y), color=my.color),
#             'opening': Dot(radius=r, point=my.ax.n2p(my.x), color=BLACK),
#         }
#         super().__init__(my, mobs, kwargs)
#         if self.props.color == Portal.rainbow[Portal.i]:
#             Portal.i = (Portal.i + 1) % len(Portal.rainbow)

class Portal(ABWComponent):
    rainbow = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    DDR = DEFAULT_DOT_RADIUS * 1.9
    i = 0

    def __init__(self, **kwargs):
        props = {
            "x": 1,
            "y": 0,
            "ax": None,
            "open": True,
            "color": Portal.rainbow[Portal.i],
            "label": ''
        }
        my = self.props = Namespace(props, kwargs)
        r = Portal.DDR if my.open else 0.0001 * Portal.DDR
        mobs = {
            'entrance': Dot(radius=1.5 * Portal.DDR, point=my.ax.n2p(my.x), color=my.color),
            'exit': Dot(radius=.75 * Portal.DDR, point=my.ax.n2p(my.y), color=my.color),
            'line': Line(color=BLACK),
            'circ': Circle(radius=Portal.DDR, color=BLACK),
            'opening': Dot(radius=r, point=my.ax.n2p(my.x), color=BLACK),
        }
        super().__init__(my, mobs, kwargs)
        m = self.mobs
        m.circ.move_to(m.entrance)
        top = m.circ.point_at_angle(PI/4)
        bottom = m.circ.point_at_angle(PI/4 + PI)
        m.line.put_start_and_end_on(top, bottom)
        if my.label:
            self.add_label(my.label)
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

    def remove(self, scene : Scene):
        for m in self.mobs:
            scene.remove(m)

    def show_arc(self, func=None, angle=TAU/4, return_mob=False):
        p = self.mobs
        arc = ArcBetweenPoints(start=p.entrance.get_center(),
                               end=p.exit.get_center(),
                               stroke_color=self.props.color,
                               z_index=-2, angle=angle)
        self.mobs.arc = arc
        if return_mob: return arc
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

    def add_label(self, label):
        m = self.mobs
        m.label = Tex(label, font_size=30)
        m.label.move_to(m.entrance)
        m.label.shift(UP*.45)
        self.mob.add(m.label)

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

    def move(self, scene, portals, run_time=1, hl=False):
        a = self.props
        a.pos += 1
        for portal in portals:
            p = portal.props
            if a.pos - 1 == p.x:
                if p.open:
                    a.pos = portal.props.y
                    scene.play(self.anim_pos(run_time=run_time/2),
                               portal.toggle(run_time=run_time/2))
                    if hl:
                        a = hlp(self, portals, run_time=run_time)
                        if a:
                            scene.play(*a)
                    return self.move(scene, portals, run_time=run_time)
                return [portal.toggle(run_time=run_time / 2),
                    self.anim_pos(run_time=run_time)]
        return [self.anim_pos(run_time=run_time)]


class Timer(ABWComponent):
    def __init__(self, **kwargs):
        props = {
            't': 0,
            'label': 't = ',
            'color': WHITE
        }
        my = self.props = Namespace(props, kwargs)
        mobs = {
            'text' : MathTex(my.label, color=my.color),
            'val'  : Integer(my.t),
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
        # self.mob.remove(m.val)
        m.val = a
        # self.mob.add(m.val)
        return r

    def light(self, run_time=1, scale_factor=1.5):
        m = self.mobs
        return [Indicate(VGroup(m.val, m.text), scale_factor=scale_factor,
                         run_time=run_time)]

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
             indi=False, run_time=.5, steps=1000,
             start_pos=0, hl = False, light_sf=1.1):
    if start_pos != -1:
        ant.props.pos = start_pos
        scene.play(ant.anim_pos())
    if t is None:
        t = Timer()
        scene.play(FadeIn(t.mob))
    for _ in range(steps):
        if ant.props.pos == ax.x_range[1]:
            break
        a = []
        if t != -1:
            a = t.tick(run_time=run_time)
        scene.play(*ant.move(scene, portals,
                             run_time=run_time, hl=hl), *a)
        if indi:
            scene.play(*t.light(.3, scale_factor=light_sf))
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

def createPortalsFrom(X, Y, S, ax):
    return createPortals( [*zip(X,Y,S)], ax )


#highlight left portals
def hlp(ant, portals, run_time=1):
    pos = ant.props.pos
    a = []
    for p in portals:
        if p.props.x >= pos:
            break
        rf = there_and_back
        a.append(ScaleInPlace(p.mobs.entrance, 1.5, rate_func=rf, run_time=run_time))
        a.append(ScaleInPlace(p.mobs.opening, 1.5, rate_func=rf, run_time=run_time))
    return a

#highlight portals
def hp(portals, run_time=1):
    a = []
    rf = there_and_back
    for p in portals:
        a.append(ScaleInPlace(p.mobs.entrance, 1.5, rate_func=rf, run_time=run_time))
        a.append(ScaleInPlace(p.mobs.opening, 1.5, rate_func=rf, run_time=run_time))
    return a

def portal_map(portals) -> "dict: int -> (mobs, Portal)":
    res = {}
    for p in portals:
        res[p.props.x] = [p.mobs.entrance, p.mobs.opening, p.mobs.circ, p.mobs.line], p
        res[p.props.y] = [p.mobs.exit], p
    return res

def get_element(portals, x) -> "(mobs, Portal)":
    mp = portal_map(portals)
    return mp[x]

def reset_portals(portals, coords):
    a = []
    for p, c in zip(portals, coords):
        if bool(p.props.open) != bool(c[2]):
            a.append(p.toggle())
    return a

def return_trip(scene : Scene, ant, portals, ax, show=True,
                rt=.5, t=None, timer_map={}, dist=None, i=[0]):
    x = ant.props.pos
    d = portal_map(portals)
    z = d[x][0][0]
    if show:
        t = Timer(label=f'cost_{i[0]} = ', color=PINK)
        dist = Timer(label=f'dist_{i[0]} = ', color=YELLOW)
        t.mob.move_to(z)
        t.mob.shift(DOWN * .7)
        t.mob.shift(LEFT*.04)
        dist.mob.move_to(t.mob)
        t.mob.shift(DOWN * .7)
        scene.play(FadeIn(t.mob), FadeIn(dist.mob))

    ant.props.pos = d[x][1].props.y

    if show:
        a = TracedPath(ant.mob.get_center,
                       stroke_color=PURE_RED,
                       stroke_width=3)
        for p in portals:
            scene.add_foreground_mobject(p.mob)
        scene.remove_foreground_mobject(ant.mob)
        scene.add_foreground_mobject(ant.mob)
        scene.add(a)
    scene.play(ant.anim_pos(), d[x][1].toggle(), run_time=rt)

    if show:
        b = TracedPath(ant.mob.get_center,
                       stroke_color=BLUE,
                       stroke_width=3)
        scene.add(b)

    while ant.props.pos != x:
        c = ant.props.pos
        if c in d and d[c][1].props.open and len(d[c][0]) > 1:
            scene.play(Indicate(timer_map[c][0], scale_factor=2), run_time=2)
            # if c != 4:
            #     raise OSError(t.props.label)
            # return_trip(scene, ant, portals,  glax, show=False,
            #             rt=.1, t=t)
            s = timer_map[c][1]
            simulate(scene, ant, portals, ax, run_time=.1, indi=False,
                     t=t, steps=s, start_pos=-1)

        simulate(scene, ant, portals, ax, run_time=rt, indi=False,
                 t=dist, steps=1, start_pos=-1)

    if show:
        total = t.props.t + dist.props.t
        label = Tex(f"$dp_{i[0]} = {total}$")
        label2 = Tex(f"${total}$")
        i[0] += 1
        label.move_to(z).shift(UP*.45)
        label.scale(.5)
        label2.move_to(label)
        label2.scale(.5)
        a = VGroup(t.mobs.val, dist.mobs.val)
        scene.play(FadeOut(t.mobs.text), FadeOut(dist.mobs.text), Transform(a, label), run_time=.5)
        scene.play(Transform(a, label2), run_time=.5)
        timer_map[x] = [a, total]
    return timer_map
