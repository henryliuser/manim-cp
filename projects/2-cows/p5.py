from manim import *
from core import *
from common import *
from random import randint


class p5(Scene):
    def construct(self):

        cows = [(0, 0), (1, 1), (2, 2)]

        # Our first thought may be to try each subset and see if
        # it’s possible to enclose only those cows. 
        grid = make_grid(cows)
        self.play(FadeIn(grid.mob.shift(DOWN)))
        possible = Tex("Possible subsets", color=GREEN_E).shift(UP*2)
        impossible = Tex("Impossible subset", color=PURE_RED).move_to(possible)

        self.play(Create(possible))

        # Here, we try to enclose only the cows highlighted blue.

        pg = gtr_enlarge(minimal_enclosures(grid, cows), grid, self, rt=1/3)

        # In this case, we cannot enclose these cows without enclosing the cow in the center, 
        # making this an impossible subset.
        a = [ScaleInPlace(grid[x][y].mobs.val, 1.4) for x, y in cows[::2]]
        a.extend(grid[x][y].anim_highlight(BLUE) for x, y in cows[::2])
        self.play(*a, run_time=1/3)
        self.wait(1)
        self.play(Transform(pg, grid.sub_grid(0, 0, 2, 2)), run_time=1/3)


        self.play(Transform(possible, impossible),
                  grid[1][1].anim_highlight(PURE_RED), run_time=1/3)

        fades = [possible, grid.mob, pg]

        self.wait(5)

        self.play(*[FadeOut(x) for x in fades])
        # However, this approach proves to be problematic.
        # Each additional cow doubles the number of possible subsets,
        # because we now ust consider every subset with that cow,
        # and every subset without that cow.

        label = Tex("Number of subsets = ").shift(UP + LEFT)
        self.add(label)
        start = MathTex(0).next_to(label)

        i = 1
        cows = [(x // 10, x % 10) for x in range(20)]
        grid = make_grid(cows, spot=DARK_BROWN, scale=1, 
                color=BLACK, outline_color=BLACK)
        grid.mob.shift(DOWN)
        for x, y in cows:
            i *= 2
            self.play(FadeIn(grid[x][y].mobs.val),
                      Transform(start, MathTex(i).next_to(label)),
                      run_time=.2)

        # Even if we had an efficient
        # method to check whether a subset has a valid enclosure,
        self.wait(8)
        fades = [grid.mob, label, start]
        self.play(*[FadeOut(x) for x in fades])


        s = "375828023454801203683362418972386504867736551759258677056523839782231681498337708535732725752658844333702457749526057760309227891351617765651907310968780236464694043316236562146724416478591131832593729111221580180531749232777515579969899075142213969117994877343802049421624954402214529390781647563339535024772584901607666862982567918622849636160208877365834950163790188523026247440507390382032188892386109905869706753143243921198482212075444022433366554786856559389689585638126582377224037721702239991441466026185752651502936472280911018500320375496336749951569521541850441747925844066295279671872605285792552660130702047998218334749356321677469529682551765858267502715894007887727250070780350262952377214028842297486263597879792176338220932619489509376"
        s = "123"
        ns = []
        for i, x in enumerate(s):
            if i % 55 == 0:
                ns.append("\n")
            ns.append(x)


        biggest_num = Tex(''.join(ns)).scale(.8)
        equation = MathTex("2^{2500} = 3.7 \\times 10^{753}")
        atoms_mob = Tex(str(10**39) + '\n' + '0'*40)


        # there are up to 2^2500 subsets of cows, 
        self.play(Create(equation))
        self.wait(3)

        # which equals this absurdly large number,
        # which is considerably
        self.play(Transform(equation, biggest_num))
        self.wait(3)

        # more than the number of atoms in the universe, 
        # shown for comparison.
        label = Tex("Number of atoms in the universe $\\approx$ ")
        label.shift(UP)
        self.play(Transform(equation, atoms_mob), Create(label))
        self.wait(3)
        self.play(*[FadeOut(x) for x in [label, equation]])
