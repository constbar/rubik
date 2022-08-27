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
# check the num of turns after every step
# status_corner_orintation or correct_edge_permutation >?? choosse naming

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
blu = lambda i: colored(i, 'blue')

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

        self.solve_bottom_corner_orientation()

        self.solve_edge_permutation()

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
                            """ is this upside down of edge? ????"""
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
                        self.state_node.moves(['D', 'B', 'D\'', 'B\'', 'D\'', 'L\'', 'D', 'L'])  # i belive this 1 orient need thinl about 0
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
                compare_one_color_small_l_shape = lambda: \
                    self.state_node.bottom[1][0] == \
                    self.state_node.bottom[1][1] == \
                    self.state_node.bottom[0][1]
                while compare_one_color_small_l_shape() is False:
                    # print(' while loop')
                    self.state_node.moves(['D'])
                self.state_node.moves(['B', 'D', 'R', 'D\'', 'R\'', 'B\''])
        else:  # this condition can be deleted with upper if
            # print(yll('yellow cross is ok'))
            pass  # cross already here

        # print(ree(self.state_node.bottom))
        # print(self.state_node)

    def solve_bottom_corner_permutation(self):
        """ here we work with permutation """
        # if target already solved -> break
        bottom_layer_corners = (1, 6, 2, 5)
        """
        print(self.state_node)
        print('1 cp', self.state_node.cp[1])
        print('6 cp', self.state_node.cp[6])
        print('2 cp', self.state_node.cp[2])
        print('5 cp', self.state_node.cp[5])
        """

        get_status_corner_permutation = lambda: [self.state_node.cp[cp] == cp
                                                 for cp in bottom_layer_corners]
        # print(ree(get_status_corner_permutation()))

        while all(get_status_corner_permutation()) is False:
            # print(all(get_status_corner_permutation()))

            while get_status_corner_permutation().count(True) < 2:
                self.state_node.moves(['D'])

            if all(get_status_corner_permutation()) is True:
                break

            # print(gre(get_status_corner_permutation()))

            # 1, 6, 2, 5
            if get_status_corner_permutation()[0] is get_status_corner_permutation()[1] is True:
                # print('1 6 at work') # +
                self.state_node.moves(['F', 'D\'', 'B\'', 'D', 'F\'', 'D\'', 'B', 'D2'])
                # break
            elif get_status_corner_permutation()[1] is get_status_corner_permutation()[2] is True:
                # print(yll('was in  2 and 6 condition'))
                # self.state_node.moves(['L', 'D\'', 'R\'', 'D', 'L\'', 'D\'', 'R', 'D2'])
                self.state_node.moves(['R', 'D\'', 'L\'', 'D', 'R\'', 'D\'', 'L', 'D2'])  # not
                break
                # self.state_node.moves(['L', 'D\'', 'R\'', 'D', 'L\'', 'D\'', 'R', 'D2'])
            elif get_status_corner_permutation()[2] is get_status_corner_permutation()[3] is True:
                # print(yll('was in  2 and 5 condition')) # +
                self.state_node.moves(['B', 'D\'', 'F\'', 'D', 'B\'', 'D\'', 'F', 'D2'])
            elif get_status_corner_permutation()[3] is get_status_corner_permutation()[0] is True:
                # print(yll('was in 5 and 1 condition'))
                self.state_node.moves(['L', 'D\'', 'R\'', 'D', 'L\'', 'D\'', 'R', 'D2']) # not from here but works
                # self.state_node.moves(['R', 'D\'', 'L\'', 'D', 'R\'', 'D\'', 'L', 'D2'])

            if all(get_status_corner_permutation()) is True:
                break

            """ this is for oposite location of conners not on their positions"""
            if get_status_corner_permutation()[0] is True:
                # print(blu('0 is true'))  # +
                self.state_node.moves(['F', 'D\'', 'B\'', 'D', 'F\'', 'D\'', 'B', 'D2'])
            elif get_status_corner_permutation()[1] is True:
                # print(blu('1 is true'))  # +
                self.state_node.moves(['R', 'D\'', 'L\'', 'D', 'R\'', 'D\'', 'L', 'D2'])
            #
            # elif get_status_corner_permutation()[2] is True:
            #     print(blu('2 is true'))
            #     self.state_node.moves(['B', 'D\'', 'F\'', 'D', 'B\'', 'D\'', 'F', 'D2'])
            # elif get_status_corner_permutation()[3] is True:
            #     print(blu('3 is true'))
            #     self.state_node.moves(['L', 'D\'', 'R\'', 'D', 'L\'', 'D\'', 'R', 'D2'])

            # print(blu(get_status_corner_permutation()))

        # print(gre(get_status_corner_permutation()))
        # print('1 cp', self.state_node.cp[1])
        # print('6 cp', self.state_node.cp[6])
        # print('2 cp', self.state_node.cp[2])
        # print('5 cp', self.state_node.cp[5])

        # print(self.state_node)

    def solve_bottom_corner_orientation(self):
        bottom_layer_corners = (1, 6, 2, 5)


        status_corner_orintation = [self.state_node.co[co] for co in bottom_layer_corners]
        # print(gre(status_corner_orintation))

        if status_corner_orintation == [0, 0, 0, 0]:  # num 1 condition
            print('great!')
            return
        # use a11 # try here switch case # if case == 0000 -> break
        #     self.state_node.moves(['R', 'D', 'R\'', 'D', 'R', 'D2', 'R\'', 'D2'])
        elif status_corner_orintation == [0, 1, 1, 1]:  # number 2 condition
            print('ok')
            self.state_node.moves(['B', 'D', 'B\'', 'D', 'B', 'D2', 'B\'', 'D2'])
        elif status_corner_orintation == [1, 0, 1, 1]:
            print('ok')
            self.state_node.moves(['L', 'D', 'L\'', 'D', 'L', 'D2', 'L\'', 'D2'])
        elif status_corner_orintation == [1, 1, 0, 1]:
            print('ok')
            self.state_node.moves(['F', 'D', 'F\'', 'D', 'F', 'D2', 'F\'', 'D2'])
        elif status_corner_orintation == [1, 1, 1, 0]:
            print('ok')
            self.state_node.moves(['R', 'D', 'R\'', 'D', 'R', 'D2', 'R\'', 'D2'])

        elif status_corner_orintation == [0, 2, 2, 2]:  # number 3 condition
            print('ok')
            self.state_node.moves(['R\'', 'D\'', 'R', 'D\'', 'R\'', 'D2', 'R', 'D2'])
        elif status_corner_orintation == [2, 0, 2, 2]:
            print('ok')
            self.state_node.moves(['B\'', 'D\'', 'B', 'D\'', 'B\'', 'D2', 'B', 'D2'])
        elif status_corner_orintation == [2, 2, 0, 2]:
            print('ok')
            self.state_node.moves(['L\'', 'D\'', 'L', 'D\'', 'L\'', 'D2', 'L', 'D2'])
        elif status_corner_orintation == [2, 2, 2, 0]:
            print('ok')
            self.state_node.moves(['F\'', 'D\'', 'F', 'D\'', 'F\'', 'D2', 'F', 'D2'])

        elif status_corner_orintation == [1, 2, 0, 0]:  # number 4 condition
            print('ok')
            self.state_node.moves(['D2'])
            self.state_node.moves(['R', 'D', 'R\'', 'D', 'R', 'D2', 'R\'', 'D2'])
            self.state_node.moves(['D2'])
            self.state_node.moves(['R\'', 'D\'', 'R', 'D\'', 'R\'', 'D2', 'R', 'D2'])
        elif status_corner_orintation == [0, 1, 2, 0]:
            print('ok')
            self.state_node.moves(['D2'])
            self.state_node.moves(['B', 'D', 'B\'', 'D', 'B', 'D2', 'B\'', 'D2'])
            self.state_node.moves(['D2'])
            self.state_node.moves(['B\'', 'D\'', 'B', 'D\'', 'B\'', 'D2', 'B', 'D2'])
        elif status_corner_orintation == [0, 0, 1, 2]:
            print('ok')
            self.state_node.moves(['D2'])
            self.state_node.moves(['L', 'D', 'L\'', 'D', 'L', 'D2', 'L\'', 'D2'])
            self.state_node.moves(['D2'])
            self.state_node.moves(['L\'', 'D\'', 'L', 'D\'', 'L\'', 'D2', 'L', 'D2'])
        elif status_corner_orintation == [2, 0, 0, 1]:
            print('ok')
            self.state_node.moves(['D2'])
            self.state_node.moves(['F', 'D', 'F\'', 'D', 'F', 'D2', 'F\'', 'D2'])
            self.state_node.moves(['D2'])
            self.state_node.moves(['F\'', 'D\'', 'F', 'D\'', 'F\'', 'D2', 'F', 'D2'])

        elif status_corner_orintation == [1, 0, 0, 2]:  # 5 condition
            print('ok')
            self.state_node.moves(['R\'', 'D\'', 'R', 'D\'', 'R\'', 'D2', 'R', 'D2'])
            self.state_node.moves(['R', 'D', 'R\'', 'D', 'R', 'D2', 'R\'', 'D2'])
        elif status_corner_orintation == [2, 1, 0, 0]:
            print('ok')
            self.state_node.moves(['B\'', 'D\'', 'B', 'D\'', 'B\'', 'D2', 'B', 'D2'])
            self.state_node.moves(['B', 'D', 'B\'', 'D', 'B', 'D2', 'B\'', 'D2'])
        elif status_corner_orintation == [0, 2, 1, 0]:
            print('ok')
            self.state_node.moves(['L\'', 'D\'', 'L', 'D\'', 'L\'', 'D2', 'L', 'D2'])
            self.state_node.moves(['L', 'D', 'L\'', 'D', 'L', 'D2', 'L\'', 'D2'])
        elif status_corner_orintation == [0, 0, 2, 1]:
            print('ok')
            self.state_node.moves(['F\'', 'D\'', 'F', 'D\'', 'F\'', 'D2', 'F', 'D2'])
            self.state_node.moves(['F', 'D', 'F\'', 'D', 'F', 'D2', 'F\'', 'D2'])

        elif status_corner_orintation == [1, 0, 2, 0]:  # number 6 condition
            print('ok')
            self.state_node.moves(['D'])
            self.state_node.moves(['R', 'D', 'R\'', 'D', 'R', 'D2', 'R\'', 'D2'])
            self.state_node.moves(['D\''])
            self.state_node.moves(['R\'', 'D\'', 'R', 'D\'', 'R\'', 'D2', 'R', 'D2'])
        elif status_corner_orintation == [0, 1, 0, 2]:
            print(ree('check'))
            self.state_node.moves(['D'])
            self.state_node.moves(['B', 'D', 'B\'', 'D', 'B', 'D2', 'B\'', 'D2'])
            self.state_node.moves(['D\''])
            self.state_node.moves(['B\'', 'D\'', 'B', 'D\'', 'B\'', 'D2', 'B', 'D2'])
        elif status_corner_orintation == [2, 0, 1, 0]:
            print('ok')
            self.state_node.moves(['D'])
            self.state_node.moves(['L', 'D', 'L\'', 'D', 'L', 'D2', 'L\'', 'D2'])
            self.state_node.moves(['D\''])
            self.state_node.moves(['L\'', 'D\'', 'L', 'D\'', 'L\'', 'D2', 'L', 'D2'])
        elif status_corner_orintation == [0, 2, 0, 1]:
            print('ok')
            self.state_node.moves(['D'])
            self.state_node.moves(['F', 'D', 'F\'', 'D', 'F', 'D2', 'F\'', 'D2'])
            self.state_node.moves(['D\''])
            self.state_node.moves(['F\'', 'D\'', 'F', 'D\'', 'F\'', 'D2', 'F', 'D2'])

        elif status_corner_orintation == [1, 1, 2, 2]:  # number 7 condition
            print('ok')
            self.state_node.moves(['D\''])
            self.state_node.moves(['B', 'D', 'B\'', 'D', 'B', 'D2', 'B\'', 'D2'])
            self.state_node.moves(['D'])
            self.state_node.moves(['B', 'D', 'B\'', 'D', 'B', 'D2', 'B\'', 'D2'])
        elif status_corner_orintation == [2, 1, 1, 2]:
            print('ok')
            self.state_node.moves(['D\''])
            self.state_node.moves(['L', 'D', 'L\'', 'D', 'L', 'D2', 'L\'', 'D2'])
            self.state_node.moves(['D'])
            self.state_node.moves(['L', 'D', 'L\'', 'D', 'L', 'D2', 'L\'', 'D2'])
        elif status_corner_orintation == [2, 2, 1, 1]:
            print('ok')
            self.state_node.moves(['D\''])
            self.state_node.moves(['F', 'D', 'F\'', 'D', 'F', 'D2', 'F\'', 'D2'])
            self.state_node.moves(['D'])
            self.state_node.moves(['F', 'D', 'F\'', 'D', 'F', 'D2', 'F\'', 'D2'])
        elif status_corner_orintation == [1, 2, 2, 1]:
            print('ok')
            self.state_node.moves(['D\''])
            self.state_node.moves(['R', 'D', 'R\'', 'D', 'R', 'D2', 'R\'', 'D2'])
            self.state_node.moves(['D'])
            self.state_node.moves(['R', 'D', 'R\'', 'D', 'R', 'D2', 'R\'', 'D2'])

        elif status_corner_orintation == [1, 2, 1, 2]:  # 8 condition
            print(ree('ok'))
            self.state_node.moves(['D2'])
            self.state_node.moves(['B\'', 'D\'', 'B', 'D\'', 'B\'', 'D2', 'B', 'D2'])
            self.state_node.moves(['D2'])
            self.state_node.moves(['B\'', 'D\'', 'B', 'D\'', 'B\'', 'D2', 'B', 'D2'])
        elif status_corner_orintation == [2, 1, 2, 1]:
            print(ree('keep watching'))
            self.state_node.moves(['D2'])
            self.state_node.moves(['R\'', 'D\'', 'R', 'D\'', 'R\'', 'D2', 'R', 'D2'])
            self.state_node.moves(['D2'])
            self.state_node.moves(['R\'', 'D\'', 'R', 'D\'', 'R\'', 'D2', 'R', 'D2'])

        # print(self.state_node)

    def solve_edge_permutation(self):
        bottom_layer_edges = (1, 9, 2, 10)
        print(self.state_node)

        a12 = ['R2', 'D', 'B', 'F\'', 'R2', 'B\'', 'F', 'D', 'R2']
        acw12 = ['B2', 'D', 'L', 'R\'', 'B2', 'L\'', 'R', 'D', 'B2']
        a13 = ['R2', 'D\'', 'B', 'F\'', 'R2', 'B\'', 'F', 'D\'', 'R2']
        acw13 = ['B2', 'D\'', 'L', 'R\'', 'B2', 'L\'', 'R', 'D\'', 'B2']

        # status_corner_orintation = [self.state_node.co[co] for co in bottom_layer_corners]
        # correct_edge_permutation = [self.state_node.ep[ep] == ep for ep in bottom_layer_edges]

        status_edge_permutation = [self.state_node.ep[ep] for ep in bottom_layer_edges]
        print(yll(status_edge_permutation))

        if status_edge_permutation == [1, 9, 2, 10]:  # correct
            print('all good')
            return

        elif status_edge_permutation == [2, 10, 1, 9]:
            print('its cross OK')
            self.state_node.moves(['R2', 'D', 'B', 'F\'', 'R2', 'B\'', 'F', 'D', 'R2'])
            self.state_node.moves(['B2', 'D', 'L', 'R\'', 'B2', 'L\'', 'R', 'D', 'B2'])

        elif status_edge_permutation == [9, 1, 10, 2]: # """ swap diagolnals?? """
            print('ok')
            self.state_node.moves(['L2', 'D\'', 'F', 'B\'', 'L2', 'F\'', 'B', 'D\'', 'L2'])  # 1
            self.state_node.moves(['R2', 'D', 'B', 'F\'', 'R2', 'B\'', 'F', 'D', 'R2'])  # a13
        elif status_edge_permutation == [10, 2, 9, 1]:
            print('ok')
            # L L D' F B' L L F' B D' L L + a12
            self.state_node.moves(['R2', 'D', 'B', 'F\'', 'R2', 'B\'', 'F', 'D', 'R2'])
            self.state_node.moves(['L2', 'D\'', 'F', 'B\'', 'L2', 'F\'', 'B', 'D\'', 'L2'])

        elif status_edge_permutation == [1, 10, 9, 2]:
            print('ok')
            self.state_node.moves(['R2', 'D\'', 'B', 'F\'', 'R2', 'B\'', 'F', 'D\'', 'R2'])
        elif status_edge_permutation == [1, 2, 10, 9]:
            print('ok')
            self.state_node.moves(['R2', 'D', 'B', 'F\'', 'R2', 'B\'', 'F', 'D', 'R2'])

        elif status_edge_permutation == [10, 9, 1, 2]:
            print('ok')
            self.state_node.moves(['B2', 'D\'', 'L', 'R\'', 'B2', 'L\'', 'R', 'D\'', 'B2'])
        elif status_edge_permutation == [2, 9, 10, 1]:
            print('ok')
            self.state_node.moves(['B2', 'D', 'L', 'R\'', 'B2', 'L\'', 'R', 'D', 'B2'])

        elif status_edge_permutation == [10, 1, 2, 9]:
            print('ok')
            self.state_node.moves(['L2', 'D\'', 'F', 'B\'', 'L2', 'F\'', 'B', 'D\'', 'L2'])
        elif status_edge_permutation == [9, 10, 2, 1]:
            print('ok')
            self.state_node.moves(['L2', 'D', 'F', 'B\'', 'L2', 'F\'', 'B', 'D', 'L2'])

        elif status_edge_permutation == [2, 1, 9, 10]:
            print('ok')
            self.state_node.moves(['F2', 'D\'', 'R', 'L\'', 'F2', 'R\'', 'L', 'D\'', 'F2'])
        elif status_edge_permutation == [9, 2, 1, 10]:
            print('ok')
            self.state_node.moves(['F2', 'D', 'R', 'L\'', 'F2', 'R\'', 'L', 'D', 'F2'])

        print(gre([self.state_node.ep[ep] for ep in bottom_layer_edges]))
        print(gre(self.state_node))


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
randm = make_random_state()
# randm =  ['R2', "U'", 'D2', 'D', 'L2', 'R2', "B'", 'F', 'B', 'U', 'B2', "L'", 'U', 'U2', 'L2', "D'", "B'", "F'", 'U', 'F2', 'R', 'B', 'F', "L'", 'D', 'L', 'D', "R'", 'D2', 'R', 'D', "R'", "D'", 'R', "L'", 'D', 'L', 'D', "L'", 'D', 'L', 'D', "F'", "D'", 'F', "L'", 'D', 'L', 'D', "B'", 'D2', 'B', 'D', "B'", "D'", 'B', "L'", 'D', 'L', 'D', "L'", 'D', 'L', 'D', "L'", 'D2', 'L', 'D', "L'", "D'", 'L', 'D', 'D', 'B', "D'", "B'", "D'", "L'", 'D', 'L', 'D', 'L', "D'", "L'", "D'", "F'", 'D', 'F', 'L', "D'", "L'", 'F', "L'", "F'", 'L', "D'", 'L', "D'", "L'", 'F', "L'", "F'", 'L', "D'", 'D', 'B', "D'", "B'", 'L', "B'", "L'", 'B', "D'", 'B', "D'", "B'", 'L', "B'", "L'", 'B', "D'", 'D', "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", 'F', "D'", "F'", 'R', "F'", "R'", 'F', "D'", 'F', "D'", "F'", 'R', "F'", "R'", 'F', "D'", "D'", "B'", 'D', 'B', 'D', 'R', "D'", "R'", 'D', "D'", "B'", 'D', 'B', 'D', 'R', "D'", "R'", 'D', 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", 'B', 'D', 'R', "D'", "R'", "B'"]
# randm = 1212 ["U'", 'D', 'D', 'R2', "U'", "U'", 'D', "D'", 'B2', "L'", 'U', 'D', "B'", 'R', 'F2', 'U2', 'L2', 'D2', 'B2', 'F']
# randm = 2121 ['R2', "R'", 'D2', 'R2', 'D2', 'F', 'R2', "U'", 'L', 'F2', 'U', "L'", 'R', 'R', "D'", 'L2', "F'", 'R', 'D', 'R2', 'B2', 'B', 'D', "B'", "D'", 'B', 'D', "B'", "D'", "B'", 'D', 'B', 'D', 'R', 'D', "R'", "D'", 'R', 'D', "R'", "D'", "R'", 'D2', 'R', 'D', "R'", "D'", 'R', 'D', 'B', "D'", "B'", 'L', "B'", "L'", 'B', "D'", 'B', "D'", "B'", 'L', "B'", "L'", 'B', "D'", "D'", "B'", 'D', 'B', 'D', 'R', "D'", "R'", 'D', 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", 'D', 'B', 'D', 'R', "D'", "R'", "B'"]
# randm =  ['R2', 'D', "F'", 'U', 'F2', 'U2', 'U', 'L', "U'", 'D2', 'U2', 'B2', "B'", "D'", "L'", 'F2', 'R2', 'F', 'D', "R'", 'B2', "L'", 'D2', 'L', 'D', "L'", "D'", 'L', 'R', 'D', "R'", "D'", 'R', 'D', "R'", "D'", "R'", 'D', 'R', 'D', "R'", "D'", 'R', 'D', "D'", "L'", 'D', 'L', 'D', 'B', "D'", "B'", 'D', 'R', "D'", "R'", "D'", "B'", 'D', 'B', 'F', "D'", "F'", 'R', "F'", "R'", 'F', "D'", 'F', "D'", "F'", 'R', "F'", "R'", 'F', "D'", 'D', 'D', 'D', 'B', 'D', 'R', "D'", "R'", "B'"]
# randm =  ['U', "D'", 'B', 'U', "L'", 'F2', "D'", 'L', "B'", 'D2', 'D2', 'U', "R'", 'B2', 'R2', "F'", 'B', 'R', "D'", "F'", 'R', "L'", 'L', 'D', "L'"]
# randm with 1 yellow center = ["B'", 'U', 'D2', 'L2', "D'", "F'", 'F2', "F'", 'F2', 'L2', 'D2', 'R', 'U', "R'", "R'", 'R', 'F2', "L'", "D'", 'B', 'R2', "B'", "D'", 'B', 'D', "B'", "D'", 'B', 'D', "L'", 'D', 'L', 'D', "L'", 'D', 'L', 'D', "L'", 'D', 'L', 'D', "R'", 'D2', 'R', 'D', "R'", "D'", 'R', "L'", 'D', 'L', 'D', "F'", 'D2', 'F', 'D', "F'", "D'", 'F', "L'", 'D', 'L', 'D', 'B', 'D', "B'", "D'", 'B', 'D', "B'", "D'", 'D', 'D', 'D', "D'", "L'", 'D', 'L', 'D', 'B', "D'", "B'", 'D', 'R', "D'", "R'", "D'", "B'", 'D', 'B', "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", "D'", "F'", 'D', 'F', 'D', 'L', "D'", "L'", 'D', 'D', "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", 'D']
# print(randm)
kek.moves(randm)
# kek.moves(["D'", 'U', 'B', 'D2', 'D2', "D'", "L'", "R'", "L'", 'L2', "D'", 'L', "B'", "U'", 'F2', 'L', 'F', "D'", "L'", 'F', 'B2'])
# print(kek)
# exit()

solv = Solver(kek)
# print(kek)

# if d2 and d2 - del all in history


