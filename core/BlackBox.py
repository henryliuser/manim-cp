from manim import *
from core import *

# Pass the scene in, so that we can handle moving to front.
class BlackBox(Rectangle):
    def __init__(self, scene, outline=WHITE, **kwargs):
        super().__init__(color=outline, fill_opacity=1, fill_color=BLACK, **kwargs)
        scene.add_foreground_mobject(self)
        scene.bring_to_front(self)


# class Cloud(VGroup):
#     def __init__(self, height, width, n_bumps, opacity=0.5, color=BLUE, **kwargs):
#         super().__init__(**kwargs)
#         bw = width / n_bumps
#         for _ in range(n_bumps):
#             e = Ellipse(width=bw*2.5, height=height, fill_opacity=1, color=color )
#             self.add(e)
#         self.arrange(RIGHT, buff=-0.5)
#         self.fill_opacity=opacity
#
