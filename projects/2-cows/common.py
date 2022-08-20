from manim import *
from core import *
from random import choice

class Cow(ABWComponent):
    def __init__(self, **kwargs):
        # props = {
        #     "radius": .3,
        # }
        # my = self.props = Namespace(props, kwargs)
        # r = my.radius
        #
        # skin = Circle(fill_opacity=1, stroke_width=0,
        #            color=WHITE, radius = 1*r)
        # snout = Ellipse(fill_opacity=1, color='#FFA1E0',
        #             stroke_width=0, width=1.1*r, height=.6*r)
        # snout.shift(.7*DOWN*r)
        #
        # eyes = []
        # nostrils = []
        # spot_circles = []
        # for x in [LEFT, RIGHT]:
        #     eyes.append(Circle(fill_opacity=1, stroke_width=0,
        #            color=BLACK, radius = .12*r))
        #     eyes[-1].shift(UP*0*r)
        #     eyes[-1].shift(x*.5*r)
        #
        #     nostrils.append(Ellipse(fill_opacity=1, stroke_width=0,
        #                 width=.12*r, height=.08*r, color=BLACK))
        #     nostrils[-1].move_to(snout)
        #     nostrils[-1].shift(.1 * r * x)
        #     nostrils[-1].shift(DOWN*.08*r)
        #
        #     spot_circles.append(Circle(radius = .8*r))
        #     spot_circles[-1].shift(x*r)
        #     spot_circles[-1].shift(UP * r * .2)
        #
        # # spot_circles.pop()
        # # spot_circles[-1].shift(UP*r*.6)
        #
        # spots = []
        # for x in spot_circles:
        #     spots.append(Intersection(skin, x, color="#633E23",
        #                  fill_opacity=1, stroke_width=1))
        #
        # ordered_parts = [skin, *spots, *eyes, snout, *nostrils]
        # whole_cow = VGroup(*ordered_parts)
        #
        # mobs = {
        #     "cow": whole_cow
        # }
        # super().__init__(my, mobs, kwargs)
        props = {
            "radius": .3,
        }
        my = self.props = Namespace(props, kwargs)
        r = my.radius

        skin = Circle(fill_opacity=1, stroke_width=0,
                   color=WHITE, radius = 1*r)
        snout = Ellipse(fill_opacity=1, color='#FFA1E0',
                    stroke_width=0, width=1.1*r, height=.6*r)
        snout.shift(.7*DOWN*r)

        eyes = []
        nostrils = []
        spot_circles = []
        for x in [LEFT, RIGHT]:
            eyes.append(Circle(fill_opacity=1, stroke_width=0,
                   color=BLACK, radius = .15*r))
            eyes[-1].shift(UP*0*r)
            eyes[-1].shift(x*.3*r)

            nostrils.append(Ellipse(fill_opacity=1, stroke_width=0,
                        width=.12*r, height=.08*r, color=BLACK))
            nostrils[-1].move_to(snout)
            nostrils[-1].shift(.1 * r * x)
            nostrils[-1].shift(DOWN*.08*r)

            spot_circles.append(Circle(radius = .5*r))
            spot_circles[-1].shift(x*r*.7)

        spot_circles.pop()
        spot_circles[-1].shift(UP*r*.6)

        spots = []
        for x in spot_circles:
            spots.append(Intersection(skin, x, color="#5C3B24",
                         fill_opacity=1, stroke_width=1))

        ordered_parts = [skin, *spots, *eyes, snout, *nostrils]
        whole_cow = VGroup(*ordered_parts)

        mobs = {
            "cow": whole_cow
        }
        super().__init__(my, mobs, kwargs)

class HashSet(ABWComponent):
    def __init__(self, **kwargs):
        props = {
            "height": 3,
            "width": 3,
            "color": BLACK,
            "outline": WHITE,
            "count": 0,
            "set": set([-1]),
        }
        my = self.props = Namespace(props, kwargs)
        my.fs = fs =  10*my.width
        mobs = {
            "box": Rectangle(color=my.outline, fill_opacity=1, fill_color=my.color,
                             height=my.height, width=my.width),
            "label": Tex("HashSet", font_size=fs),
            "counter": Integer(my.count, font_size=fs),
            "text": Tex("Distinct subsets: ", font_size=fs),
            "error": Tex("Already counted", font_size = fs, color=RED),
            "success": Tex("New subset", font_size = fs, color=GREEN),
        }

        super().__init__(my, mobs, kwargs)
        my.buffer = my.width*.04
        m = self.mobs
        m.label.shift(UP*.3*my.height)
        m.counter.move_to(m.text).next_to(m.text, RIGHT, buff=my.buffer)
        VGroup(m.text, m.counter).move_to(m.box).shift(UP*.1*my.height)
        m.error.shift(DOWN*.35*my.height).scale(1/10000)
        m.success.move_to(m.error).scale(1/10000)

    def put(self, mob, scene, val=None, rt=1):
        my = self.props
        m = self.mobs

        scale_factor = min(1, (3/4 * my.width) / width(mob))
        mob.generate_target()
        mob.target.move_to(m.box).shift(DOWN*.15*my.height)
        scene.play(ScaleAndMove(mob, scale_factor))

        if val not in my.set or val is None:
            my.set.add(val)
            my.count += 1
            a = Integer(my.count, font_size=my.fs)
            a.move_to(m.counter)
            a.next_to(m.text, RIGHT, buff=my.buffer)

            scene.play(FadeOut(m.success, run_time=1/60))
            m.success.scale(10000)
            scene.play(Create(m.success), run_time=rt/4)
            scene.wait(rt/4)

            r = [FadeOut(m.counter), FadeIn(a), FadeOut(mob), FadeOut(m.success)]
            scene.play(*r, run_time=rt/2)
            self.mob.remove(m.counter)
            m.counter = a
            self.mob.add(m.counter)
            m.success.scale(1/10000)

        else:
            scene.play(FadeOut(m.error, run_time=1/60))
            m.error.scale(10000)
            scene.play(Create(m.error), run_time=rt/4)
            scene.wait(rt/4)
            scene.play(FadeOut(mob), FadeOut(m.error), run_time=rt/2)
            m.error.scale(1/10000)



