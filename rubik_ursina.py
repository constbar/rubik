import ursina as urs
import time
import itertools

from termcolor import colored
gre = lambda i: colored(i, 'green')   # del this block
yll = lambda i: colored(i, 'yellow')

# make center of cube in center should be rounding via center
# make switch case
# make annotations
# rotate colors in cube
# del all ursina text in terminal
# ubrat' fps number in window

globvar = True

def rotate(axis, layer):
    global globvar
    globvar = False

    for cubie in cubies:
        cubie.position, cubie.rotation = round(cubie.world_position, 1), cubie.world_rotation  # +\n
        cubie.parent = urs.scene

    center.rotation = 0

    for cubie in cubies:
        if eval(f'cubie.{axis}') == layer:
            cubie.parent = center


def toggle_animation_trigger():
    global globvar
    globvar = not globvar


def input(key):
    # maybe space for shufling
    # if key in rotations:

    global globvar
    # if key not in rotations:
    if key in rotations and globvar:
        pass
    else:
        return

    axis, layer, rotation_degree = rotations[key]  # sloj
    # print('axis, layer, rotation_degree =', axis, layer, rotation_degree)
    shift = urs.held_keys['shift']

    rotate(axis, layer)

    rotation_degree = rotation_degree if not shift else -rotation_degree
    # eval(f'center.animate_rotation_{axis}({rotation_degree}, duration=.5)')
    eval(f'center.animate_rotation_{axis}({rotation_degree}, duration=.1)')

    # if globvar:
    urs.invoke(toggle_animation_trigger, delay=.15)
    # urs.invoke(toggle_animation_trigger, delay=.5 + .11)

import time

"""
def input(key):
    # maybe space for shufling
    # for space add text 1st rotate than solve
    if key not in 'space':
        return
    # action = False
    # for i in ['R', 'L', 'B']:
    for i in ['R']:
        axis, layer, degree = ROT[i]
        print(axis, layer, degree)
        rotate(axis, layer)
        eval(f'center.animate_rotation_{axis}({degree}, duration=.5)')

    print(key)
"""

class Cubie(urs.Entity):
    def __init__(self, coord):
        super().__init__()
        self.model = 'kek2.obj'
        self.scale = .5
        self.position = coord
        # self.i = 1 if coord == (1, 1, 1) else 0 # center poistion

        # if self.y == 0:
        #     self.color = urs.color.black
        # if pos == (-1, -1, -1):
        # if pos == (1, 1, 1):Q
        #     self.color = urs.color.black

        # self.target position
        # self.real position

if __name__ == '__main__':
    # print(globvar)
    # toggle_animation_trigger()
    # print(globvar)
    # /exit()

    rotations = {
        'u': ('y', 1, 90), 'd': ('y', -1, -90),
        'r': ('x', 1, 90), 'l': ('x', -1, -90),
        'f': ('z', -1, 90), 'b': ('z', 1, -90)
    }
    ROT = {
        'U': ('y', 1, 90), 'd': ('y', -1, -90),
        'R': ('x', 1, 90), 'L': ('x', -1, -90),
        'f': ('z', -1, 90), 'B': ('z', 1, -90)
    }

    app = urs.Ursina()
    urs.EditorCamera()
    center = urs.Entity()
    # print(gre(center))
    # print(gre(center.rotation))

    cubies = list()
    for coordinates in itertools.product((-1, 0, 1), repeat=3):
        cubies.append(Cubie(coordinates))

    # urs.camera.position = (1, 1, 10) 0 0 10
    app.run()

