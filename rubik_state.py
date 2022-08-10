from __future__ import annotations
from queue import PriorityQueue
# state0 сделать как шафл
# can @property be with __
# if only one 1 will be type of moovig (cepo or faces) -> make cepo with 1 self withoub self.ce self.po etc.. or maybe 2

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
clockwise = (1, 0) # make upper
counterclockwise = (0, 1)
s_c = 3
num_faces = 6

class State:  # rename like rubik state or cube state
    # goal_edge_permutation = [0] * 12  # better list i belive
    # goal_corner_permutation = '0' * 8
    # goal_edge_orientation = '0' * 12
    # goal_corner_orientation = '0' * 8
    # delete None as default value
    # reorder input vals
    def __init__(self, properties, faces, stage, notation, notation_history):  # here add glubina poiska # nado li dobavit' None avtomatom?? # rename moves history
        self.properties = copy.deepcopy(properties)
        self.cp = self.properties['corner_permutation']
        self.ep = self.properties['edge_permutation']
        self.co = self.properties['corner_orientation']
        self.eo = self.properties['edge_orientation']

        self.faces = faces
        self.top, self.left, self.front, \
            self.right, self.back, self.bottom = \
            [np.array(list(faces[s_c ** 2 * i:s_c ** 2 * (i + 1)]))
             .reshape(s_c, s_c) for i in range(num_faces)]

        self.notation = notation  # if not none
        self.notation_history = notation_history # if not none
        self.stage = 'stage_0' if stage is None else stage

        self.notation_history = list() if notation_history is None else notation_history

        if self.notation:
            self.moves(self.notation)
            self.notation_history.append(self.notation)
            # if self.notation_history:
                # self.notation_history.append(self.notation)
        # self.faces =

    def moves(self, move):  # maybe rename it
        """ !!!!!!!!!!! add description
        the notation with the number 2 makes a double clockwise rotation.
        apostrophe notation makes a counter-clockwise rotation.
        """
        def l_clockwise():
            self.cp[0], self.cp[4], self.cp[1], self.cp[5] = \
                self.cp[5], self.cp[0], self.cp[4], self.cp[1]

            self.ep[4], self.ep[0], self.ep[5], self.ep[1] = \
                self.ep[1], self.ep[4], self.ep[0], self.ep[5]
            ###
            self.left = np.rot90(self.left, axes=clockwise)
            self.front[:, [0]], self.top[:, [0]], \
                self.back[:, [2]], self.bottom[:, [0]] \
                = self.top[:, [0]], self.back[:, [2]][::-1], \
                self.bottom[:, [0]][::-1], self.front[:, [0]]

        def r_clockwise():
            self.cp[3], self.cp[7], self.cp[2], self.cp[6] = \
                self.cp[6], self.cp[3], self.cp[7], self.cp[2]

            self.ep[6], self.ep[3], self.ep[7], self.ep[2] = \
                self.ep[2], self.ep[6], self.ep[3], self.ep[7]
            ###
            self.right = np.rot90(self.right, axes=clockwise)
            self.front[:, [2]], self.top[:, [2]], \
                self.back[:, [0]], self.bottom[:, [2]] \
                = self.bottom[:, [2]], self.front[:, [2]], \
                self.top[:, [2]][::-1], self.back[:, [0]][::-1]

        def f_clockwise():
            self.cp[4], self.cp[3], self.cp[6], self.cp[1] = \
                self.cp[1], self.cp[4], self.cp[3], self.cp[6]

            self.ep[5], self.ep[8], self.ep[6], self.ep[9] = \
                self.ep[9], self.ep[5], self.ep[8], self.ep[6]

            self.co[self.cp[1]] = State.calculate_new_co(self.co[self.cp[1]] + 1)
            self.co[self.cp[3]] = State.calculate_new_co(self.co[self.cp[3]] + 1)
            self.co[self.cp[4]] = State.calculate_new_co(self.co[self.cp[4]] - 1)
            self.co[self.cp[6]] = State.calculate_new_co(self.co[self.cp[6]] - 1)
            ###
            self.front = np.rot90(self.front, axes=clockwise)
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

            self.co[self.cp[0]] = State.calculate_new_co(self.co[self.cp[0]] + 1)
            self.co[self.cp[2]] = State.calculate_new_co(self.co[self.cp[2]] + 1)
            self.co[self.cp[5]] = State.calculate_new_co(self.co[self.cp[5]] - 1)
            self.co[self.cp[7]] = State.calculate_new_co(self.co[self.cp[7]] - 1)
            ###
            self.back = np.rot90(self.back, axes=clockwise)
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

            self.co[self.cp[0]] = State.calculate_new_co(self.co[self.cp[0]] - 1)
            self.co[self.cp[3]] = State.calculate_new_co(self.co[self.cp[3]] - 1)
            self.co[self.cp[4]] = State.calculate_new_co(self.co[self.cp[4]] + 1)
            self.co[self.cp[7]] = State.calculate_new_co(self.co[self.cp[7]] + 1)

            self.eo[self.ep[0]] = (self.eo[self.ep[0]] + 1) % 2
            self.eo[self.ep[3]] = (self.eo[self.ep[3]] + 1) % 2
            self.eo[self.ep[8]] = (self.eo[self.ep[8]] + 1) % 2
            self.eo[self.ep[11]] = (self.eo[self.ep[11]] + 1) % 2
            ###
            self.top = np.rot90(self.top, axes=clockwise)
            self.front[[0]], self.right[[0]], \
                self.back[[0]], self.left[[0]] \
                = self.right[[0]], self.back[[0]], \
                self.left[[0]], self.front[[0]]

        def d_clockwise():
            self.cp[1], self.cp[6], self.cp[2], self.cp[5] = \
                self.cp[5], self.cp[1], self.cp[6], self.cp[2]

            self.ep[1], self.ep[9], self.ep[2], self.ep[10] = \
                self.ep[10], self.ep[1], self.ep[9], self.ep[2]

            self.co[self.cp[1]] = State.calculate_new_co(self.co[self.cp[1]] - 1)
            self.co[self.cp[2]] = State.calculate_new_co(self.co[self.cp[2]] - 1)
            self.co[self.cp[5]] = State.calculate_new_co(self.co[self.cp[5]] + 1)
            self.co[self.cp[6]] = State.calculate_new_co(self.co[self.cp[6]] + 1)

            self.eo[self.ep[1]] = (self.eo[self.ep[1]] + 1) % 2
            self.eo[self.ep[2]] = (self.eo[self.ep[2]] + 1) % 2
            self.eo[self.ep[9]] = (self.eo[self.ep[9]] + 1) % 2
            self.eo[self.ep[10]] = (self.eo[self.ep[10]] + 1) % 2
            ###
            self.bottom = np.rot90(self.bottom, axes=clockwise)
            self.front[[2]], self.right[[2]], \
                self.back[[2]], self.left[[2]] \
                = self.left[[2]], self.front[[2]], \
                self.right[[2]], self.back[[2]]

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

    def h_cost(self):  # input list
        # maybe property  # reaname it # or get h cost
        # def weight_stage_cepo(self, stage):  # input list
        # rashiftovke of corner pern edge orientations
        # count number of not zeros?
        # middle edges to middle layer - article page 14 begin

        # print(self.stage)
        # exit()
        # if self.stage == 'stage_0':
        #     kek = 0
        #     for i in range(8):
        #         if self.cp[i] == i:
        #             kek += 1
        #     return 16 - self.co.count(0) - kek
            # return 8 - self.сo.count(0)

        lr_slice_heuristic = 0
        if self.stage == 'stage_0':
            for i in [0, 3, 8, 11]:
                if self.ep[i] == i:
                    lr_slice_heuristic += 1
                if self.eo[i] == 0:
                    lr_slice_heuristic += 1
            # for i in [0, 3, 8, 11]:
            #     if self.eo[i] == 0:
            #         heur += 1

            # for i in [0, 3, 4, 7]:
            #     if self.cp[i] == i:
            #         heur += 1

            return 8 - lr_slice_heuristic

    def f_cost(self):
        """ len of history shows g(n). distance in steps from the initial node """
        return len(self.notation_history) + self.h_cost()
        # return self.h_cost()

    def is_goal_stage(self): # is goal stage state
        """make 12 not hardcoded"""
        # print(gre(self.cost('stage_0')))
        return self.h_cost() == 0

        # if self.stage == 'stage_0':
        # elif self.stage == 'stage_1': # maybe it will be unnecessary
        #     return

    def __lt__(self, other: State) -> bool: # add here whitch state is compre
        return self.f_cost() < other.f_cost()
        # st = 'stage_0'
        # return self.h_cost(st) + len(self.notation_history) < other.h_cost(st) + len(other.notation_history)

    def make_line_state(self):  # maybe
        make_one_line = lambda matrix: str(matrix.tolist())
        single_array = map(make_one_line, [
            self.top, self.left, self.front, self.right, self.back, self.bottom])
        # single_array = ''.join(re.findall(r'[a-z]', str(list(single_array))))
        return ''.join(re.findall(r'[a-z]', str(list(single_array))))

    def __str__(self):
        def sum_lines_np(*matrices):  # make line face in 1 line
            # for showing faces in color
            final_str = ''
            nums = len(matrices)
            for i in range(s_c):
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
        data = {'permutation': [str_dict['corner_permutation'], str_dict['edge_permutation']],
                'orientation': [str_dict['corner_orientation'], str_dict['edge_orientation']]}
        df = pd.DataFrame.from_dict(data, orient='index').rename(columns={0: 'corner', 1: 'edge'})
        return scheme + '\n\n' + self.make_line_state() + '\n\n' + df.to_string()
        # return scheme + '\n\n' + single_array + '\n\n' + df.to_string()

    @staticmethod
    def calculate_new_co(corner_orientation):
        return 2 if corner_orientation == -1 else corner_orientation % 3


# in solver make perebor hodov po osyam