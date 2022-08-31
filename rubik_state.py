from __future__ import annotations

from random import randint
import re
import numpy as np
import copy
from termcolor import colored
from itertools import repeat
from typing import Final
import operator
import pandas as pd

gre = lambda i: colored(i, 'green')
yll = lambda i: colored(i, 'yellow')


class RubikState:
    __slots__ = ('properties', 'cp', 'ep', 'co', 'eo',
                 'faces', 'top', 'left', 'front', 'right',
                 'back', 'bottom',  'notation', 'notation_path')
    cube_size = 3
    num_cube_faces = 6
    clockwise = (1, 0)
    solved_properties = {'corner_position': list(range(8)),
                         'edge_position': list(range(12)),
                         'corner_orientation': [0] * 8,
                         'edge_orientation': [0] * 12}
    solved_faces = 'wwwwwwwwwgggggggggrrrrrrrrrbbbbbbbbboooooooooyyyyyyyyy'
    possible_notations = ('L', 'L2', 'L\'', 'R', 'R2', 'R\'',
                          'F', 'F2', 'F\'', 'B', 'B2', 'B\'',
                          'U', 'U2', 'U\'', 'D', 'D2', 'D\'')

    def __init__(self, properties, faces, notation, notation_path):
        self.properties = RubikState.solved_properties if properties is None else copy.deepcopy(properties)
        self.cp = self.properties['corner_position']
        self.ep = self.properties['edge_position']
        self.co = self.properties['corner_orientation']
        self.eo = self.properties['edge_orientation']

        self.faces = RubikState.solved_faces if faces is None else faces
        self.top, self.left, self.front, \
            self.right, self.back, self.bottom = \
            [np.array(list(self.faces[RubikState.cube_size ** 2 * i:RubikState.cube_size ** 2 * (i + 1)]))
             .reshape(RubikState.cube_size, RubikState.cube_size) for i in range(RubikState.num_cube_faces)]

        self.notation = notation
        self.notation_path = list() if notation_path is None else notation_path

        if self.notation:
            self.make_move(self.notation)
            self.notation_path.append(self.notation)

    def make_move(self, move):
        """
        in the first block of each notation, all permutations of cubies are made according
        to changes in positions and orientations.
        in the first block, the first line is for positions, the second line is for orientations
        in the second block, the movements occur according to faclet-colors
        """
        def l_clockwise():
            self.cp[0], self.cp[4], self.cp[1], self.cp[5] = \
                self.cp[5], self.cp[0], self.cp[4], self.cp[1]
            self.ep[4], self.ep[0], self.ep[5], self.ep[1] = \
                self.ep[1], self.ep[4], self.ep[0], self.ep[5]

            self.left = np.rot90(self.left, axes=RubikState.clockwise)
            self.front[:, [0]], self.top[:, [0]], \
                self.back[:, [2]], self.bottom[:, [0]] \
                = self.top[:, [0]], self.back[:, [2]][::-1], \
                self.bottom[:, [0]][::-1], self.front[:, [0]]

        def r_clockwise():
            self.cp[3], self.cp[7], self.cp[2], self.cp[6] = \
                self.cp[6], self.cp[3], self.cp[7], self.cp[2]
            self.ep[6], self.ep[3], self.ep[7], self.ep[2] = \
                self.ep[2], self.ep[6], self.ep[3], self.ep[7]

            self.right = np.rot90(self.right, axes=RubikState.clockwise)
            self.front[:, [2]], self.top[:, [2]], \
                self.back[:, [0]], self.bottom[:, [2]] \
                = self.bottom[:, [2]], self.front[:, [2]], \
                self.top[:, [2]][::-1], self.back[:, [0]][::-1]

        def f_clockwise():
            self.cp[4], self.cp[3], self.cp[6], self.cp[1] = \
                self.cp[1], self.cp[4], self.cp[3], self.cp[6]
            self.ep[5], self.ep[8], self.ep[6], self.ep[9] = \
                self.ep[9], self.ep[5], self.ep[8], self.ep[6]

            self.co[self.cp[1]] = RubikState.calculate_new_co(self.co[self.cp[1]] + 1)
            self.co[self.cp[3]] = RubikState.calculate_new_co(self.co[self.cp[3]] + 1)
            self.co[self.cp[4]] = RubikState.calculate_new_co(self.co[self.cp[4]] - 1)
            self.co[self.cp[6]] = RubikState.calculate_new_co(self.co[self.cp[6]] - 1)

            self.front = np.rot90(self.front, axes=RubikState.clockwise)
            self.top[[2]], self.right[:, [0]], \
                self.bottom[[0]], self.left[:, [2]] \
                = np.rot90(self.left[:, [2]][::-1]), \
                np.rot90(self.top[[2]])[::-1], \
                np.rot90(self.right[:, [0]][::-1]), \
                np.rot90(self.bottom[[0]])[::-1]

        def b_clockwise():
            self.cp[7], self.cp[0], self.cp[5], self.cp[2] = \
                self.cp[2], self.cp[7], self.cp[0], self.cp[5]
            self.ep[7], self.ep[11], self.ep[4], self.ep[10] = \
                self.ep[10], self.ep[7], self.ep[11], self.ep[4]

            self.co[self.cp[0]] = RubikState.calculate_new_co(self.co[self.cp[0]] + 1)
            self.co[self.cp[2]] = RubikState.calculate_new_co(self.co[self.cp[2]] + 1)
            self.co[self.cp[5]] = RubikState.calculate_new_co(self.co[self.cp[5]] - 1)
            self.co[self.cp[7]] = RubikState.calculate_new_co(self.co[self.cp[7]] - 1)

            self.back = np.rot90(self.back, axes=RubikState.clockwise)
            self.top[[0]], self.right[:, [2]], \
                self.bottom[[2]], self.left[:, [0]] \
                = np.rot90(self.right[:, [2]]), \
                np.rot90(self.bottom[[2]]), \
                np.rot90(self.left[:, [0]]), \
                np.rot90(self.top[[0]])

        def u_clockwise():
            self.cp[0], self.cp[7], self.cp[3], self.cp[4] = \
                self.cp[4], self.cp[0], self.cp[7], self.cp[3]
            self.ep[0], self.ep[11], self.ep[3], self.ep[8] = \
                self.ep[8], self.ep[0], self.ep[11], self.ep[3]

            self.co[self.cp[0]] = RubikState.calculate_new_co(self.co[self.cp[0]] - 1)
            self.co[self.cp[3]] = RubikState.calculate_new_co(self.co[self.cp[3]] - 1)
            self.co[self.cp[4]] = RubikState.calculate_new_co(self.co[self.cp[4]] + 1)
            self.co[self.cp[7]] = RubikState.calculate_new_co(self.co[self.cp[7]] + 1)
            self.eo[self.ep[0]] = (self.eo[self.ep[0]] + 1) % 2
            self.eo[self.ep[3]] = (self.eo[self.ep[3]] + 1) % 2
            self.eo[self.ep[8]] = (self.eo[self.ep[8]] + 1) % 2
            self.eo[self.ep[11]] = (self.eo[self.ep[11]] + 1) % 2

            self.top = np.rot90(self.top, axes=RubikState.clockwise)
            self.front[[0]], self.right[[0]], \
                self.back[[0]], self.left[[0]] \
                = self.right[[0]], self.back[[0]], \
                self.left[[0]], self.front[[0]]

        def d_clockwise():
            self.cp[1], self.cp[6], self.cp[2], self.cp[5] = \
                self.cp[5], self.cp[1], self.cp[6], self.cp[2]
            self.ep[1], self.ep[9], self.ep[2], self.ep[10] = \
                self.ep[10], self.ep[1], self.ep[9], self.ep[2]

            self.co[self.cp[1]] = RubikState.calculate_new_co(self.co[self.cp[1]] - 1)
            self.co[self.cp[2]] = RubikState.calculate_new_co(self.co[self.cp[2]] - 1)
            self.co[self.cp[5]] = RubikState.calculate_new_co(self.co[self.cp[5]] + 1)
            self.co[self.cp[6]] = RubikState.calculate_new_co(self.co[self.cp[6]] + 1)
            self.eo[self.ep[1]] = (self.eo[self.ep[1]] + 1) % 2
            self.eo[self.ep[2]] = (self.eo[self.ep[2]] + 1) % 2
            self.eo[self.ep[9]] = (self.eo[self.ep[9]] + 1) % 2
            self.eo[self.ep[10]] = (self.eo[self.ep[10]] + 1) % 2

            self.bottom = np.rot90(self.bottom, axes=RubikState.clockwise)
            self.front[[2]], self.right[[2]], \
                self.back[[2]], self.left[[2]] \
                = self.left[[2]], self.front[[2]], \
                self.right[[2]], self.back[[2]]

        if isinstance(move, list):
            self.notation_path += move
            for mv in move:
                self.make_move(mv)

        match move:
            case 'L': l_clockwise()
            case 'L2': [l_clockwise() for _ in range(2)]
            case 'L\'': [l_clockwise() for _ in range(3)]
            case 'R': r_clockwise()
            case 'R2': [r_clockwise() for _ in range(2)]
            case 'R\'': [r_clockwise() for _ in range(3)]
            case 'F': f_clockwise()
            case 'F2': [f_clockwise() for _ in range(2)]
            case 'F\'': [f_clockwise() for _ in range(3)]
            case 'B': b_clockwise()
            case 'B2': [b_clockwise() for _ in range(2)]
            case 'B\'': [b_clockwise() for _ in range(3)]
            case 'U': u_clockwise()
            case 'U2': [u_clockwise() for _ in range(2)]
            case 'U\'': [u_clockwise() for _ in range(3)]
            case 'D': d_clockwise()
            case 'D2': [d_clockwise() for _ in range(2)]
            case 'D\'': [d_clockwise() for _ in range(3)]

    @property
    def f_cost(self):
        """
        heuristic function formula is f(n) = g(n) + h(n).
        g(n) is the cost of reaching from the initial state to the current
        one uses the length of the path of the notations.
        """
        return len(self.notation_path) + self.h_cost

    @property
    def h_cost(self):
        """
        estimation of the weights of the rubik's state.
        4 edge positions and 4 edge orientations.
        ▢  11 ▢
        0  ▢  3
        ▢  8  ▢
        """
        top_layer_cross_heuristic = 0
        for i in [0, 11, 3, 8]:
            if self.ep[i] == i:
                top_layer_cross_heuristic += 1
            if self.eo[i] == 0:
                top_layer_cross_heuristic += 1
        return 8 - top_layer_cross_heuristic

    def __lt__(self, other: RubikState) -> bool:
        return self.f_cost < other.f_cost

    def is_target_state(self):
        return self.h_cost == 0

    def make_line_state(self):  # maybe
        make_one_line = lambda matrix: str(matrix.tolist())
        single_array = map(make_one_line, [
            self.top, self.left, self.front, self.right, self.back, self.bottom])
        return ''.join(re.findall(r'[a-z]', str(list(single_array))))

    def __str__(self):
        def sum_lines_np(*matrices):
            final_str = ''
            nums = len(matrices)
            for i in range(RubikState.cube_size):
                for num in range(nums):
                    final_str += matrices[num][i].__str__()
                    final_str += '  ' if num < nums - 1 else ''
                final_str += '\n' if i < nums else ''
            final_str = final_str.replace('][', ' ')
            final_str = re.sub(r'[\[\]\']', '', final_str)
            return final_str

        empty_np = np.full((3, 3), ' ')
        scheme = sum_lines_np(self.left, self.front, self.right, self.back)
        scheme = sum_lines_np(empty_np, self.top) + '\n' + \
            scheme + sum_lines_np(empty_np, self.bottom)

        str_dict = {k: ' '.join(map(str, v)) for k, v in self.properties.items()}
        data = {'position': [str_dict['corner_position'], str_dict['edge_position']],
                'orientation': [str_dict['corner_orientation'], str_dict['edge_orientation']]}
        df = pd.DataFrame.from_dict(data, orient='index').rename(columns={0: 'corner', 1: 'edge'})
        return scheme + '\n\n' + self.make_line_state() + '\n\n' + df.to_string()

    @staticmethod
    def make_random_notations(num):
        random_notations = list()
        for _ in range(num):
            notation = randint(0, 17)
            random_notations.append(RubikState.possible_notations[notation])
        return random_notations

    @staticmethod
    def calculate_new_co(corner_orientation):
        return 2 if corner_orientation == -1 else corner_orientation % 3
