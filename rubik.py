from __future__ import annotations
from queue import PriorityQueue
# state0 сделать как шафл
# can @property be with __

import copy
from termcolor import colored
from itertools import repeat
from typing import Final
import operator
import pandas as pd

gre = lambda i: colored(i, 'green')
yll = lambda i: colored(i, 'yellow')


class State:  # rename like rubik state or cube state
    goal_edge_permutation = [0] * 12  # better list i belive
    goal_corner_permutation = '0' * 8
    goal_edge_orientation = '0' * 12
    goal_corner_orientation = '0' * 8
    id = 0
    # delete None as default value

    def __init__(self, properties, stage, notation, notation_history):  # here add glubina poiska # nado li dobavit' None avtomatom?? # rename moves history
        self.properties = copy.deepcopy(properties)
        self.cp = self.properties['corner_permutation']
        self.ep = self.properties['edge_permutation']
        self.co = self.properties['corner_orientation']
        self.eo = self.properties['edge_orientation']

        self.notation = notation  # if not none
        self.notation_history = notation_history # if not none
        self.id = None  # del # make it in right order
        self.stage = 'stage_0' if stage is None else stage

        # self.notation_history = self.notation_history  # list or none
        self.notation_history = list() if notation_history is None else notation_history

        if self.notation:
            self.moves(self.notation)
            self.notation_history.append(self.notation)
            # if self.notation_history:
                # self.notation_history.append(self.notation)

        # print(id(self.total_state))
        # print(id(total_state))
        # moves need to init
        # if moves.split() > 1 -> couple moves -> apply it to them
        # pass here dictionary i belive is better
        # self.corner_permutations =
        search_depth = 0

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

        def r_clockwise():
            self.cp[3], self.cp[7], self.cp[2], self.cp[6] = \
                self.cp[6], self.cp[3], self.cp[7], self.cp[2]

            self.ep[6], self.ep[3], self.ep[7], self.ep[2] = \
                self.ep[2], self.ep[6], self.ep[3], self.ep[7]

        def f_clockwise():
            self.cp[4], self.cp[3], self.cp[6], self.cp[1] = \
                self.cp[1], self.cp[4], self.cp[3], self.cp[6]

            self.ep[5], self.ep[8], self.ep[6], self.ep[9] = \
                self.ep[9], self.ep[5], self.ep[8], self.ep[6]

            self.co[self.cp[1]] = State.calculate_new_co(self.co[self.cp[1]] + 1)
            self.co[self.cp[3]] = State.calculate_new_co(self.co[self.cp[3]] + 1)
            self.co[self.cp[4]] = State.calculate_new_co(self.co[self.cp[4]] - 1)
            self.co[self.cp[6]] = State.calculate_new_co(self.co[self.cp[6]] - 1)

        def b_clockwise():
            self.cp[7], self.cp[0], self.cp[5], self.cp[2] = \
                self.cp[2], self.cp[7], self.cp[0], self.cp[5]

            self.ep[7], self.ep[11], self.ep[4], self.ep[10] = \
                self.ep[10], self.ep[7], self.ep[11], self.ep[4]

            self.co[self.cp[0]] = State.calculate_new_co(self.co[self.cp[0]] + 1)
            self.co[self.cp[2]] = State.calculate_new_co(self.co[self.cp[2]] + 1)
            self.co[self.cp[5]] = State.calculate_new_co(self.co[self.cp[5]] - 1)
            self.co[self.cp[7]] = State.calculate_new_co(self.co[self.cp[7]] - 1)

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
            case _: raise Exception  # make another except # delete it

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

        heur = 0
        if self.stage == 'stage_0':
            for i in [0, 3, 8, 11]:
                if self.ep[i] == i:
                    heur += 1
                if self.eo[i] == 0:
                    heur += 1
            # for i in [0, 3, 8, 11]:
            #     if self.eo[i] == 0:
            #         heur += 1

            # for i in [0, 3, 4, 7]:
            #     if self.cp[i] == i:
            #         heur += 1

            return 8 - heur


        if self.stage == 'stage_01':
            return 12 - self.eo.count(0)  # example 12 - 9 zeros = 3
        elif self.stage == 'stage_12':
            # lr slise means layer btw L and R sides. e8 9 10 11 edges by indexing
            # плюс последние 8 9 10 11 для боковух
            lr_slice_heuristic = 0
            # print('!!!edge_perm', self.ep[-4:]) # lr_edges
            for edge_permutation in self.ep[-4:]:
                if edge_permutation in [8, 9, 10, 11]:
                    lr_slice_heuristic += 2
            return 16 - self.co.count(0) - lr_slice_heuristic
            # if sorted(self.ep[-4:]) == [8, 9, 10, 11]:
            #     return 0  # edges and corners orientations
            # return 1
        elif self.stage == 'stage_11':
            # print('stage 2 is here')
            lr_slice_heuristic = 0
            # print('!!!edge_perm', self.ep[-4:]) # lr_edges
            for edge_permutation in self.ep[-4:]:
                if edge_permutation in [8, 9, 10, 11]:
                    lr_slice_heuristic += 1
            # if sorted(self.ep[-4:]) == [8, 9, 10, 11]:
            #     lr_slice_heuristic = 1
                  # edges and corners orientations
            # lr_slice_heuristic = lr_slice_heuristic // 4
            # print(lr_slice_heuristic)
            # return 9 - self.co.count(0) - lr_slice_heuristic
            # return 1 - lr_slice_heuristic  # edges and corners orientations
            return 12 - self.co.count(0) - lr_slice_heuristic
            # return 9 - self.co.count(0) - lr_slice_heuristic
            # return 8 - self.co.count(0)

        """
        print('lr_slice_heuristic', lr_slice_heuristic)
        print('self.ep[-4:]:', self.ep[-4:])
        print("HH", 12 - self.co.count(0) - lr_slice_heuristic)
        print(self.notation)
        print(self)
        print(self.properties)
        print(self.notation_history)
        print()
        """
            # print('lr_slice_heuristic', lr_slice_heuristic)
            # print('HEUR', 24 - self.eo.count(0) - self.co.count(0) - lr_slice_heuristic)
            # print(self)
            # return 24 - self.eo.count(0) - self.co.count(0) - lr_slice_heuristic  # edges and corners orientations
            # return 12 - self.co.count(0) - lr_slice_heuristic  # edges and corners orientations
            # return 8 - self.co.count(0)  # edges and corners orientations
            # return 20 - self.eo.count(0) - self.co.count(0)

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

    def __str__(self):
        # print(gre(f"corner_permutation: {self.properties['corner_permutation']}"))
        # print(gre(f"corner_orientation: {self.properties['corner_orientation']}"))
        # print(yll(f"edge_permutation: {self.properties['edge_permutation']}"))
        # print(yll(f"edge_orientation: {self.properties['edge_orientation']}"))
        str_dict = {k: ' '.join(map(str, v)) for k, v in self.properties.items()}
        data = {'permutation': [str_dict['corner_permutation'], str_dict['edge_permutation']],
                'orientation': [str_dict['corner_orientation'], str_dict['edge_orientation']]}
        df = pd.DataFrame.from_dict(data, orient='index').rename(columns={0: 'corner', 1: 'edge'})
        return df.to_string()

    @staticmethod
    def calculate_new_co(corner_orientation):
        return 2 if corner_orientation == -1 else corner_orientation % 3


# in solver make perebor hodov po osyam