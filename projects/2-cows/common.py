from manim import *
from core import *
from random import choice

class Cow(ABWComponent):
    def __init__(self, **kwargs):
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


class CoordinateList(ABWComponent):
    def __init__(self, **kwargs):
        props = {
            "coords": [],
            "coords_mobs": [],
            "scale": 1
        }
        my = self.props = Namespace(props, kwargs)
        mobs = {
            "starter": Circle(stroke_width=0, fill_opacity=0, radius=0)
        }
        super().__init__(my, mobs, kwargs)

    def append(self, mob, pair):
        my = self.props
        my.coords.append(pair)
        my.coords_mobs.append(mob)
        self.mob.add(mob)

    def AddWithFade(self, x, y):
        my = self.props
        mobs = []
        for s in f"({x},{y})":
            mobs.append(MathTex(s))
            mobs[-1].next_to(self.mob, RIGHT, buff=.1*my.scale).scale(my.scale)
            self.mob.add(mobs[-1])
        self.mob.remove(*mobs)
        mobs[2].shift(DOWN*.2*my.scale)
        new_mob = VGroup(*mobs)
        self.append(new_mob, (x, y))
        return FadeIn(new_mob)

    def AddFromAxes(self, x, y, grid, rf=smooth):

        my = self.props
        pre = ',' if my.coords else ''
        mobs = []
        for s in f"{pre}({x},{y})":
            mobs.append(MathTex(s))
            mobs[-1].next_to(self.mob, RIGHT, buff=.1*my.scale)
            self.mob.add(mobs[-1])

        self.mob.remove(*mobs)

        mobs[-3].shift(DOWN*.2*my.scale)
        if len(mobs) == 6:
            mobs[0].shift(DOWN*.2*my.scale)

        x1, y1 = grid.mobs.x_axis[x], grid.mobs.y_axis[y]
        x2, y2 = x1.copy(), y1.copy()
        res = [Transform(x2, mobs[-2], rate_func=rf),
               Transform(y2, mobs[-4], rate_func=rf)]

        mobs.pop(-4)
        mobs.pop(-2)

        res += [FadeIn(x, rate_func=rf) for x in mobs]
        new_mob = VGroup(*mobs, x2, y2)
        self.append(new_mob, (x, y))
        return res

    def reset(self):
        my = self.props
        my.coords = []
        res = [FadeOut(x) for x in my.coords_mobs]
        for x in my.coords_mobs:
            self.mob.remove(x)
        my.coords_mobs = []
        return res

    def pop(self, scene):
        nl = self.mob.copy()
        scene.add(nl)
        scene.remove(*self.props.coords_mobs)
        res = tuple(self.props.coords)
        scene.play(*self.reset(), run_time=1/60)
        return nl, res


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
        scene.wait(rt*2)


def n6_alg(grid, scene, rt=1/6):
    pg = grid.sub_grid(0, 0, 0, 0)
    scene.play(FadeIn(pg), run_time=rt)

    for coords in unwrap_coords(grid):
        ng = grid.sub_grid(*coords)
        r = grid.cells_in_rect(*coords)
        scene.play(Transform(pg, ng), run_time=rt)
        scene.wait(rt)
        for x, y, c in r:
            scene.play(c.anim_highlight(RED), run_time=rt/2)
        scene.play(*[c.anim_highlight(BLACK) for x, y, c in r], run_time=rt)

def composite(a):
    total = sum(a)
    running_total = 0
    res = []
    for t in a:
        res.append(squish_rate_func(smooth, running_total/total, (running_total + t)/total))
        running_total += t
    return total, res


def n5_alg(grid, scene, cl, hs, rt=1/6):
    pg = grid.sub_grid(0, 0, 0, 0)
    scene.play(FadeIn(pg), run_time=rt)
    area = 0
    total = []
    flag = False

    for coords in unwrap_coords(grid)[:30]:
        ng = grid.sub_grid(*coords)

        new_area = width(ng) * height(ng)
        if new_area <= area:
            nl, res = cl.pop(scene)
            hs.put(nl, scene, val=res)
            scene.play(*[x.anim_highlight(BLACK) for x in total], run_time=rt)
            total = []
            flag = False

        if flag:
            nl = cl.mob.copy()
            hs.put(nl, scene, val=tuple(cl.props.coords))

        area = new_area

        scene.play(Transform(pg, ng), run_time=rt)

        r = grid.cells_in_rect(*coords)
        flag = False

        t = 0
        anim_queue = []
        sm = (len(r) - len(total)) * rt/2 + rt * 2
        s = smooth
        # sweep
        for x, y, c in r:
            if c not in total:
                if is_cow(c):
                    a = t/sm
                    b = (t+rt/2)/sm
                    anim_queue.append(c.anim_highlight(GREEN,
                                                       rate_func=squish_rate_func(s,a,b)))
                    # scene.wait(rt)
                    # scene.play(*cl.AddFromAxes(x, y, grid), run_time=rt*4)
                    b = (t+rt*2)/sm
                    anim_queue.extend(cl.AddFromAxes(x, y, grid,
                                                      rf=squish_rate_func(s,a,b)))
                    flag = True

                else:
                    a = t/sm
                    b = (t+rt/2)/sm
                    anim_queue.append(c.anim_highlight(RED, rate_func=squish_rate_func(s,a,b)))
                total.append(c)
                t += rt / 2
        scene.play(*anim_queue, run_time=sm)
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
        return True
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
