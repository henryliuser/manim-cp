from manim import *
from core import *

# prefix sum animation
def psumAnim(A):
    ps = [0]
    for x in A:
        ps += [ x + ps[-1] ]

    class Main(Scene):
        def construct(self):
            pass

class Portal(ABWComponent):
    rainbow = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
    DDR = DEFAULT_DOT_RADIUS*2
    i = 0
    def __init__(self, **kwargs):
        props = {
            "x": 1,
            "y": 0,
            "ax": None,
            "open": True,
            "color": Portal.rainbow[Portal.i],
            # "entrance_label": ''
        }
        my = self.props = Namespace(props, kwargs)
        r = Portal.DDR if my.open else 0.0001 * Portal.DDR
        mobs = {
            'entrance': Dot(radius=1.5*Portal.DDR, point=my.ax.n2p(my.x), color=my.color),
            # 'entrance_label': Tex(my.entrance_label,font_size=15)
            #     .move_to(my.ax.n2p(my.x)).shift(UP*.33),
            'exit': Dot(radius=.75*Portal.DDR, point=my.ax.n2p(my.y), color=my.color),
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

    def show_arc(self):
        p = self.mobs
        arc = ArcBetweenPoints(start=p.entrance.get_center(),
                             end=p.exit.get_center(),
                             stroke_color=self.props.color,
                             z_index=-2)
        self.mobs.arc = arc
        return Create(arc)

    def show_arrow(self):
        arrow = Circle(radius=.06, color=self.props.color,
                       fill_opacity=1, fill_color=self.props.color,
                       z_index=-1)
        self.mobs.arrow = arrow
        return MoveAlongPath(self.mobs.arrow, self.mobs.arc, run_time=2)
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
        return FadeOut(self.mobs.arc, self.mobs.arrow)



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
            #'label': Tex('A', font_size=22, color=invert_color(my.color)).move_to(my.ax.n2p(my.pos)),
            'eye': Dot(my.ax.n2p(my.pos) + UP * .02 + RIGHT * .075,
                       color=BLACK, radius=DDR * .5)
        }
        super().__init__(my, mobs, kwargs)

    def anim_pos(self):
        ax = self.props.ax
        pos = self.props.pos
        return self.mob.animate.move_to(ax.n2p(pos))

    def move(self, scene, portals):
        a = self.props
        a.pos += 1
        for portal in portals:
            p = portal.props
            if a.pos - 1 == p.x:
                if p.open:
                    a.pos = portal.props.y
                    scene.play(self.anim_pos(), portal.toggle())
                    return self.move(scene, portals)
                return [portal.toggle(run_time=.5), self.anim_pos()]
        return [self.anim_pos()]


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


    def tick(self):
        m = self.mobs
        self.props.t += 1
        return [ApplyWave(m.text, run_time=1),
                ApplyWave(m.val, run_time=1),
                m.val.animate.set_value(self.props.t)]

    def reset(self, ant):
        m = self.mobs
        self.props.t = 0
        ant.props.pos = 0
        return [ant.anim_pos(),
                ApplyWave(m.text, run_time=1),
                ApplyWave(m.val, run_time=1),
                m.val.animate.set_value(self.props.t)]




def createPortals(tuples, ax):
    res = []
    for x, y, o in tuples:
        res.append(Portal(x=x,y=y,open=o,ax=ax))
    return res