def make_grid(points):
    n = max(points)[0] + 1
    m = max(points, key=lambda x:x[1])[1] + 1
    mtx = [[None for _ in range(m)] for _ in range(n)]
    for x, y in points:
        mtx[x][y] = Cow().mob
    return Grid(mtx)

def unwrap_coords(grid):
    res = []
    for x1 in range(grid.props.nx):
        for y1 in range(grid.props.ny):
            for x2 in range(x1, grid.props.nx):
                for y2 in range(y1, grid.props.ny):
                    res.append((x1, y1, x2, y2))
    return res

def go_through_rects(coords_list, grid, scene, rt=1/6):
    pg = grid.sub_grid(*coords_list[0])
    scene.play(FadeIn(pg), run_time=rt)
    for coords in coords_list:
        ng = grid.sub_grid(*coords)
        scene.play(Transform(pg, ng), run_time=rt)
        scene.wait(.2)


def n6_alg(grid, scene, rt=1/6):
    pg = grid.sub_grid(0, 0, 0, 0)
    scene.play(FadeIn(pg), run_time=rt)

    for coords in unwrap_coords(grid):
        ng = grid.sub_grid(*coords)
        c = grid.cells_in_rect(*coords)
        scene.play(Transform(pg, ng), run_time=rt)
        scene.wait(rt/2)
        for x in c:
            scene.play(x.anim_highlight(RED), run_time=rt/2)
        scene.play(*[x.anim_highlight(BLACK) for x in c], run_time=rt)

def n5_alg(grid, scene, rt=1/6):
    pg = grid.sub_grid(0, 0, 0, 0)
    scene.play(FadeIn(pg), run_time=rt)
    area = 0
    total = []

    for coords in unwrap_coords(grid):
        ng = grid.sub_grid(*coords)
        c = grid.cells_in_rect(*coords)

        new_area = abs((coords[2] - coords[0] + 1) * (coords[3] - coords[1] + 1))
        if new_area <= area:
            scene.play(*[x.anim_highlight(BLACK) for x in total], run_time=rt)
            total = []
        area = new_area

        scene.play(Transform(pg, ng), run_time=rt)
        for x in c:
            if x not in total:
                scene.play(x.anim_highlight(RED), run_time=rt/2)
        total += c
        scene.wait(rt)

def maps(coords_list):
    x_map, y_map = {}, {}
    for x, y in coords_list:
        x_map[x] = y
        y_map[y] = x
    return x_map, y_map

def is_minimal(coords, x_map, y_map):
    x1, y1, x2, y2 = coords
    if not (x1 in x_map and y1 <= x_map[x1] <= y2):
        return False
    if not (x2 in x_map and y1 <= x_map[x2] <= y2):
        return False
    if not (y1 in y_map and x1 <= y_map[y1] <= x2):
        return False
    if not (y2 in y_map and x1 <= y_map[y2] <= x2):
        return False
    return True

# returns corner coordinates for all minimal enclosures
def minimal_enclosures(grid, pairs):
    x_map, y_map = maps(pairs)
    a = unwrap_coords(grid)
    return [c for c in a if is_minimal(c, x_map, y_map)]

# pass result into make_grid
def gen_random_pasture(num_cows, mx, my):
    x_set = list(range(mx))
    y_set = list(range(my))
    res = []
    for _ in range(num_cows):
        e = (choice(x_set), choice(y_set))
        res.append(e)
        x_set.remove(e[0])
        y_set.remove(e[1])
    return res

def is_cow(cell):
    try:
        val = cell.mobs.val
        return isinstance(val, Cow)
    except AttributeError:
        return False

def compress_grid(coords):
    x_map, y_map = maps(coords)
    sx = {x:i for i, x in enumerate(sorted(y_map.values()))}
    sy = {x:i for i, x in enumerate(sorted(x_map.values()))}
    new_coords = []
    for x, y in coords:
        new_coords.append((sx[x], sy[y]))
    return new_coords