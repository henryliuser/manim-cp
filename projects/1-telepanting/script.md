> cut the bullshit. just jump into the problem.
> leave credits in the description.

# problem statement
We have an ant on a road, initially at position 0.
Each second, it crawls right by 1 unit.
It wants to reach the end of the road, but to its surprise,
there are a series of portals in its path. Each portal has
a unique entrance point and exit point, with the exit always being to the left
of the entrance.

Let X[i] be the position of the entrance to the i-th portal.
Let Y[i] be the position of the exit of the i-th portal.
At any given time, an entrance can be either open or closed.
When our ant walks into an open entrance, it instantly teleports to the corresponding exit and closes the entrance.
When the ant crosses a closed entrance, it continues without interruption, opening the entrance as it passes.
In other words, whenever the ant reaches an entrance, it gets toggled on or off.

Our goal is to write a program that computes the total time in seconds for our ant
to pass the rightmost and final entrance, given an initial configuration of the open/closed states.

> add stuff about time limit

# pause and digest
First, let's take a moment to digest that whole problem. ...
For a small road, we can manually simulate the entire process, tracking the time as we go -- that's not so hard.

However, consider a road 1 billion units long with hundreds of thousands of portals. The ant would take (literal) ages, and so would our simulation.


At first glance, it seems like there are just a ton of complicated
moving parts, and, I won't fault you for that. I had absolutely no
idea where to start when I first came across this problem.
In these kinds of situations, the only thing we can really do is grab an example and
start playing around and picking it apart.

> add the sample case to the axis

In the provided sample case, we've got a portal at... *fill in*.
Let's start by walking through a simulation of the process.
It takes us x_0 seconds to get to the first one, then gets teleported back
here to y_0. This time we walk past the first portal, because it's inactive, and
go all the way to the 2nd portal... *easy fill during VO*

There aren't any super obvious footholds here yet, so let's just try to look for any
sort of *trends* to latch on to. See if any pattern jumps out at you.

> rewind the simulation and move it back and forth

# Hunting for patterns
Maybe you've already spotted it. Look at the portals positioned left of the ant
at any given time. It sure looks like they're always open. While it's difficult
to see the immediate value of this fact, noticing any sort of patterns is
still useful in building intuition for the problem, so let's try to explore this
observation a little more.

*The obvious question, then, why is this true and can we prove it?*
Well, at the beginning, it's obviously true - there aren't any portals behind us,
and therefore no closed portals.
Let's see if the property still holds as we walk across new portals.
Assume that all of the portals behind us are open. If we cross a closed portal, it opens, and the property is still true -- everything behind us is still open.
If we instead cross an open portal, it sends us backwards to the left. Since the entrances to the left of us were already open, and we've only moved leftwards, the property is still true.


With a little bit of casework, we've managed to develop an inductive proof for
this observation. Now how does it help us?

# pressing for a solution
At first, it seemed like the configuration of portals in our path could be arbitrary.
With this observation, we know that the state of the portals behind us is consistent and predictible.
Recall that all of the portals only send us backwards. Since it's guaranteed that we reach the end,
then we are guaranteed to make progress at all of these positions between the beginning and end,
because the only way to go forward is to walk forward. So eventually, we will hit each of these
points, some of them we'll hit many times. When we take a portal, we toggle it off, and then  we'll be transported backwards. We may fly through some extremely complicated series of other portals, but there is certainly
> show ant zipping around a series of portals behind us

some point at which we finally return to the portal entrance, and walk across it, flipping it back to active. We also know that if we ever reach a portal, it is Guaranteed that all of the
portals behind us are active -- we proved it earlier. If we're able to compute the time
it takes to return to a portal after entering it, given that all the portals behind it are active,
then we can simply loop across the original portals in order, adding the value as we go
> show previous animation but with every portal, highlighting the fact that
> we're computing this value Per portal

For those who are familiar with it, the recurring nature of the sub-problems we've
explored so far might begin to motivate a dynamic programming solution. If you
aren't sure what that is, you can think of it for now as a technique where we use store
previously computed values to make computing newer ones easier.

To formalize this, let's denote this value as dp[i]: the time it takes to return to the i-th
portal after entering it, given that all of the ones behind it are also active. In other words,
dp[i] is the time penalty of entering this portal when it and all the portals behind it are active. Let's now take a look at what happens when we enter a portal:
> jump to position

