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
# think about naming of steps in solve class

import tests
import os
import re
import numpy
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
        # print(len(self.state_node.notation_history))

        for stage in range(len(stages)):  # num stage
            self.solve_white_cross(stage)  # start solves group # white cross
            # print('SIZe OF QUE', self.open_list.qsize())
            self.open_list = PriorityQueue()  # need to delete open list
            # print('SIZe OF QUE', self.open_list.qsize())

        print(yll(self.state_node.notation_history))
        print(gre('after of first cross stage'), gre(len(self.state_node.notation_history)))

        self.solve_top_layer()
        print('after solving first top layer', len(self.state_node.notation_history))

        self.solve_middle_layer_edges()
        print('after solving middle layer', len(self.state_node.notation_history))

        self.solve_yellow_cross()
        print('history after bottom layer\n', self.state_node.notation_history)

        self.solve_bottom_corner_permutation()

    def solve_white_cross(self, stage):
        """ make explanation here
        stage input here unnecessary """
        threshold = self.state_node.f_cost()
        self.open_list = PriorityQueue()  # need i?
        solved = False  # solved state
        ii = 0
        while solved is False:
            # print(ii)
            self.open_list.put(self.state_node)
            thresholds = list()

            # print('threshold for children', threshold)
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
            # print()
            # log(f"thresholds {thresholds}")
            # log(f'end while | size que {self.open_list.qsize()}')
            threshold = min(thresholds)
            log(f"threshold after all : {threshold}")
            log('')
            ii += 1
        # print('NUM ITERS IS', ii)

    def solve_top_layer(self):
        # if target already solved -> break
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

            # check here correct_corner_permutation and correct_corner_orientation for true

            """ if corner zanyat drugim cornerom to ego nado smestit' and move"""
            if self.state_node.cp[0] != 0:
                # self.state_node.moves(['L\'', 'D', 'L', 'D'])
                self.state_node.moves(['L\'', 'D', 'L'])
            elif self.state_node.cp[7] != 7:
                # self.state_node.moves(['B\'', 'D', 'B', 'D'])
                self.state_node.moves(['B\'', 'D', 'B'])
            elif self.state_node.cp[3] != 3:
                # self.state_node.moves(['R\'', 'D', 'R', 'D'])
                self.state_node.moves(['R\'', 'D', 'R'])
            elif self.state_node.cp[4] != 4:
                # self.state_node.moves(['F\'', 'D', 'F', 'D'])
                self.state_node.moves(['F\'', 'D', 'F'])
            self.state_node.moves(['D'])

            # after all permutations can be added just [D]
            # else:
            #     print(ree('YEEEEEEEEEEEEEEEESS THIS IS WHAT I NEED'))
            #     self.state_node.moves(['D'])

            correct_corner_permutation = all(self.state_node.cp[cp] == cp for cp in up_layer_corners)
            correct_corner_orientation = all(self.state_node.co[cp] == 0 for cp in up_layer_corners)

    def solve_middle_layer_edges(self):
        # up_layer_corners
        # print(yll(self.state_node))

        mid_layer_edges = (4, 7, 6, 5)  # rename

        correct_edge_permutation = False # what if its true -> nothing need to go in while
        correct_edge_orientation = False # add in name mid edge

        # chech it here if it right - no need to enter to while

        i = 1
        while correct_edge_permutation is False or correct_edge_orientation is False:
            for edge in mid_layer_edges:
                if self.state_node.ep[edge] == edge:
                    if self.state_node.eo[edge] == 0:
                        continue
                    else:
                        if edge == 4:
                            self.state_node.moves(['B', 'D\'', 'B\'', 'L', 'B\'', 'L\'', 'B', 'D\''] * 2)
                        elif edge == 7:
                            self.state_node.moves(['R', 'D\'', 'R\'', 'B', 'R\'', 'B\'', 'R', 'D\''] * 2)
                        elif edge == 6:
                            self.state_node.moves(['F', 'D\'', 'F\'', 'R', 'F\'', 'R\'', 'F', 'D\''] * 2)
                        elif edge == 5:
                            self.state_node.moves(['L', 'D\'', 'L\'', 'F', 'L\'', 'F\'', 'L', 'D\''] * 2)
                else:
                    """ make doc """
                    if self.state_node.ep[1] == 4:
                        self.state_node.moves(['D', 'B', 'D\'', 'B\'', 'D\'', 'L\'', 'D', 'L'])
                    elif self.state_node.ep[10] == 4:
                        self.state_node.moves(['D\'', 'L\'', 'D', 'L', 'D', 'B', 'D\'', 'B\''])
                    elif self.state_node.ep[10] == 7:
                        self.state_node.moves(['D', 'R', 'D\'', 'R\'', 'D\'', 'B\'', 'D', 'B'])
                    elif self.state_node.ep[2] == 7:
                        self.state_node.moves(['D\'', 'B\'', 'D', 'B', 'D', 'R', 'D\'', 'R\''])
                    elif self.state_node.ep[2] == 6:
                        self.state_node.moves(['D', 'F', 'D\'', 'F\'', 'D\'', 'R\'', 'D', 'R'])
                    elif self.state_node.ep[9] == 6:
                        self.state_node.moves(['D\'', 'R\'', 'D', 'R', 'D', 'F', 'D\'', 'F\''])
                    elif self.state_node.ep[9] == 5:
                        self.state_node.moves(['D', 'L', 'D\'', 'L\'', 'D\'', 'F\'', 'D', 'F'])
                    elif self.state_node.ep[1] == 5:
                        self.state_node.moves(['D\'', 'F\'', 'D', 'F', 'D', 'L', 'D\'', 'L\''])

            # correct_edge_permutation = all(self.state_node.ep[ep] == ep for ep in mid_layer_edges)
            # correct_edge_orientation = all(self.state_node.eo[ep] == 0 for ep in mid_layer_edges)

            # if correct_edge_permutation is True and correct_edge_orientation is True:
            #     print(correct_edge_permutation, correct_edge_orientation)
            #     print(gre('good. it will not be redundant'))
            #     break

            # make here if solution is already done and in upper part
            # make property for this layer for cheking res
            if i % 3:  #4?
                """ the cost of movve tot find in upper liocations is cheaper than out of corner down"""
                self.state_node.moves(['D'])
                # print('make moove D')
            else:
                # print('use out of corner')
                if self.state_node.ep[4] != 4:
                    self.state_node.moves(['D\'', 'L\'', 'D', 'L', 'D', 'B', 'D\'', 'B\''])
                elif self.state_node.ep[7] != 7:
                    self.state_node.moves(['D\'', 'B\'', 'D', 'B', 'D', 'R', 'D\'', 'R\''])
                elif self.state_node.ep[6] != 6:
                    self.state_node.moves(['D\'', 'R\'', 'D', 'R', 'D', 'F', 'D\'', 'F\''])
                elif self.state_node.ep[5] != 5:
                    self.state_node.moves(['D\'', 'F\'', 'D', 'F', 'D', 'L', 'D\'', 'L\''])
                i = 0
            i += 1

            # can be funcs
            correct_edge_permutation = all(self.state_node.ep[ep] == ep for ep in mid_layer_edges)
            correct_edge_orientation = all(self.state_node.eo[ep] == 0 for ep in mid_layer_edges)

        # print(gre(self.state_node))
        # print('end len after mid layer', len(self.state_node.notation_history))

    def solve_yellow_cross(self):
        # exit()
        # 1 9 2 10 our target

        # print(self.state_node)

        """ at the beg we check the stse of yellow side
        usually bottom is yellow side """

        if self.state_node.bottom[0][1] != self.state_node.bottom[1][1] and \
                self.state_node.bottom[1][0] != self.state_node.bottom[1][1] and \
                self.state_node.bottom[1][2] != self.state_node.bottom[1][1] and \
                self.state_node.bottom[2][1] != self.state_node.bottom[1][1]:
            """if it 1 center only"""
            self.state_node.moves(['B', 'R', 'D', 'R\'', 'D\'', 'B\'',
                                   'D2', 'B', 'R', 'D', 'R\'', 'D\'', 'B\''])

        left_right_bar = set(self.state_node.bottom[1])
        back_front_bar = set(self.state_node.bottom[:, 1])

        if len(left_right_bar) != 1 or len(back_front_bar) != 1:
            """ if yellow cross dsnt exists """
            if len(left_right_bar) == 1 or len(back_front_bar) == 1:  # unnecess condition
                # print(yll(self.state_node.bottom))
                # print('bf       ', back_front_bar)
                # print('lr       ', left_right_bar)
                if len(back_front_bar) == 1:
                    # print(ree('left_right_bar match'))
                    """ make parallel yellow bar """
                    self.state_node.moves(['D'])
                    # print(gre(self.state_node.bottom))
                self.state_node.moves(['B', 'R', 'D', 'R\'', 'D\'', 'B\''])
                # print(gre(self.state_node.bottom))
            else:
                # print(gre(self.state_node.bottom))
                compare_little_l_shape = lambda: \
                    self.state_node.bottom[1][0] == \
                    self.state_node.bottom[1][1] == \
                    self.state_node.bottom[0][1]
                while compare_little_l_shape() is False:
                    # print(' while loop')
                    self.state_node.moves(['D'])
                self.state_node.moves(['B', 'D', 'R', 'D\'', 'R\'', 'B\''])
        else:  # this condition can be deleted with upper if
            # print(yll('yellow cross is ok'))
            pass  # cross already here

        # print(ree(self.state_node.bottom))
        # print(self.state_node)

    def solve_bottom_corner_permutation(self):
        # if target already solved -> break
        bottom_layer_corners = (1, 6, 2, 5)

        print(self.state_node)
        print('1 cp', self.state_node.cp[1])
        print('6 cp', self.state_node.cp[6])
        print('2 cp', self.state_node.cp[2])
        print('5 cp', self.state_node.cp[5])

        while [self.state_node.cp[cp] == cp for cp in bottom_layer_corners].count(True) != 2:
            print('move D')
            self.state_node.moves(['D'])
        # self.state_node.moves(['D'])
        # self.state_node.moves(['D'])
        print()
        print('1 cp', self.state_node.cp[1])
        print('6 cp', self.state_node.cp[6])
        print('2 cp', self.state_node.cp[2])
        print('5 cp', self.state_node.cp[5])

        correct_corner_permutation = [self.state_node.cp[cp] == cp for cp in bottom_layer_corners]
        print(correct_corner_permutation)
        # exit()
        # print(correct_corner_permutation[0])
        # print(correct_corner_permutation[2])
        if correct_corner_permutation[0] == correct_corner_permutation[2]:
        # if correct_corner_permutation[0] == correct_corner_permutation[2] or \
        #         correct_corner_permutation[1] == correct_corner_permutation[3]:
        # bec the 2 other will be the same if first conditition will be true
            print(yll('opposite corner location'))
            self.state_node.moves(['L', 'D\'', 'R\'', 'D', 'L\'', 'D\'', 'R', 'D2'])  # works
        else:
            # U R U' L' U R' U' L self.state_node.moves(['D', 'R', 'D\'', 'L\'', 'D', 'R\'', 'D\'', 'L'])
            # self.state_node.moves(['L', 'D\'', 'R\'', 'D', 'L\'', 'D\'', 'R', 'D2'])  # works
            print(gre('near trues'))
        # self.state_node.moves(['L', 'D\'', 'R\'', 'D', 'L\'', 'D\'', 'R', 'D2'])  # works

        # self.state_node.moves(['D'])
        # self.state_node.moves(['D'])
        # self.state_node.moves(['D'])


        c1 = self.state_node.cp[1] == 1
        c6 = self.state_node.cp[6] == 6
        c2 = self.state_node.cp[2] == 2
        c5 = self.state_node.cp[5] == 5

        print('1 cp', self.state_node.cp[1])
        print(ree('6 cp'), self.state_node.cp[6])
        print(ree('2 cp'), self.state_node.cp[2])
        print('5 cp', self.state_node.cp[5])

        print(c1, c6, c2, c5)
        exit()
        # if self.state_node.cp[2] == 2:  # 2 5
        #     self.state_node.moves(['D', 'R', 'D\'', 'L\'', 'D', 'R\'', 'D\'', 'L'])
        self.state_node.moves(['D'])
        # self.state_node.moves(['D'])


        # self.state_node.moves(['D', 'R', 'D\'', 'L\'', 'D', 'R\'', 'D\'', 'L'])
        # self.state_node.moves(['D'])
        # self.state_node.moves(['D'])

        print(gre(self.state_node))
        print('1 cp', self.state_node.cp[1])
        print('6 cp', self.state_node.cp[6])
        print('2 cp', self.state_node.cp[2])
        print('5 cp', self.state_node.cp[5])
        # print('yellow_faces', yellow_faces)

        # bottom_layer_edges = (1, 9, 2, 10)
        # correct_edge_permutation = all(self.state_node.ep[ep] == ep for ep in bottom_layer_edges)
        # correct_edge_orientation = all(self.state_node.eo[ep] == 0 for ep in bottom_layer_edges)

