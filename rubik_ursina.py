import itertools
import sys
from typing import List, Tuple

import ursina as urs

from rubik_state import RubikState


class Cubie(urs.Entity):
    def __init__(self, coord: Tuple[int, ...]):
        super().__init__()
        self.model = 'cubie.obj'
        self.position = coord
        self.scale = .5


class RubikVisualizer(urs.Ursina):
    notations = {'L': ('x', -1, -90), 'L2': ('x', -1, -180), 'L\'': ('x', -1, 90), 'L2\'': ('x', -1, 180),
                 'R': ('x', 1, 90), 'R2': ('x', 1, 180), 'R\'': ('x', 1, -90), 'R2\'': ('x', 1, -180),
                 'F': ('z', -1, 90), 'F2': ('z', -1, 180), 'F\'': ('z', -1, -90), 'F2\'': ('z', -1, -180),
                 'B': ('z', 1, -90), 'B2': ('z', 1, -180), 'B\'': ('z', 1, 90), 'B2\'': ('z', 1, 180),
                 'U': ('y', 1, 90), 'U2': ('y', 1, 180), 'U\'': ('y', 1, -90), 'U2\'': ('y', 1, -180),
                 'D': ('y', -1, -90), 'D2': ('y', -1, -180), 'D\'': ('y', -1, 90), 'D2\'': ('y', -1, 180)}

    def __init__(self, shuffled_notations: List[str], solution_notations: List[str]):
        super().__init__()
        urs.EditorCamera()
        urs.window.borderless = False
        urs.window.exit_button.visible = False
        urs.window.fps_counter.enabled = False

        self.shuffled_notations = shuffled_notations
        self.solution_notations = solution_notations
        self.cubies: List[Cubie] = list()
        self.center = urs.Entity()
        self.notation_index = 0
        self.action = True

        self.init_cubies()
        self.make_shuffled_cube()

    def init_cubies(self) -> None:
        for coordinates in itertools.product((-1, 0, 1), repeat=3):
            self.cubies.append(Cubie(coordinates))

    def make_shuffled_cube(self) -> None:
        for notation in self.shuffled_notations:
            self.rotate_side_without_animation(notation)

    def rotate_cubie_positions(self, notation: str) -> Tuple[str, int]:
        axis, layer, rotation_degree = RubikVisualizer.notations[notation]
        for cubie in self.cubies:
            cubie.position, cubie.rotation = round(cubie.world_position, 1), cubie.world_rotation
            cubie.parent = urs.scene
        self.center.rotation = 0

        for cubie in self.cubies:
            if eval(f'cubie.{axis}') == layer:
                cubie.parent = self.center
        return axis, rotation_degree

    def rotate_side_without_animation(self, notation: str) -> None:
        axis, rotation_degree = self.rotate_cubie_positions(notation)
        exec(f'self.center.rotation_{axis} = {rotation_degree}')

    def toggle_animation_trigger(self) -> None:
        self.action = not self.action

    def rotate_side_with_animation(self, notation: str) -> None:
        self.action = False
        axis, rotation_degree = self.rotate_cubie_positions(notation)
        eval(f'self.center.animate_rotation_{axis}({rotation_degree}, duration=.1)')
        urs.invoke(self.toggle_animation_trigger, delay=.35)

    def input(self, key: str) -> None:
        super().input(key)
        if urs.held_keys['space'] and self.action or urs.held_keys['right arrow'] and self.action:
            if self.notation_index < len(self.solution_notations):
                notation_text = urs.Text(text=f'{self.solution_notations[self.notation_index]}',
                                         scale=3, x=.3, y=.3, color=urs.color.white)
                urs.destroy(notation_text, .3)
                self.rotate_side_with_animation(self.solution_notations[self.notation_index])
                self.notation_index += 1
        elif urs.held_keys['left arrow'] and self.action:
            if self.notation_index > 0:
                self.notation_index -= 1
                if len(self.solution_notations[self.notation_index]) == 1 or \
                        '2' in self.solution_notations[self.notation_index]:
                    self.rotate_side_with_animation(self.solution_notations[self.notation_index] + '\'')
                else:
                    self.rotate_side_with_animation(self.solution_notations[self.notation_index].strip('\''))
        elif key == 'escape':
            sys.exit()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit('wrong number of input variables')
    shuffled_notations = sys.argv[1].split()
    solution_notations = sys.argv[2].split()

    if not all(nt in RubikState.possible_notations for
               nt in set(shuffled_notations) | set(solution_notations)):
        sys.exit(f"possible notations: {' '.join([i for i in RubikState.possible_notations])}")
    rubik_visualizer = RubikVisualizer(shuffled_notations, solution_notations)
    rubik_visualizer.run()
