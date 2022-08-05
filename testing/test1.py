from manim import *
from core import *

class Correlation(Scene):
    def construct(self):
        ns  = []
        tsc = []

        def lerp(i, j, x):
            dx = tsc[j] - tsc[i]
            dy = ns[j] - ns[i]
            m = dy / dx
            b = ns[i] - m * tsc[i]
            return m * x + b

        @sub_scene
        def arrays():
            NS, TSC = Array(ns), Array(tsc)
            TSC.mob.shift(2*DOWN)
            NS.label = MathTex('ns =').next_to(NS.mob, LEFT)
            TSC.label = MathTex('tsc =').next_to(TSC.mob, LEFT)

            self.play( Create(NS.mob), Create(TSC.mob), Write(NS.label), Write(TSC.label) )

            @cluster
            def query():
                Q = []
                arw = Mono("->").shift(3/2*UP + 5/4*RIGHT)
                qry = Mono("correlate()").next_to(arw, LEFT)
                res = Mono("?").next_to(arw, RIGHT)
                def update_qry(x):
                    m = Mono(f"correlate({x})").next_to(arw, LEFT)
                    return Transform(qry, m)
                def update_res(x):
                    m = Mono(f"{x}").next_to(arw, RIGHT)
                    return Transform(res, m)
            
            def step():
                for i,t in enumerate(query.Q):
                    RT = 1/8 if i else 1/3
                    self.play( query.update_qry(t), query.update_res('?') )
                    j = anim_bisect(self, TSC, t, 'j', RT=RT)
                    x = lerp(j-1, j, t)
                    self.play( query.update_res(x) )
                    self.wait()
        
        @sub_scene
        def lerping():
            pass
            
        @sub_scene
        def graph():
            pass
            
        for _ in range(4):
            next(arrays)