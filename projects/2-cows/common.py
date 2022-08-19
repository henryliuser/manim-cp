from manim import *
from core import *

class Cow(ABWComponent):
    def __init__(self, **kwargs):
        props = {}
        my = self.props = Namespace(props, kwargs)
        mobs = {}
        super().__init__(my, mobs, kwargs)
