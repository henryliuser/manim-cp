from manim import *
from core import *

class actually_funny(Scene):
    def construct(self):
        @cluster
        def eq():
            x = 5
            vg = VGroup( Rectangle(), Circle() )
            self.play( Create(MathTex("123")) )
            print((x + 1) * 3)
            y = 2 + x - 10 * 2

        self.play( Create(eq.vg.to_edge(UP)) )
        self.play( Create(Mono(rf"{eq.x, eq.y, [*all_vmobs_in(eq)]}").to_edge(DOWN)) )
        self.wait()

class opa(Scene):
    def construct(self):
        self.camera.background_color=WHITE
        i = ImageMobject("pic.png").scale(2)
        self.play( FadeIn(i) )
        self.wait()
        self.play( FadeOut(i) )
        self.wait()


class test(Scene):
    def construct(self):
        a = Array.Element(value=8)
        b = Array.Element(value=5)
        ab = VGroup(a.mob.to_edge(LEFT), b.mob.to_edge(RIGHT))
        c = Array.Element(value=13)
        self.play( Create(ab) )
        # self.play( Create(c.mob.to_edge(DOWN)) )
        self.play( Transform(ab, c.mob.to_edge(DOWN)) )


# class MovingZoomedSceneAround(ZoomedScene):
#     def __init__(self, **kwargs):
#         ZoomedScene.__init__(
#             self,
#             zoom_factor=0.3,
#             zoomed_display_height=1,
#             zoomed_display_width=6,
#             image_frame_stroke_width=20,
#             zoomed_camera_config={
#                 "default_frame_stroke_width": 3,
#                 },
#             **kwargs
#         )
#
#     def construct(self):
#         dot = Dot().shift(UL * 2)
#         image = ImageMobject(np.uint8([[0, 100, 30, 200],
#                                        [255, 0, 5, 33]]))
#         image.height = 7
#         frame_text = Text("Frame", color=PURPLE, font_size=67)
#         cam_text = Text("Zoomed camera", color=RED, font_size=67)
#
#         self.add(image, dot)
#         cam = self.zoomed_camera
#         display = self.zoomed_display
#         frame = cam.frame
#         zoomed_display_frame = display.display_frame
#
#         frame.move_to(dot)
#         frame.set_color(PURPLE)
#         zoomed_display_frame.set_color(RED)
#         display.shift(DOWN)
#
#         zd_rect = BackgroundRectangle(display, fill_opacity=0, buff=MED_SMALL_BUFF)
#         self.add_foreground_mobject(zd_rect)
#
#         unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(display))
#
#         frame_text.next_to(frame, DOWN)
#
#         self.play(Create(frame), FadeIn(frame_text, shift=UP))
#         self.activate_zooming()
#
#         self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)
#         cam_text.next_to(zoomed_display_frame, DOWN)
#         self.play(FadeIn(cam_text, shift=UP))
#         # Scale in        x   y  z
#         scale_factor = [0.5, 1.5, 0]
#         self.play(
#             frame.animate.scale(scale_factor),
#             display.animate.scale(scale_factor),
#             FadeOut(cam_text),
#             FadeOut(frame_text)
#         )
#         self.play(frame.animate.to_edge(RIGHT), display.animate.to_edge(DOWN+LEFT))
#         self.wait(3)
#
# class Test2(Scene):
#     def construct(self):
#         BB = Rectangle(height=3, width=6, fill_opacity=1, fill_color=BLACK, color=WHITE)
#         self.play( GrowFromCenter(BB) )
#         p = MathTex("penalty_i = \,\,?")
#         self.play( Write(p) )
#
#         self.wait(3)