import ursina as urs
import time
import itertools

# make center of cube in center should be rounding via center
# make switch case
# make annotations
# rotate colors in cube

rotations = {
    'u': ('y', 1, 90), 'd': ('y', -1, -90),
    'r': ('x', 1, 90), 'l': ('x', -1, -90),
    'f': ('z', -1, 90), 'b': ('z', 1, -90)
}

def rotate(axis, line):  # comment it    | making animation # can call it layer
    for cubie in cubies:
        cubie.position, cubie.rotation = \
            round(cubie.world_position, 1), cubie.world_rotation  # maybe unused in future
        # print('real', cubie.position, cubie.rotation)
        # print('word', cubie.world_position, cubie.world_rotation)
        cubie.parent = urs.scene
    center.rotation = 0

    for cubie in cubies:
        if eval(f'cubie.{axis}') == line:
            cubie.parent = center


def input(key):
    if key not in rotations:
        return
    action = False
    axis, line, rotation_degree = rotations[key]
    shift = urs.held_keys['shift']
    # if action:
    rotate(axis, line)
    rotation_degree = rotation_degree if not shift else -rotation_degree
    eval(f'center.animate_rotation_{axis}({rotation_degree}, duration=.5)')
    # urs.invoke(not action, delay=.5 + .11)


class Cubie(urs.Entity):
    def __init__(self, coord):
        super().__init__()
        self.model = 'kek2.obj'
        self.scale = .5
        self.position = coord
        self.i = 1 if coord == (1, 1, 1) else 0

        # if self.y == 0:
        #     self.color = urs.color.black
        # if pos == (-1, -1, -1):
        # if pos == (1, 1, 1):Q
        #     self.color = urs.color.black

        # self.target position
        # self.real position


app = urs.Ursina()

center = urs.Entity()
cubies = list()
for coordinates in itertools.product((-1, 0, 1), repeat=3):
    cubies.append(Cubie(coordinates))

action = True


urs.EditorCamera()
# ursina.camera.position = (0, 0, 10)

app.run()
