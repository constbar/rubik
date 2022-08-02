from __future__ import annotations
from queue import PriorityQueue
# state0 сделать как шафл

import copy
from termcolor import colored
from itertools import repeat
from typing import Final
import operator

gre = lambda i: colored(i, 'green')
yll = lambda i: colored(i, 'yellow')


class Solver:
    def __init__(self, init_state):
        self.init__state = init_state


class State:  # rename like rubik state
    goal_edge_permutation = [0] * 12  # better list i belive
    goal_corner_permutation = '0' * 8
    goal_edge_orientation = '0' * 12
    goal_corner_orientation = '0' * 8
    id = 0
    # delete None as default value

    def __init__(self, properties, notation, notation_history):  # here add glubina poiska
        self.properties = copy.deepcopy(properties)
        self.cp = self.properties['corner_permutation']
        self.ep = self.properties['edge_permutation']
        self.co = self.properties['corner_orientation']
        self.eo = self.properties['edge_orientation']

        self.notation = notation
        self.notation_history = notation_history
        self.id = None

        # self.notation_history = self.notation_history  # list or none
        if notation_history is not None:
            self.notation_history = notation_history
        else:
            self.notation_history = list()

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
        """ the notation with the number 2 makes a double clockwise rotation.
        apostrophe notation makes a counter-clockwise rotation. """
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

        match move:
            case 'U': u_clockwise()
            case 'U2': [u_clockwise() for _ in range(2)]
            case 'U\'': [u_clockwise() for _ in range(3)]
            case 'D': d_clockwise()
            case 'D2': [d_clockwise() for _ in range(2)]
            case 'D\'': [d_clockwise() for _ in range(3)]
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
            case _: raise Exception  # make another except

    def h_cost(self, stage='stage_0'):  # input list
        # maybe property  # reaname it # or get h cost
        # def weight_stage_cepo(self, stage):  # input list
        # rashiftovke of corner pern edge orientations
        # count number of not zeros?
        if stage == 'stage_0':
            return 12 - self.eo.count(0)  # example 12 - 9 zeros = 3
        elif stage == 'stage_1':
            # плюс последние 8 9 9 10 11 для боковух
            return 20 - self.eo.count(0) - self.co.count(0) # edges and corners orientations


    def f_cost(self):
        """ len of history shows g(n). distance in steps from the initial node """
        return len(self.notation_history) + self.h_cost()
        pass

    def is_goal_stage(self, stage):
        """make 12 not hardcoded"""
        # print(gre(self.cost('stage_0')))

        if stage == 'stage_0':
            return self.h_cost('stage_0') == 0
        elif stage == 'stage_1':
            return

    def __lt__(self, other: State) -> bool: # add here whitch state is compre
        return self.f_cost() < other.f_cost()
        # st = 'stage_0'
        # return self.h_cost(st) + len(self.notation_history) < other.h_cost(st) + len(other.notation_history)

    def __str__(self):
        # can make it more beauty with numpy
        print(gre(f"corner_permutation: {self.properties['corner_permutation']}"))
        print(gre(f"corner_orientation: {self.properties['corner_orientation']}"))
        print(yll(f"edge_permutation: {self.properties['edge_permutation']}"))
        print(yll(f"edge_orientation: {self.properties['edge_orientation']}"))
        return ''

    @staticmethod
    def calculate_new_co(corner_orientation):
        return 2 if corner_orientation == -1 else corner_orientation % 3


# in solver make perebor hodov po osyam