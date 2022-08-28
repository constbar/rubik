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
# permutaion rename in position

import tests
import os
import re
import numpy
import time
import copy
import logging
import timeit
from rubik_state import RubikState
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


class Solver:
    # __slots__ =
    possible_notations = ['L', 'L2', 'L\'', 'R', 'R2', 'R\'', # maybe better place it in rubik state
                          'F', 'F2', 'F\'', 'B', 'B2', 'B\'',
                          'U', 'U2', 'U\'', 'D', 'D2', 'D\'']

    def __init__(self, shuffled_rubik_state):
        self.rubik_state = shuffled_rubik_state
        # print('!!!!!!!!!!!!!!!!!!', len(self.state_node.notation_history))

        self.solve_top_layer_cross()

        print(yll(self.rubik_state))
        print(yll(self.rubik_state.notation_path))

        # exit()
        print(gre('after of first cross stage'), gre(len(self.rubik_state.notation_path)))
        self.solve_top_layer_corners()
        print('after solving first top layer', len(self.rubik_state.notation_path))
        self.solve_middle_layer_edges()
        print('after solving middle layer', len(self.rubik_state.notation_path))
        self.solve_bottom_layer_cross()
        print('history after bottom layer\n', self.rubik_state.notation_path)
        self.solve_positions_bottom_layer_corners()
        self.solve_orientations_bottom_layer_corners()
        self.solve_positions_bottom_layer_edges()
        print('history after all\n', len(self.rubik_state.notation_path))

    def solve_top_layer_cross(self):
        """
        at this stage, a cross is assembled on the top layer. most often the top layer in the rubik is white.
        the edges of the cross will be in the correct positions and correct orientations.
        the correct location of the edges of the cross of the upper layer looks like this
        ▢  11 ▢
        0  ▢  3
        ▢  8  ▢
        at this stage, to optimize the number of moves, the ida star search algorithm is used to achieve
        the target state of the stage
        """
        open_list = PriorityQueue()
        threshold = self.rubik_state.f_cost

        while 42:
            open_list.put(self.rubik_state)
            thresholds = list()

            while open_list.qsize():
                lowest_cost_state = open_list.get()
                if lowest_cost_state.is_target_state() is True:
                    self.rubik_state = lowest_cost_state
                    return

                for notation in Solver.possible_notations:
                    new_state = RubikState(lowest_cost_state.properties, lowest_cost_state.make_line_state(),
                                           notation, copy.deepcopy(lowest_cost_state.notation_path))
                    if new_state.f_cost <= threshold:
                        open_list.put(new_state)
                    else:
                        thresholds.append(new_state.f_cost)
            threshold = min(thresholds)

    def solve_top_layer_corners(self):
        """
        at this stage, need to bring the corners of the top layer to the correct
        positions and in the correct orientations.
        work goes with the corners of the top layer, look like this
        0  ▢  7
        ▢  ▢  ▢
        4  ▢  3
        each corner has an orientation of 0, 1 or 2, need to bring all corner orientations to 0
        """
        up_layer_corners = (0, 7, 3, 4)
        is_correct_corner_position = lambda: all(self.rubik_state.cp[cp] == cp for cp in up_layer_corners)
        is_correct_corner_orientation = lambda: all(self.rubik_state.co[cp] == 0 for cp in up_layer_corners)

        while is_correct_corner_position() is False or is_correct_corner_orientation() is False:
            for corner in up_layer_corners:
                """each corner has a state 0 or 1 or 2. in else performs 1 or 2 orientations"""
                if self.rubik_state.cp[corner] == corner:
                    if self.rubik_state.co[corner] == 0:
                        """ case where the corner is in its place and with a right orientation """
                        continue
                    else:
                        """ cases where the corner is in its place and with the wrong orientation """
                        if corner == 0:
                            if self.rubik_state.co[corner] == 1:
                                self.rubik_state.make_move(['B', 'D', 'B\'', 'D\''] * 2)
                            elif self.rubik_state.co[corner] == 2:
                                self.rubik_state.make_move(['L\'', 'D\'', 'L', 'D'] * 2)
                        elif corner == 7:
                            if self.rubik_state.co[corner] == 1:
                                self.rubik_state.make_move(['R', 'D', 'R\'', 'D\''] * 2)
                            elif self.rubik_state.co[corner] == 2:
                                self.rubik_state.make_move(['B\'', 'D\'', 'B', 'D'] * 2)
                        elif corner == 3:
                            if self.rubik_state.co[corner] == 1:
                                self.rubik_state.make_move(['F', 'D', 'F\'', 'D\''] * 2)
                            elif self.rubik_state.co[corner] == 2:
                                self.rubik_state.make_move(['R\'', 'D\'', 'R', 'D'] * 2)
                        elif corner == 4:
                            if self.rubik_state.co[corner] == 1:
                                self.rubik_state.make_move(['L', 'D', 'L\'', 'D\''] * 2)
                            elif self.rubik_state.co[corner] == 2:
                                self.rubik_state.make_move(['F\'', 'D\'', 'F', 'D'] * 2)
                else:
                    """ cases where need to bring all the corners to their correct positions """
                    if self.rubik_state.cp[5] == 0:
                        if self.rubik_state.co[0] == 0:
                            self.rubik_state.make_move(['B', 'D', 'B\''])
                        elif self.rubik_state.co[0] == 1:
                            self.rubik_state.make_move(['L\'', 'D2', 'L', 'D', 'L\'', 'D\'', 'L'])
                        elif self.rubik_state.co[0] == 2:
                            self.rubik_state.make_move(['L\'', 'D\'', 'L'])
                    elif self.rubik_state.cp[2] == 7:
                        if self.rubik_state.co[7] == 0:
                            self.rubik_state.make_move(['B\'', 'D\'', 'B'])
                        elif self.rubik_state.co[7] == 1:
                            self.rubik_state.make_move(['R', 'D', 'R\''])
                        elif self.rubik_state.co[7] == 2:
                            self.rubik_state.make_move(['B\'', 'D2', 'B', 'D', 'B\'', 'D\'', 'B'])
                    elif self.rubik_state.cp[6] == 3:
                        if self.rubik_state.co[3] == 0:
                            self.rubik_state.make_move(['F', 'D', 'F\''])
                        elif self.rubik_state.co[3] == 1:
                            self.rubik_state.make_move(['R\'', 'D2', 'R', 'D', 'R\'', 'D\'', 'R'])
                        elif self.rubik_state.co[3] == 2:
                            self.rubik_state.make_move(['R\'', 'D\'', 'R'])
                    elif self.rubik_state.cp[1] == 4:
                        if self.rubik_state.co[4] == 0:
                            self.rubik_state.make_move(['F\'', 'D\'', 'F'])
                        elif self.rubik_state.co[4] == 1:
                            self.rubik_state.make_move(['L', 'D', 'L\''])
                        elif self.rubik_state.co[4] == 2:
                            self.rubik_state.make_move(['F\'', 'D2', 'F', 'D', 'F\'', 'D\'', 'F'])

            if is_correct_corner_position() is True and is_correct_corner_orientation() is True:
                return

            """ block with cases when all corners are not in their positions and offsets are needed """
            if self.rubik_state.cp[0] != 0:
                self.rubik_state.make_move(['L\'', 'D', 'L'])
            elif self.rubik_state.cp[7] != 7:
                self.rubik_state.make_move(['B\'', 'D', 'B'])
            elif self.rubik_state.cp[3] != 3:
                self.rubik_state.make_move(['R\'', 'D', 'R'])
            elif self.rubik_state.cp[4] != 4:
                self.rubik_state.make_move(['F\'', 'D', 'F'])
            self.rubik_state.make_move(['D'])

    def solve_middle_layer_edges(self):
        """
        at this stage, need to bring the edges of the middle layer to the correct positions and orientations.
        as a result of this stage, the top 2 rubik's layers will be solved.
        work goes with the edges of the middle layer, look like this
        4  ▢  7
        ▢  ▢  ▢
        5  ▢  6
        """
        mid_layer_edges = (4, 7, 6, 5)
        is_correct_edge_position = lambda: all(self.rubik_state.ep[ep] == ep for ep in mid_layer_edges)
        is_correct_edge_orientation = lambda: all(self.rubik_state.eo[ep] == 0 for ep in mid_layer_edges)

        i = 1
        while is_correct_edge_position() is False or is_correct_edge_orientation() is False:
            for edge in mid_layer_edges:
                if self.rubik_state.ep[edge] == edge:
                    if self.rubik_state.eo[edge] == 0:
                        """ case where the edge is in its place and with a right orientation """
                        continue
                    else:
                        """ cases where the edge is in its place and with the wrong orientation, 
                        this edge just needs to be turned over """
                        if edge == 4:
                            self.rubik_state.make_move(['B', 'D\'', 'B\'', 'L', 'B\'', 'L\'', 'B', 'D\''] * 2)
                        elif edge == 7:
                            self.rubik_state.make_move(['R', 'D\'', 'R\'', 'B', 'R\'', 'B\'', 'R', 'D\''] * 2)
                        elif edge == 6:
                            self.rubik_state.make_move(['F', 'D\'', 'F\'', 'R', 'F\'', 'R\'', 'F', 'D\''] * 2)
                        elif edge == 5:
                            self.rubik_state.make_move(['L', 'D\'', 'L\'', 'F', 'L\'', 'F\'', 'L', 'D\''] * 2)
                else:
                    """ cases where need to bring all the edges to their correct positions """
                    if self.rubik_state.ep[1] == 4:
                        self.rubik_state.make_move(['D', 'B', 'D\'', 'B\'', 'D\'', 'L\'', 'D', 'L'])
                    elif self.rubik_state.ep[10] == 4:
                        self.rubik_state.make_move(['D\'', 'L\'', 'D', 'L', 'D', 'B', 'D\'', 'B\''])
                    elif self.rubik_state.ep[10] == 7:
                        self.rubik_state.make_move(['D', 'R', 'D\'', 'R\'', 'D\'', 'B\'', 'D', 'B'])
                    elif self.rubik_state.ep[2] == 7:
                        self.rubik_state.make_move(['D\'', 'B\'', 'D', 'B', 'D', 'R', 'D\'', 'R\''])
                    elif self.rubik_state.ep[2] == 6:
                        self.rubik_state.make_move(['D', 'F', 'D\'', 'F\'', 'D\'', 'R\'', 'D', 'R'])
                    elif self.rubik_state.ep[9] == 6:
                        self.rubik_state.make_move(['D\'', 'R\'', 'D', 'R', 'D', 'F', 'D\'', 'F\''])
                    elif self.rubik_state.ep[9] == 5:
                        self.rubik_state.make_move(['D', 'L', 'D\'', 'L\'', 'D\'', 'F\'', 'D', 'F'])
                    elif self.rubik_state.ep[1] == 5:
                        self.rubik_state.make_move(['D\'', 'F\'', 'D', 'F', 'D', 'L', 'D\'', 'L\''])

            if is_correct_edge_position() is True and is_correct_edge_orientation() is True:
                return

            """ block with cases where all the edges are not in their positions and offsets are needed """
            if i % 3:
                self.rubik_state.make_move(['D'])
            else:
                if self.rubik_state.ep[4] != 4:
                    self.rubik_state.make_move(['D\'', 'L\'', 'D', 'L', 'D', 'B', 'D\'', 'B\''])
                elif self.rubik_state.ep[7] != 7:
                    self.rubik_state.make_move(['D\'', 'B\'', 'D', 'B', 'D', 'R', 'D\'', 'R\''])
                elif self.rubik_state.ep[6] != 6:
                    self.rubik_state.make_move(['D\'', 'R\'', 'D', 'R', 'D', 'F', 'D\'', 'F\''])
                elif self.rubik_state.ep[5] != 5:
                    self.rubik_state.make_move(['D\'', 'F\'', 'D', 'F', 'D', 'L', 'D\'', 'L\''])
                i = 0
            i += 1

    def solve_bottom_layer_cross(self):
        """
        at this stage, a cross is built on the bottom layer. most often in rubik it is yellow.
        to look at the bottom layer correctly, mentally rotate the rubik along the X axis 2 times.
        this notation is called X2 for cube rotation as R2.
        the correct location of the edges of the cross of the bottom layer looks like this
        ▢  9  ▢
        1  ▢  2
        ▢  10 ▢
        the correct cross is checked by the bar from the left to the right side and
        the bar from the front to the back side.

        1  ▢  2 - from left to right bar

        9 - from back to front bar
        ▢
        10
        """
        if self.rubik_state.bottom[0][1] != self.rubik_state.bottom[1][1] and \
                self.rubik_state.bottom[1][0] != self.rubik_state.bottom[1][1] and \
                self.rubik_state.bottom[1][2] != self.rubik_state.bottom[1][1] and \
                self.rubik_state.bottom[2][1] != self.rubik_state.bottom[1][1]:
            """ a state where only the center is on the layer in the correct place """
            self.rubik_state.make_move(['B', 'R', 'D', 'R\'', 'D\'', 'B\'',
                                        'D2', 'B', 'R', 'D', 'R\'', 'D\'', 'B\''])

        left_right_bar = set(self.rubik_state.bottom[1])
        back_front_bar = set(self.rubik_state.bottom[:, 1])

        if len(left_right_bar) != 1 or len(back_front_bar) != 1:
            if len(left_right_bar) == 1 or len(back_front_bar) == 1:
                if len(back_front_bar) == 1:
                    """ to apply the moves, need to bring the bf bar to lr bar """
                    self.rubik_state.make_move(['D'])
                """ to apply the moves that makes a cross from lr bar """
                self.rubik_state.make_move(['B', 'R', 'D', 'R\'', 'D\'', 'B\''])
            else:
                compare_one_color_small_l_shape = lambda: \
                    self.rubik_state.bottom[1][0] == \
                    self.rubik_state.bottom[1][1] == \
                    self.rubik_state.bottom[0][1]
                while compare_one_color_small_l_shape() is False:
                    """
                    to apply further the moves, need to bring the 'small l' 
                    to one color in this state on the layer
                       9
                    1  ▢
                    """
                    self.rubik_state.make_move(['D'])
                self.rubik_state.make_move(['B', 'D', 'R', 'D\'', 'R\'', 'B\''])
        else:
            """ target stage already reached """
            return

    def solve_positions_bottom_layer_corners(self):
        """
        at this stage, the corners should be in the correct positions.
        the correct location of the corners of the bottom layer looks like this
        1  ▢  6
        ▢  ▢  ▢
        5  ▢  2
        """
        bottom_layer_corner_target_positions = (1, 6, 2, 5)
        get_current_bool_corner_positions = lambda: [self.rubik_state.cp[cp] == cp
                                                     for cp in bottom_layer_corner_target_positions]

        while all(get_current_bool_corner_positions()) is False:
            while get_current_bool_corner_positions().count(True) < 2:
                self.rubik_state.make_move(['D'])

            if all(get_current_bool_corner_positions()) is True:
                return

            """ the positions of the corners at this stage can be in different variations.
            like [True, True, False, False] or [False, True, True, False] and so on.
            condition works if 2 corners are in their correct places and they are together """
            if get_current_bool_corner_positions()[0] is get_current_bool_corner_positions()[1] is True:
                self.rubik_state.make_move(['F', 'D\'', 'B\'', 'D', 'F\'', 'D\'', 'B', 'D2'])
            elif get_current_bool_corner_positions()[1] is get_current_bool_corner_positions()[2] is True:
                self.rubik_state.make_move(['R', 'D\'', 'L\'', 'D', 'R\'', 'D\'', 'L', 'D2'])
            elif get_current_bool_corner_positions()[2] is get_current_bool_corner_positions()[3] is True:
                self.rubik_state.make_move(['B', 'D\'', 'F\'', 'D', 'B\'', 'D\'', 'F', 'D2'])
            elif get_current_bool_corner_positions()[3] is get_current_bool_corner_positions()[0] is True:
                self.rubik_state.make_move(['L', 'D\'', 'R\'', 'D', 'L\'', 'D\'', 'R', 'D2'])

            if all(get_current_bool_corner_positions()) is True:
                return

            """ condition works if 2 corners are in their correct places and are opposite each other """
            if get_current_bool_corner_positions()[0] is True:
                self.rubik_state.make_move(['F', 'D\'', 'B\'', 'D', 'F\'', 'D\'', 'B', 'D2'])
            elif get_current_bool_corner_positions()[1] is True:
                self.rubik_state.make_move(['R', 'D\'', 'L\'', 'D', 'R\'', 'D\'', 'L', 'D2'])

    def solve_orientations_bottom_layer_corners(self):
        """
        at this stage, the corners should be in the correct orientation.
        i.e. the orientations of all corners must be 0.
        the location of the corners of the bottom layer for which the
        correct orientation is needed look like this
        1  ▢  6
        ▢  ▢  ▢
        5  ▢  2
        in total 8 possible options for the orientations of the corners of
        the bottom layer. each of them is separated into a block
        """
        bottom_layer_corner_target_orientations = (1, 6, 2, 5)
        current_corner_orientation = [self.rubik_state.co[co] for co in bottom_layer_corner_target_orientations]
        match current_corner_orientation:
            case [0, 0, 0, 0]:
                """ target stage already reached """
                return

            case [0, 1, 1, 1]:
                self.rubik_state.make_move(['B', 'D', 'B\'', 'D', 'B', 'D2', 'B\'', 'D2'])
            case [1, 0, 1, 1]:
                self.rubik_state.make_move(['L', 'D', 'L\'', 'D', 'L', 'D2', 'L\'', 'D2'])
            case [1, 1, 0, 1]:
                self.rubik_state.make_move(['F', 'D', 'F\'', 'D', 'F', 'D2', 'F\'', 'D2'])
            case [1, 1, 1, 0]:
                self.rubik_state.make_move(['R', 'D', 'R\'', 'D', 'R', 'D2', 'R\'', 'D2'])

            case [0, 2, 2, 2]:
                self.rubik_state.make_move(['R\'', 'D\'', 'R', 'D\'', 'R\'', 'D2', 'R', 'D2'])
            case [2, 0, 2, 2]:
                self.rubik_state.make_move(['B\'', 'D\'', 'B', 'D\'', 'B\'', 'D2', 'B', 'D2'])
            case [2, 2, 0, 2]:
                self.rubik_state.make_move(['L\'', 'D\'', 'L', 'D\'', 'L\'', 'D2', 'L', 'D2'])
            case [2, 2, 2, 0]:
                self.rubik_state.make_move(['F\'', 'D\'', 'F', 'D\'', 'F\'', 'D2', 'F', 'D2'])

            case [1, 2, 0, 0]:
                self.rubik_state.make_move(['D2'])
                self.rubik_state.make_move(['R', 'D', 'R\'', 'D', 'R', 'D2', 'R\'', 'D2'])
                self.rubik_state.make_move(['D2'])
                self.rubik_state.make_move(['R\'', 'D\'', 'R', 'D\'', 'R\'', 'D2', 'R', 'D2'])
            case [0, 1, 2, 0]:
                self.rubik_state.make_move(['D2'])
                self.rubik_state.make_move(['B', 'D', 'B\'', 'D', 'B', 'D2', 'B\'', 'D2'])
                self.rubik_state.make_move(['D2'])
                self.rubik_state.make_move(['B\'', 'D\'', 'B', 'D\'', 'B\'', 'D2', 'B', 'D2'])
            case [0, 0, 1, 2]:
                self.rubik_state.make_move(['D2'])
                self.rubik_state.make_move(['L', 'D', 'L\'', 'D', 'L', 'D2', 'L\'', 'D2'])
                self.rubik_state.make_move(['D2'])
                self.rubik_state.make_move(['L\'', 'D\'', 'L', 'D\'', 'L\'', 'D2', 'L', 'D2'])
            case [2, 0, 0, 1]:
                self.rubik_state.make_move(['D2'])
                self.rubik_state.make_move(['F', 'D', 'F\'', 'D', 'F', 'D2', 'F\'', 'D2'])
                self.rubik_state.make_move(['D2'])
                self.rubik_state.make_move(['F\'', 'D\'', 'F', 'D\'', 'F\'', 'D2', 'F', 'D2'])

            case [1, 0, 0, 2]:
                self.rubik_state.make_move(['R\'', 'D\'', 'R', 'D\'', 'R\'', 'D2', 'R', 'D2'])
                self.rubik_state.make_move(['R', 'D', 'R\'', 'D', 'R', 'D2', 'R\'', 'D2'])
            case [2, 1, 0, 0]:
                self.rubik_state.make_move(['B\'', 'D\'', 'B', 'D\'', 'B\'', 'D2', 'B', 'D2'])
                self.rubik_state.make_move(['B', 'D', 'B\'', 'D', 'B', 'D2', 'B\'', 'D2'])
            case [0, 2, 1, 0]:
                self.rubik_state.make_move(['L\'', 'D\'', 'L', 'D\'', 'L\'', 'D2', 'L', 'D2'])
                self.rubik_state.make_move(['L', 'D', 'L\'', 'D', 'L', 'D2', 'L\'', 'D2'])
            case [0, 0, 2, 1]:
                self.rubik_state.make_move(['F\'', 'D\'', 'F', 'D\'', 'F\'', 'D2', 'F', 'D2'])
                self.rubik_state.make_move(['F', 'D', 'F\'', 'D', 'F', 'D2', 'F\'', 'D2'])

            case [1, 0, 2, 0]:
                self.rubik_state.make_move(['D'])
                self.rubik_state.make_move(['R', 'D', 'R\'', 'D', 'R', 'D2', 'R\'', 'D2'])
                self.rubik_state.make_move(['D\''])
                self.rubik_state.make_move(['R\'', 'D\'', 'R', 'D\'', 'R\'', 'D2', 'R', 'D2'])
            case [0, 1, 0, 2]:
                self.rubik_state.make_move(['D'])
                self.rubik_state.make_move(['B', 'D', 'B\'', 'D', 'B', 'D2', 'B\'', 'D2'])
                self.rubik_state.make_move(['D\''])
                self.rubik_state.make_move(['B\'', 'D\'', 'B', 'D\'', 'B\'', 'D2', 'B', 'D2'])
            case [2, 0, 1, 0]:
                self.rubik_state.make_move(['D'])
                self.rubik_state.make_move(['L', 'D', 'L\'', 'D', 'L', 'D2', 'L\'', 'D2'])
                self.rubik_state.make_move(['D\''])
                self.rubik_state.make_move(['L\'', 'D\'', 'L', 'D\'', 'L\'', 'D2', 'L', 'D2'])
            case [0, 2, 0, 1]:
                self.rubik_state.make_move(['D'])
                self.rubik_state.make_move(['F', 'D', 'F\'', 'D', 'F', 'D2', 'F\'', 'D2'])
                self.rubik_state.make_move(['D\''])
                self.rubik_state.make_move(['F\'', 'D\'', 'F', 'D\'', 'F\'', 'D2', 'F', 'D2'])

            case [1, 1, 2, 2]:
                self.rubik_state.make_move(['D\''])
                self.rubik_state.make_move(['B', 'D', 'B\'', 'D', 'B', 'D2', 'B\'', 'D2'])
                self.rubik_state.make_move(['D'])
                self.rubik_state.make_move(['B', 'D', 'B\'', 'D', 'B', 'D2', 'B\'', 'D2'])
            case [2, 1, 1, 2]:
                self.rubik_state.make_move(['D\''])
                self.rubik_state.make_move(['L', 'D', 'L\'', 'D', 'L', 'D2', 'L\'', 'D2'])
                self.rubik_state.make_move(['D'])
                self.rubik_state.make_move(['L', 'D', 'L\'', 'D', 'L', 'D2', 'L\'', 'D2'])
            case [2, 2, 1, 1]:
                self.rubik_state.make_move(['D\''])
                self.rubik_state.make_move(['F', 'D', 'F\'', 'D', 'F', 'D2', 'F\'', 'D2'])
                self.rubik_state.make_move(['D'])
                self.rubik_state.make_move(['F', 'D', 'F\'', 'D', 'F', 'D2', 'F\'', 'D2'])
            case [1, 2, 2, 1]:
                self.rubik_state.make_move(['D\''])
                self.rubik_state.make_move(['R', 'D', 'R\'', 'D', 'R', 'D2', 'R\'', 'D2'])
                self.rubik_state.make_move(['D'])
                self.rubik_state.make_move(['R', 'D', 'R\'', 'D', 'R', 'D2', 'R\'', 'D2'])

            case [1, 2, 1, 2]:
                self.rubik_state.make_move(['D2'])
                self.rubik_state.make_move(['B\'', 'D\'', 'B', 'D\'', 'B\'', 'D2', 'B', 'D2'])
                self.rubik_state.make_move(['D2'])
                self.rubik_state.make_move(['B\'', 'D\'', 'B', 'D\'', 'B\'', 'D2', 'B', 'D2'])
            case [2, 1, 2, 1]:
                self.rubik_state.make_move(['D2'])
                self.rubik_state.make_move(['R\'', 'D\'', 'R', 'D\'', 'R\'', 'D2', 'R', 'D2'])
                self.rubik_state.make_move(['D2'])
                self.rubik_state.make_move(['R\'', 'D\'', 'R', 'D\'', 'R\'', 'D2', 'R', 'D2'])

    def solve_positions_bottom_layer_edges(self):
        """
        at this stage, the edges should be in the correct positions.
        target positions of the bottom layer edges look like this
        ▢  9  ▢
        1  ▢  2
        ▢  10 ▢
        """
        bottom_layer_edge_target_positions = (1, 9, 2, 10)
        current_edge_position = [self.rubik_state.ep[ep] for ep in bottom_layer_edge_target_positions]

        match current_edge_position:
            case [1, 9, 2, 10]:
                """ target stage already reached """
                return

            case [2, 10, 1, 9]:
                """ edge state in which the edges are opposite their target positions """
                self.rubik_state.make_move(['R2', 'D', 'B', 'F\'', 'R2', 'B\'', 'F', 'D', 'R2'])
                self.rubik_state.make_move(['B2', 'D', 'L', 'R\'', 'B2', 'L\'', 'R', 'D', 'B2'])

            case [9, 1, 10, 2]:
                """ edge state block where edges are diagonal from their target states """
                self.rubik_state.make_move(['L2', 'D\'', 'F', 'B\'', 'L2', 'F\'', 'B', 'D\'', 'L2'])
                self.rubik_state.make_move(['R2', 'D', 'B', 'F\'', 'R2', 'B\'', 'F', 'D', 'R2'])
            case [10, 2, 9, 1]:
                self.rubik_state.make_move(['R2', 'D', 'B', 'F\'', 'R2', 'B\'', 'F', 'D', 'R2'])
                self.rubik_state.make_move(['L2', 'D\'', 'F', 'B\'', 'L2', 'F\'', 'B', 'D\'', 'L2'])

            case [1, 10, 9, 2]:
                """ edge state block where the 3 right edges are out of place. depending on the 
                current position, these 3 wrong edges need to be moved clockwise or counterclockwise """
                self.rubik_state.make_move(['R2', 'D\'', 'B', 'F\'', 'R2', 'B\'', 'F', 'D\'', 'R2'])
            case [1, 2, 10, 9]:
                self.rubik_state.make_move(['R2', 'D', 'B', 'F\'', 'R2', 'B\'', 'F', 'D', 'R2'])
            case [10, 9, 1, 2]:
                self.rubik_state.make_move(['B2', 'D\'', 'L', 'R\'', 'B2', 'L\'', 'R', 'D\'', 'B2'])
            case [2, 9, 10, 1]:
                self.rubik_state.make_move(['B2', 'D', 'L', 'R\'', 'B2', 'L\'', 'R', 'D', 'B2'])
            case [10, 1, 2, 9]:
                self.rubik_state.make_move(['L2', 'D\'', 'F', 'B\'', 'L2', 'F\'', 'B', 'D\'', 'L2'])
            case [9, 10, 2, 1]:
                self.rubik_state.make_move(['L2', 'D', 'F', 'B\'', 'L2', 'F\'', 'B', 'D', 'L2'])
            case [2, 1, 9, 10]:
                self.rubik_state.make_move(['F2', 'D\'', 'R', 'L\'', 'F2', 'R\'', 'L', 'D\'', 'F2'])
            case [9, 2, 1, 10]:
                self.rubik_state.make_move(['F2', 'D', 'R', 'L\'', 'F2', 'R\'', 'L', 'D', 'F2'])

            case _:# DELETE IT
                print(ree("THIS CASE NOT EXISTS!!!"))




