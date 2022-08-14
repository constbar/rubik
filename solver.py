# maybe make list of notations for applying all moves
# if shuffled state starts - dont write the turns to somewhere
# make in moves \' in back
# tuple use less memory than list # use tuple everywhere
# solver:
import numpy as np
# if last turn was in the same coordinate axis ?
# if last was repeated with this turn -> continue
# print(st)
# add timer
# make in rubik moves in good order like subgroup state
# try solved orientaion to solve

import tests
import os
import re
import time
import copy
import logging
import timeit
from rubik_state import State
from termcolor import colored
from queue import PriorityQueue
from typing import Optional, Dict, Any
import queue
from random import randint

logging.basicConfig(level=logging.INFO, filename='log.log',
                    filemode='w', format='%(message)s')
log = lambda i: logging.info(i)

gre = lambda i: colored(i, 'green')
yll = lambda i: colored(i, 'yellow')
ree = lambda i: colored(i, 'red')

stages = ['stage_0'] #, 'stage_1']#, 'stage_2']  # rename to stage 0

config_dict = {
    '3x3x3': {
        # goal state ??
        # 'subgroup_0_moves': ['U', 'D', 'L', 'R', 'F', 'B'],
        # 'subgroup_0_moves': ['L', 'R', 'F', 'B', 'U', 'D'],
        # 'stage_0_moves': ['L', 'R', 'F', 'B', 'U', 'D'],
        'stage_0_moves': ["L", "L'", "L2", "R", "R'", "R2", "F", "F'", "F2", "B", "B'", "B2", "U", "U'", "U2", "D", "D'", "D2"],
        'stage_1_moves': ['L', 'R', 'F', 'B', 'U2', 'D2'],
        'stage_2_moves': ['L', 'R', 'F', 'B', 'U2', 'D2'],
    }
}


