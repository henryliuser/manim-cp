from core import *

class dynamicProgramming(Scene):
    def construct(self):
        sc = 0.55
        FS = 25
        D, L, R = sc*DOWN, sc*LEFT, sc*RIGHT
        RT = 1/8

        def fib(x, pt, A):
            lab = MathTex(f'fib({x})', font_size=FS, fill_opacity=0.6, color=BLUE)
            self.play( Write(lab.move_to(pt)), run_time=RT )
            A += [lab]
            if x in [0,1]: return x
            return fib(x-1, pt+D+L, A) + fib(x-2, pt+D+R, A)
        A = []
        fib(9, 3/2*UP, A)
        self.play( *map(FadeOut, A), run_time=2 )

        DP = Array( [0, 1] + ['?'] * 8 )
        DP.mob.to_edge(UP,buff=1.2)
        idx = [Tex(f"${i}$").move_to(DP(i)).shift(UP) for i in range(10)]
        self.play( Create(DP.mob), *map(Create, idx) )
        dp = DP.og

        def fib_dp(x, pt, A):
            v = dp[x] != '?'
            lab = MathTex(f'fib({x})', font_size=FS, color=RED if v else BLUE)
            A += [lab]
            self.play( Write(lab.move_to(pt)), run_time=RT )
            if v: return dp[x]
            if x in [0,1]: return x
            dp[x] = fib_dp(x-1, pt+D+L, A) + fib_dp(x-2, pt+D+R, A)
            # self.play( Transform(lab), MathTex("") )
            lab = DP[x].mobs.tex
            self.play( Transform(lab, Tex(dp[x]).move_to(lab)), run_time=RT )
            self.play( Indicate(lab), run_time=3*RT )
            return dp[x]
        A = []
        fib_dp(9, UP, A)
        self.play( *map(FadeOut, A), FadeOut(DP.mob), *map(FadeOut, idx) )
    
            