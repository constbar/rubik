import ursina as urs
import time
import itertools

from termcolor import colored
gre = lambda i: colored(i, 'green')   # del this block
yll = lambda i: colored(i, 'yellow')

# todo:
#   make center of cube in center should be rounding via center
#   make switch case
#   make annotations
#   rotate colors in cube
#   del all ursina text in terminal
#   ubrat' fps number in window
#   if key == 'escape':


class Cubie(urs.Entity):
    def __init__(self, coord):
        super().__init__()
        self.model = 'kek2.obj'
        self.scale = .5
        self.position = coord


class Rubik(urs.Ursina):  # re vis
    ROT = {
        'U': ('y', 1, 90), 'd': ('y', -1, -90),
        'r': ('x', 1, 90), 'L': ('x', -1, -90),
        'f': ('z', -1, 90), 'B': ('z', 1, -90)}

    rotations = {'u': ('y', 1, 90), 'd': ('y', -1, -90),
                 'r': ('x', 1, 90), 'l': ('x', -1, -90),
                 'f': ('z', -1, 90), 'b': ('z', 1, -90)}

    def __init__(self):
        super().__init__()
        urs.EditorCamera()
        self.center = urs.Entity()

        self.cubies = list()
        self.action = True

        for coordinates in itertools.product((-1, 0, 1), repeat=3):
            self.cubies.append(Cubie(coordinates))


    def toggle_animation_trigger(self):  # re
        self.action = not self.action

    def rotate(self, axis, layer):
        self.action = False

        for cubie in self.cubies:
            cubie.position, cubie.rotation = round(cubie.world_position, 1), cubie.world_rotation  # +\n
            cubie.parent = urs.scene

        self.center.rotation = 0

        for cubie in self.cubies:
            if eval(f'cubie.{axis}') == layer:
                cubie.parent = self.center

    def input(self, key):
        super().input(key)
        # maybe space for shufling
        # if key in rotations:

        if key in Rubik.rotations and self.action:
            pass
        else:
            return
        # if key in Rubik.rotations and self.action:
        #     pass
        # else:

        # axis, layer, rotation_degree = Rubik.rotations[key]
        axis, layer, rotation_degree = Rubik.ROT[key]

        self.rotate(axis, layer)

        # eval(f'center.animate_rotation_{axis}({rotation_degree}, duration=.5)')
        eval(f'self.center.animate_rotation_{axis}({rotation_degree}, duration=.1)')

        # if globvar:
        urs.invoke(self.toggle_animation_trigger, delay=.15)
        # urs.invoke(toggle_animation_trigger, delay=.5 + .11)




if __name__ == '__main__':

    rubik = Rubik()
    rubik.run()

    exit()
    # if globvar:
    #     for key in ['R', 'L', 'R', 'L', 'R', 'L', 'R', 'L', 'R', 'L']:
    #         axis, layer, rotation_degree = ROT[key]
    #         shift = urs.held_keys['shift']
    #
    #         rotate(axis, layer)
    #
    #         rotation_degree = rotation_degree if not shift else -rotation_degree
    #         # eval(f'center.animate_rotation_{axis}({rotation_degree}, duration=.5)')
    #         eval(f'center.animate_rotation_{axis}({rotation_degree}, duration=.1)')
    #
    #         # if globvar:
    #         urs.invoke(toggle_animation_trigger, delay=.15)