class Solver:
    def __init__(self, shuffled_node):  # it is the biging state
        self.state_node = shuffled_node  # this node will be over init for each stage # re like rubik state
        self.open_list = PriorityQueue()  # add it in first step
        self.solution_path = list()

        for stage in range(len(stages)):  # num stage
            self.solve_white_cross(stage)  # start solves group # white cross
            # print('SIZe OF QUE', self.open_list.qsize())
            self.open_list = PriorityQueue() # need to delete open list
            # print('SIZe OF QUE', self.open_list.qsize())
        print('end of cross stage')
        print('fin white cross stage\n\n')
        print(self.solution_path)
        # print(self.state_node)

        self.solve_top_layer()

        # print(gre('\n\nafter white corners'))
        # print(self.state_node)

        self.solve_middle_layer_edges()

    def solve_white_cross(self, stage):
        """ make explanation here
        stage input here unnecessary """
        threshold = self.state_node.f_cost()
        self.open_list = PriorityQueue()  # need i?
        solved = False  # solved state
        ii = 0
        while solved is False:
            print(ii)
            self.open_list.put(self.state_node)
            thresholds = list()

            print('threshold for children', threshold)
            while self.open_list.qsize():
                lowest_node = self.open_list.get()

                if lowest_node.is_goal_stage():
                    """
                    print(gre('BiNGO! the answer is here'))
                    print(lowest_node.ep)
                    print(lowest_node.eo)

                    print(gre(lowest_node))
                    print(gre(lowest_node.notation))
                    print(gre(lowest_node.notation_history))
                    print()
                    """
                    # for k, v in lowest_node.properties.items():
                    #     print(k, v)
                    self.solution_path += lowest_node.notation_history
                    solved = True
                    self.state_node = lowest_node
                    """
                    self.start_node = State( no need yet for next level
                        # copy.deepcopy(lowest_node.properties), f'stage_{stage + 1}', None, None
                        lowest_node.properties, f'stage_{stage + 1}', None, None
                    )
                    """
                    break

                # for notation in g0:
                for notation in config_dict['3x3x3'][f'stage_{stage}_moves']:
                    # print(stage)
                    # print(config_dict['3x3x3'][f'{stage}_moves'])
                    new_state = State(lowest_node.properties, lowest_node.make_line_state(),
                                      stages[stage], notation,  # rename move history
                                      copy.deepcopy(lowest_node.notation_history))
                    # print(f'node cost {new_state.f_cost()}, '
                    #       f'{new_state.notation}, {new_state.notation_history}')
                    if new_state.f_cost() <= threshold:
                        self.open_list.put(new_state)
                    else:
                        thresholds.append(new_state.f_cost())
            if solved is True:
                break
            print()
            # log(f"thresholds {thresholds}")
            # log(f'end while | size que {self.open_list.qsize()}')
            threshold = min(thresholds)
            log(f"threshold after all : {threshold}")
            log('')
            ii += 1
        print('NUM ITERS IS', ii)

    def solve_top_layer(self):
        solved_state = False  # re
        up_layer_corners = (0, 7, 3, 4)  # rename

        # print(gre(self.state_node))

        correct_corner_permutation = False
        correct_corner_orientation = False
        while correct_corner_permutation is False or correct_corner_orientation is False:
            for corner in up_layer_corners:  # re # i = check corner pernumtstion  # re corner num
                """each corner has a state 0 or 1 or 2. in else performs 1 or 2 orientations"""
                if self.state_node.cp[corner] == corner:
                    if self.state_node.co[corner] == 0:
                        continue
                    else:
                        if corner == 0:
                            if self.state_node.co[corner] == 1:
                                self.state_node.moves(['B', 'D', 'B\'', 'D\''] * 2)
                            elif self.state_node.co[corner] == 2:
                                self.state_node.moves(['L\'', 'D\'', 'L', 'D'] * 2)
                        elif corner == 7:
                            if self.state_node.co[corner] == 1:
                                self.state_node.moves(['R', 'D', 'R\'', 'D\''] * 2)
                            elif self.state_node.co[corner] == 2:
                                self.state_node.moves(['B\'', 'D\'', 'B', 'D'] * 2)
                        elif corner == 3:
                            if self.state_node.co[corner] == 1:
                                self.state_node.moves(['F', 'D', 'F\'', 'D\''] * 2)
                            elif self.state_node.co[corner] == 2:
                                self.state_node.moves(['R\'', 'D\'', 'R', 'D'] * 2)
                        elif corner == 4:
                            if self.state_node.co[corner] == 1:
                                self.state_node.moves(['L', 'D', 'L\'', 'D\''] * 2)
                            elif self.state_node.co[corner] == 2:
                                self.state_node.moves(['F\'', 'D\'', 'F', 'D'] * 2)
                else:  # if bottom layer #  print(gre(self.state_node))
                    """ make here example if on position 6 corner 
                    stay corner number 3 with following pos -> rotate
                    thhis is jsut variation to take need corner from bottom
                    to top layer with definite orirntation """
                    if self.state_node.cp[5] == 0:
                        if self.state_node.co[0] == 0:
                            self.state_node.moves(['B', 'D', 'B\''])
                        elif self.state_node.co[0] == 1:
                            self.state_node.moves(['L\'', 'D2', 'L', 'D', 'L\'', 'D\'', 'L'])
                        elif self.state_node.co[0] == 2:
                            self.state_node.moves(['L\'', 'D\'', 'L'])
                    elif self.state_node.cp[2] == 7:
                        if self.state_node.co[7] == 0:
                            self.state_node.moves(['B\'', 'D\'', 'B'])
                        elif self.state_node.co[7] == 1:
                            self.state_node.moves(['R', 'D', 'R\''])
                        elif self.state_node.co[7] == 2:
                            self.state_node.moves(['B\'', 'D2', 'B', 'D', 'B\'', 'D\'', 'B'])
                    elif self.state_node.cp[6] == 3:
                        if self.state_node.co[3] == 0:
                            self.state_node.moves(['F', 'D', 'F\''])
                        elif self.state_node.co[3] == 1:
                            self.state_node.moves(['R\'', 'D2', 'R', 'D', 'R\'', 'D\'', 'R'])
                        elif self.state_node.co[3] == 2:
                            self.state_node.moves(['R\'', 'D\'', 'R'])
                    elif self.state_node.cp[1] == 4:
                        if self.state_node.co[4] == 0:
                            self.state_node.moves(['F\'', 'D\'', 'F'])
                        elif self.state_node.co[4] == 1:
                            self.state_node.moves(['L', 'D', 'L\''])
                        elif self.state_node.co[4] == 2:
                            self.state_node.moves(['F\'', 'D2', 'F', 'D', 'F\'', 'D\'', 'F'])
            """ if corner zanyat drugim cornerom to ego nado smestit' and move"""
            if self.state_node.cp[0] != 0:
                self.state_node.moves(['L\'', 'D', 'L', 'D'])
            elif self.state_node.cp[7] != 7:
                self.state_node.moves(['B\'', 'D', 'B', 'D'])
            elif self.state_node.cp[3] != 3:
                self.state_node.moves(['R\'', 'D', 'R', 'D'])
            elif self.state_node.cp[4] != 4:
                self.state_node.moves(['F\'', 'D', 'F', 'D'])
            # else:
            #     self.state_node.moves(['D'])

            correct_corner_permutation = all(self.state_node.cp[cp] == cp for cp in up_layer_corners)
            correct_corner_orientation = all(self.state_node.co[cp] == 0 for cp in up_layer_corners)

    def solve_middle_layer_edges(self):
        # up_layer_corners
        print(yll(self.state_node))

        mid_layer_edges = (4, 5, 6, 7)  # rename

        correct_edge_permutation = False
        correct_edge_orientation = False

        for edge in mid_layer_edges:
            # print(edge)
            if self.state_node.ep[edge] == edge:
                print('bingo')
                if self.state_node.eo[edge] == 0:
                    continue
                else:
                    if edge == 4:
                        pass
                        # self.state_node.moves(['B', 'D\'', 'B\'', 'L', 'B\'', 'L\'', 'B', 'D\''] * 2)
                    elif edge == 5:  # L D' L' F L' F' L D'            # can i multiple tuple?
                        # self.state_node.moves(['L', 'D\'', 'L\'', 'F', 'L\'', 'F\'', 'L', 'D\''] * 2)
                        pass
                    elif edge == 6:
                        pass
                        self.state_node.moves(['F', 'D\'', 'F\'', 'R', 'F\'', 'R\'', 'F', 'D\''] * 2)
                    elif edge == 7:
                        pass # R D' R' B R' B' R D'
                        # self.state_node.moves(['R', 'D\'', 'R\'', 'B', 'R\'', 'B\'', 'R', 'D\''] * 2)
                        # self.state_node.moves([])


        print(gre(self.state_node))


def make_random_state():
    random_list = []
    for i in range(0, 15):
        n = randint(0, 17)
        random_list.append(config_dict['3x3x3']['stage_0_moves'][n])
    # print(random_list)
    return random_list


test = tests.clear_state
# test = tests.test6

kek = State(test['cepo'], test['faces'], None, None, None)
# randm = make_random_state()
randm = ["D'", "L'", 'U', 'L2', 'B', 'B2', 'F2', "D'", 'D', 'U2', 'F2', 'B', 'F', 'B', 'B']
print(randm)
kek.moves(randm)
kek.moves(['R', 'F2', 'U', 'F', 'D', 'R', "L'", 'F2'])
# print(kek)
# exit()

# kek.moves([])
# kek.moves(["R'", 'D', 'R', "F'", 'D2'])
# kek.moves(['R\'', 'D\'', 'R', 'D', 'R\'', 'D\'', 'R', 'D'])
# kek.moves(['R\'', 'D\'', 'R', 'D', 'R\'', 'D\'', 'R', 'D'])
# print(kek)
# exit()
# mv = "R U R' U' R U R' U'"
# for m in mv.split():
#     kek.moves(m)
# print(kek)


solv = Solver(kek)
# print(kek)


