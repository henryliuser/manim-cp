*1-telepanting:*

X incorrect highlight on 1st psum_anim, index 0
X (dist) Line still extends past Y[i], just make 
X highlight src dpi
X self.remove(eq) -> Transform(eqc, dpi)
X eqc -> dpi -> ps should happen centered below eq
X case on S[i]
X fadeout labels when showing dist

X psum:
X dp[l..r] inclusive
X ps[r+1] - ps[r]
X hold dp[l:r]
X hold ps[r], ps[l]
X release dp[l:r]
X slice dp and send_to
X just shift up


squash shit
show i, so i,j intersect is more apparent
0 shows up before 'ans = '


NARRATION NOTES:
-m end vs. ans
-m implicit dp array
-m on j <= i, no ps. this to avoid confusion

--------------------------------------------
*GENERAL:*

core.Array
A.align_to_index(B,i)

refactor ABWComponent to use `cursed.namespace`

tf/revert decorator? 
SaveState(x, x.animate...)
Revert(x)

fix combine 

add combine to bash script