I've highlighted this segment in yellow. No matter what series of portals we enter,
we will certainly have to walk this segment in full. Besides that, the time it
takes is just the sum of the time penalties for all of the portals located between the i-th exit,
which is where we just popped out of, and the i-th entrance. We don't have to worry about
the case where some of them are active and some aren't, because if we EVER entered portal
i, it necessarily implies that everything before it is active.

Graphically, we can tell now that dp[i] is equal to the distance between the
exit and entrance, X[i] - Y[i], which is this yellow part,
plus the sum of all the dp values contained in the yellow range.
The cool part is, since these portals all came before us, we already have their dp values!
Whenever we compute dp[i], all of the dp values for the portals before the i-th portal have already been solved for in previous iterations!

For a naive solution, we can just loop across the previous dp values manually,
adding them to our current value only if the position is greater than Y[i]. Once we've computed
all of the dp values, we can just loop once over the input again, and add dp[i] if i is active.
Since we're looping across all previous values to compute each new value of dp,
this yields a time complexity of O(N^2), meaning that in general our algorithm will run in time
for smaller inputs, in the case of this question, up to around N = 5000.

# optimizing!
So that's great! We actually have a working solution in a reasonable time complexity. It's
not quite fast enough to pass the problem under these constraints yet, but, take a minute
to convince yourself that you understand why it works! It's pretty tricky!
As a recap, we first observed that whenever you reach a portal, it's guaranted that
all the portals behind you are active. We then showed that the time penalty
To speed this up, we can quickly find the range of portals contained in this yellow section
using binary search. Since the portals are given to us in sorted order, and also we process them
in sorted order, we can perform a binary search to find the necessary range in O(log(N)).
> binary search animation

But this doesn't help our overall time complexity, because we still need to sum across this range
one by one. Since we're dealing with subarray sums here, it'll be quite helpful to consider
the prefix sum technique, which allows us to query for any subarray sums in constant time, or O(1).
For a brief explanation of prefix sums, imagine we have an array of random numbers and we want
to ask for the sum of a particular range [L,R]. If we have a huge number of these queries, it's
not scalable to sum the values one by one each time. Instead, let's make a new array, storing
the *running* sum at each position. The final element will include the sum of all the numbers in the array. Then, to query the sum of a particular range, we can just take the running sum up to R and subtract it from the running sum up to the element right before L, and the resulting difference
is the new amount added between L and R. If we build a prefix sum across our dp array, and we know that the right bound is fixed at X[i], and we can binary search for the left bound L in O(log N), AND we can find the subarray sum in O(1), then we can compute each new value of dp in O(log N), for a total time complexity of O(N log N). This is absolutely fast enough to pass the constraints,
and is a pretty natural extension of the O(N^2) solution using the very standard techniques of binary search and prefix sums.

I encourage you to digest the solution for a bit, try to implement it yourself, and submit it
to the grader on codeforces. The problem is linked in the description. When you're ready,
come back and resume this video to see my example implementation.

```
from bisect import *  

"""
N: number of portals
X: list of entrance positions
Y: list of exit positions
S: list of initial states
"""
def solve(N, X, Y, S):
    time = 0
    dp = [0] * N
    ps = [0] * (N+1)  # prefix sum
    for i in range(N):
        enter = X[i]
        exit  = Y[i]
        j = bisect_left(X, exit)  # binary search the leftmost portal
        dist = enter - exit       # with an entrance ahead of the i-th exit:
        penalty = ps[i] - ps[j]   # take the subarray sum of these contained portals
        dp[i] = penalty + dist
        ps[i+1] = ps[i] + dp[i]
        if S[i] == 1:
            time += dp[i]         # add it to the total time if it was initially active

    end = X[-1] + 1
    return time + end

==================================

#include <bits/stdc++.h>
using namespace std;

int N;
vector<int> X, Y, S;

int solve() {
    int time = 0;
    vector<int> dp(N), ps(N);
    for (int i = 0; i < N; ++i) {
        int enter = X[i];
        int exit  = Y[i];
        auto it = lower_bound(begin(X), end(X), exit);
        int j = it - begin(X);
        int dist = enter - exit;
        int penalty = ps[i] - ps[j];
        dp[i] = penalty + dist;
        ps[i+1] = ps[i] + dp[i];
        if (S[i] == 1)
            time += dp[i];
    }
    int end = X.back() + 1;
    return time + end;
}
```

# credits
This is CodeForces Global Round 15, Problem F, authored by user *fill*.
The link to the problem, as always, is in the description.
Now, problem F typically indicates that this question is
really quite challenging! Only *{x}%* of participants
*({x} people out {tot})* were actually able to solve it
during the contest. Let's take a look at what kind of problem
would be able to trip up that many people.