def make_random_state():
    random_list = []
    for i in range(0, 15):
        n = randint(0, 17)
        random_list.append(config_dict['3x3x3']['stage_0_moves'][n])
    # print(random_list)
    # need to remove first 15 turns
    return random_list


test = tests.clear_state
# test = tests.test6

kek = State(test['cepo'], test['faces'], None, None, None)
# randm = make_random_state()
randm =  ['L', 'R', 'D2', "B'", 'R2', 'F', 'L2', "U'", 'B', "R'", "D'", "L'", "L'", "B'", "F'", 'U', "R'", "D'", 'F2']
# randm with 1 yellow center = ["B'", 'U', 'D2', 'L2', "D'", "F'", 'F2', "F'", 'F2', 'L2', 'D2', 'R', 'U', "R'", "R'", 'R', 'F2', "L'", "D'", 'B', 'R2', "B'", "D'", 'B', 'D', "B'", "D'", 'B', 'D', "L'", 'D', 'L', 'D', "L'", 'D', 'L', 'D', "L'", 'D', 'L', 'D', "R'", 'D2', 'R', 'D', "R'", "D'", 'R', "L'", 'D', 'L', 'D', "F'", 'D2', 'F', 'D', "F'", "D'", 'F', "L'", 'D', 'L', 'D', 'B', 'D', "B'", "D'", 'B', 'D', "B'", "D'", 'D', 'D', 'D', "D'", "L'", 'D', 'L', 'D', 'B', "D'", "B'", 'D', 'R', "D'", "R'", "D'", "B'", 'D', 'B', "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", "D'", "F'", 'D', 'F', 'D', 'L', "D'", "L'", 'D', 'D', "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", 'D']
# print(randm)
kek.moves(randm)
# kek.moves(["D'", 'U', 'B', 'D2', 'D2', "D'", "L'", "R'", "L'", 'L2', "D'", 'L', "B'", "U'", 'F2', 'L', 'F', "D'", "L'", 'F', 'B2'])
# print(kek)
# exit()

solv = Solver(kek)
# print(kek)

# if d2 and d2 - del all in history


