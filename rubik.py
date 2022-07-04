import ursina as urs
import time
import itertools

# make center of cube in center should be rounding via center
# make switch case
# make annotations

rotations = {
    'f': ('y', 1, 90),
    # 'f': ()
}

def rotate(axis, line):  # comment it    | making animation
    for cubie in cubies:
        cubie.position, cubie.rotation = \
            round(cubie.world_position, 1), cubie.world_rotation  # maybe unused in future
        # print(cubie.position, cubie.rotation)
        cubie.parent = urs.scene
    center.rotation = 0

    for cubie in cubies:
        if eval(f'cubie.{axis}') == line:
            cubie.parent = center


def input(key):
    if key not in rotations:
         return
    axis, line, rotation_degree = rotations[key]
    # print(axis, line)
    # shift = urs.held_keys['shift']
    # rotate(axis, line)
    rotate('y', 1)
    eval(f'center.animate_rotation_{axis}({rotation_degree}, duration=.5)')


    # if urs.held_keys['f']:
    #     center.animate_rotation_z(90, duration=.5)
    # eval(f'center.animate_rotation_{axis}(90, duration=.5)')  # check spaces in duration

    # if urs.held_keys['q']:
    #     right = [i for i in cubies if i.x == 1]
    #     for i in right:
    #         i.animate_rotation_x(90, duration=.5)
            # i.rotation_x += 90
            # i = urs.scene
        # print([i for i in right])


class Cubie(urs.Entity):
    def __init__(self, coord):
        super().__init__()
        self.model = 'kek2.obj'
        self.scale = .5
        self.position = coord

        if self.y == 0:
            self.color = urs.color.black
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


urs.EditorCamera()
# ursina.camera.position = (0, 0, 10)


app.run()
