import copy
from termcolor import colored
from itertools import repeat
from typing import Final
import operator

gre = lambda i: colored(i, 'green')

class Solver:
    def __init__(self, init_state):
        self.init__state = init_state

test = { # maybe name it in full
    'corner_permutation': list(range(8)),
    'edge_permutation': list(range(12)),
    'corner_orientation': [0] * 8,
    'edge_orientation': [0] * 12
}

RUru = { # maybe name it in full
    'corner_permutation': [7, 1, 2, 6, 4, 5, 3, 0],
    'edge_permutation': [0, 1, 2, 6, 4, 5, 11, 7, 8, 9, 10, 3],
    'corner_orientation': [2, 0, 0, 2, 0, 0, 0, 2],
    'edge_orientation': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
}


class State:  # rename like rubik state
    goal_edge_permutation = [0] * 12  # better list i belive
    goal_corner_permutation = '0' * 8
    goal_edge_orientation = '0' * 12
    goal_corner_orientation = '0' * 8

    def __init__(self, properties, moves=None):  # here add glubina poiska
        self.properties = copy.deepcopy(properties)

        self.cp = self.properties['corner_permutation']
        self.ep = self.properties['edge_permutation']
        self.co = self.properties['corner_orientation']
        self.eo = self.properties['edge_orientation']

        # print(id(self.total_state))
        # print(id(total_state))
        # moves need to init
        # if moves.split() > 1 -> couple moves -> apply it to them
        # pass here dictionary i belive is better
        # self.corner_permutations =
        search_depth = 0

    @staticmethod
    def calculate_new_co(orientation):
        return 2 if orientation == -1 else orientation % 3

    def moves(self, move):
        """ U notation """
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

            # print(id(self.co))
            # print(id(self.total_state['corner_orientation']))

        def u_double_clockwise():
            [u_clockwise() for _ in range(2)]

        def u_counterclockwise():
            [u_clockwise() for _ in range(3)]

        """ D notation """
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

        def d_double_clockwise():
            [d_clockwise() for _ in range(2)]

        def d_counterclockwise():
            [d_clockwise() for _ in range(3)]

        """ L notation """
        def l_clockwise():
            self.cp[0], self.cp[4], self.cp[1], self.cp[5] = \
                self.cp[5], self.cp[0], self.cp[4], self.cp[1]

            self.ep[4], self.ep[0], self.ep[5], self.ep[1] = \
                self.ep[1], self.ep[4], self.ep[0], self.ep[5]

        def l_double_clockwise():
            [l_clockwise() for _ in range(2)]

        def l_counterclockwise():
            [l_clockwise() for _ in range(3)]

        """ R notation """
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
            case 'U2': u_double_clockwise()
            case 'U\'': u_counterclockwise()

            case 'D': d_clockwise()
            case 'D2': d_double_clockwise()
            case 'D\'': d_counterclockwise()

            case 'L': l_clockwise()
            case 'L2': l_double_clockwise()
            case 'L\'': l_counterclockwise()

            case 'R': r_clockwise()
            case 'R2': [r_clockwise() for _ in range(2)]
            case 'R\'': [r_clockwise() for _ in range(3)]

            case 'F': f_clockwise()
            case 'F2': [f_clockwise() for _ in range(2)]
            case 'F\'': [f_clockwise() for _ in range(3)]

            case 'B': b_clockwise()
            case 'B2': [b_clockwise() for _ in range(2)]
            case 'B\'': [b_clockwise() for _ in range(3)]


    def __str__(self):
        pass


go = State(test)
# for k, v in test.items():
#     print(k[:8], v)
print()
print()

# go.d_double_clockwise()
go.moves('B2')
# go.moves('R\'')
# go.moves('R\'')
# go.moves('R\'')
# go.moves('R2')
# go.moves('R')
# go.moves('R')
# go.moves('R')
# go.r_clockwise()
# go.u_clockwise()
# go.r_counterclockwise()
# go.u_counterclockwise()


# go.u_clockwise()
for k, v in go.properties.items():
    print(k[:8], v)
