from manim import *
from core import *
from common import *

class sandbox_sam(Scene):
    def construct(self):

        # self.play(Create(a.mob))
        # self.wait(1)
        a = gen_random_pasture(5, 7, 7)
        grid = make_grid(a)
        self.play(Create(grid.mob))
        # self.play(Create(grid.make_axes()))
        self.wait(1)
        # new_grid = make_grid(compress_grid(a))
        # self.play(Transform(grid.mob, new_grid.mob))
        self.wait(1)

        # b = minimal_enclosures(grid, a)
        #
        # go_through_rects(b, grid, self)
        # self.wait(1)

        # p = grid[0][0]
        # adder = p.props.stroke_width/100
        # w, h = p.props.width - adder, p.props.height - adder
        # re = Rectangle(width=w, height=h, color=WHITE,
        #                stroke_width=0, fill_opacity=.3)
        # re.move_to(grid[0][0].mob)
        # self.play(FadeIn(re))
        # re.generate_target()
        # for coords in b[:10]:
        #     ng = grid.sub_grid(*coords)
        #     c = grid.cells_in_rect(*coords)
        #     # re.target.move_to(c[0].mob)
        #     self.play(Transform(pg, ng), run_time=1/6)
        #     # for x in c[1:]:
        #     #     self.wait(1/6)
        #     #     re.target.move_to(x.mob)
        #     #     self.play(MoveToTarget(re), run_time=1/6)
        #     self.wait(.2)
        #     for x in c:
        #         self.play(x.anim_highlight(RED), run_time=1/15)
        #         # self.wait(1/15)
        #     #     self.play(x.anim_highlight(BLACK), run_time=1/60)
        #     self.play(*[x.anim_highlight(BLACK) for x in c], run_time=1/6)
        # self.wait(1)