def make_random_state():
    config_dict = {
        '3x3x3': {
            # goal state ??
            # 'subgroup_0_moves': ['U', 'D', 'L', 'R', 'F', 'B'],
            # 'subgroup_0_moves': ['L', 'R', 'F', 'B', 'U', 'D'],
            # 'stage_0_moves': ['L', 'R', 'F', 'B', 'U', 'D'],
            'stage_0_moves': ["L", "L'", "L2", "R", "R'", "R2", "F", "F'", "F2", "B", "B'", "B2", "U", "U'", "U2", "D",
                              "D'", "D2"],
            'stage_1_moves': ['L', 'R', 'F', 'B', 'U2', 'D2'],
            'stage_2_moves': ['L', 'R', 'F', 'B', 'U2', 'D2'],
        }
    }

    random_list = []
    # for i in range(0, 15):
    for i in range(0, 20):
        n = randint(0, 17)
        random_list.append(config_dict['3x3x3']['stage_0_moves'][n])
    # print(random_list)
    # need to remove first 15 turns
    return random_list


test = tests.clear_state
# test = tests.test6

kek = RubikState(test['cepo'], test['faces'], None, None)
randm = make_random_state()
# randm =  ['L', 'R', "B'", "F'", 'R2', "D'", 'D', 'F', 'D2', "B'", 'U', 'B2', "B'", 'B2', 'L', "F'", 'L2', 'D', 'R', "F'", "F'", "D'", 'F', 'D']
# randm = cross ["U'", 'F2', 'D', 'L', "D'", 'D2', "B'", "R'", "D'", "B'", "L'", 'U', 'L2', "B'", 'B', "R'", "D'", 'F', 'R', 'F', "L'"]
# randm = 1212 ["U'", 'D', 'D', 'R2', "U'", "U'", 'D', "D'", 'B2', "L'", 'U', 'D', "B'", 'R', 'F2', 'U2', 'L2', 'D2', 'B2', 'F']
# randm = 2121 ['R2', "R'", 'D2', 'R2', 'D2', 'F', 'R2', "U'", 'L', 'F2', 'U', "L'", 'R', 'R', "D'", 'L2', "F'", 'R', 'D', 'R2', 'B2', 'B', 'D', "B'", "D'", 'B', 'D', "B'", "D'", "B'", 'D', 'B', 'D', 'R', 'D', "R'", "D'", 'R', 'D', "R'", "D'", "R'", 'D2', 'R', 'D', "R'", "D'", 'R', 'D', 'B', "D'", "B'", 'L', "B'", "L'", 'B', "D'", 'B', "D'", "B'", 'L', "B'", "L'", 'B', "D'", "D'", "B'", 'D', 'B', 'D', 'R', "D'", "R'", 'D', 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", 'D', 'B', 'D', 'R', "D'", "R'", "B'"]
# randm =  ['R2', 'D', "F'", 'U', 'F2', 'U2', 'U', 'L', "U'", 'D2', 'U2', 'B2', "B'", "D'", "L'", 'F2', 'R2', 'F', 'D', "R'", 'B2', "L'", 'D2', 'L', 'D', "L'", "D'", 'L', 'R', 'D', "R'", "D'", 'R', 'D', "R'", "D'", "R'", 'D', 'R', 'D', "R'", "D'", 'R', 'D', "D'", "L'", 'D', 'L', 'D', 'B', "D'", "B'", 'D', 'R', "D'", "R'", "D'", "B'", 'D', 'B', 'F', "D'", "F'", 'R', "F'", "R'", 'F', "D'", 'F', "D'", "F'", 'R', "F'", "R'", 'F', "D'", 'D', 'D', 'D', 'B', 'D', 'R', "D'", "R'", "B'"]
# randm =  ['U', "D'", 'B', 'U', "L'", 'F2', "D'", 'L', "B'", 'D2', 'D2', 'U', "R'", 'B2', 'R2', "F'", 'B', 'R', "D'", "F'", 'R', "L'", 'L', 'D', "L'"]
# randm with 1 yellow center = ["B'", 'U', 'D2', 'L2', "D'", "F'", 'F2', "F'", 'F2', 'L2', 'D2', 'R', 'U', "R'", "R'", 'R', 'F2', "L'", "D'", 'B', 'R2', "B'", "D'", 'B', 'D', "B'", "D'", 'B', 'D', "L'", 'D', 'L', 'D', "L'", 'D', 'L', 'D', "L'", 'D', 'L', 'D', "R'", 'D2', 'R', 'D', "R'", "D'", 'R', "L'", 'D', 'L', 'D', "F'", 'D2', 'F', 'D', "F'", "D'", 'F', "L'", 'D', 'L', 'D', 'B', 'D', "B'", "D'", 'B', 'D', "B'", "D'", 'D', 'D', 'D', "D'", "L'", 'D', 'L', 'D', 'B', "D'", "B'", 'D', 'R', "D'", "R'", "D'", "B'", 'D', 'B', "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", "D'", "F'", 'D', 'F', 'D', 'L', "D'", "L'", 'D', 'D', "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", 'D']
# print(randm)
kek.make_move(randm)
# kek.moves(["D'", 'U', 'B', 'D2', 'D2', "D'", "L'", "R'", "L'", 'L2', "D'", 'L', "B'", "U'", 'F2', 'L', 'F', "D'", "L'", 'F', 'B2'])
# print(kek)
# exit()

solv = Solver(kek)
# print(kek)
print(gre(solv.rubik_state))
# if d2 and d2 - del all in history


