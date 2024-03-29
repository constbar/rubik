## rubik

a project of École 42, where it is necessary to build a rubik 3x3x3 
solver that fits in less than 150 rotations.

the metric for counting rotations is the half-turn metric (HTM). 
only these rotations are possible: 
`L, L2, L', R, R2, R', F, F2, F', B, B2, B', U, U2, U', D, D2, D'`.

rubik's solving algorithm is a 7-step build (white cross, white corners, 
middle layer, etc.).

![](rubik.gif)

this configuration was used to mark the positions of the corners and 
edges of the rubik:

![](ec_pos.png)

### how to use
python 3.10 required.
visualization requires the `ursina` library.

```
python3 rubik.py -s <num of spins> -vis
```
press `spacebar` for solution step

optional arguments:

`-s` set the number of shuffles

`-v` show solution time

`-vis` visualize rubik\'s solution