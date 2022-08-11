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

logging.basicConfig(level=logging.INFO, filename='log.log',
                    filemode='w', format='%(message)s')
log = lambda i: logging.info(i)

gre = lambda i: colored(i, 'green')
yll = lambda i: colored(i, 'yellow')

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
        self.state_node = shuffled_node  # this node will be over init for each stage
        self.open_list = PriorityQueue()  # add it in first step
        self.solution_path = list()

        for stage in range(len(stages)):  # num stage
            self.solve_cross(stage)  # start solves group # white cross
            # print('SIZe OF QUE', self.open_list.qsize())
            self.open_list = PriorityQueue() # need to delete open list
            # print('SIZe OF QUE', self.open_list.qsize())
        print('end of cross stage')
        print('fin white cross stage\n\n')
        print(self.solution_path)
        # print(self.state_node)

        self.solve_white_edges()

        print(gre('\n\nafter white corners'))
        print(self.state_node)

    def solve_cross(self, stage):
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

    def solve_white_edges(self):
        solved_state = False  # re
        up_layer_corners = (0, 7, 3, 4)  # rename
        # while //
        # self.start_node.moves(['R', 'D2', 'D'])
        #
        for corner in up_layer_corners:  # re # i = check corner pernumtstion
            if self.state_node.cp[corner] == corner:
                print('match permutation')
                if self.state_node.co[corner] == 0:
                    print('full match')
                    continue
                else:
                    if corner == 0:
                        if self.state_node.co[corner] == 1:
                            self.state_node.moves(['R\'', 'D\'', 'R', 'D'] * 2)  # or mult corner
                        if self.state_node.co[corner] == 2:
                            pass
                            # [F D F' D'] check it for counterclockwise move corner
                            # self.state_node.moves(['R', 'U', 'R', 'U'] * 2) wrong

                    # elif if corner == 7
                    # elif if corner == 3
                    # elif if corner == 4


            # elif self.start_node.co[i] != i:
            #     print('check_corner_orinentation')

        # print(0, self.start_node.ep[0])
        # print(7, self.start_node.ep[7])
        # print(3, self.start_node.ep[3])
        # print(4, self.start_node.ep[4])

# test = tests.clear_state
test = tests.test4
kek = State(test['cepo'], test['faces'], None, None, None)
# print(kek.make_line_state())

# mv = "R U R' U' R U R' U'"
# for m in mv.split():
#     kek.moves(m)
print(kek)


solv = Solver(kek)
# print('kek.faces')


