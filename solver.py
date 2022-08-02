# if shuffled state starts - dont write the turns to somewhere
# solver:
# if last turn was in the same coordinate axis ?
# if last was repeated with this turn -> continue
# print(st)
# add timer
# make in rubik moves in good order like subgroup state

import os
import re
import time
import copy
import logging
import timeit
from rubik import State
from termcolor import colored
from queue import PriorityQueue
from typing import Optional, Dict, Any
import queue

logging.basicConfig(level=logging.INFO, filename='log.log',
                    filemode='w', format='%(message)s')
log = lambda i: logging.info(i)

gre = lambda i: colored(i, 'green')
yll = lambda i: colored(i, 'yellow')

test = {  # maybe name it in full
    'corner_permutation': list(range(8)),
    'edge_permutation': list(range(12)),
    'corner_orientation': [0] * 8,
    'edge_orientation': [0] * 12
}

U = {  # maybe name it in full
    'corner_permutation': [4, 1, 2, 7, 3, 5, 6, 0],
    'edge_permutation': [8, 1, 2, 11, 4, 5, 6, 7, 3, 9, 10, 0],
    'corner_orientation': [1, 0, 0, 1, 2, 0, 0, 2],
    'edge_orientation': [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1]
}

qwerty = {  # 'U','R2','U','R','U','B2','R','B\'','R','U','L','D','L','D2'
    'corner_permutation': [4, 6, 0, 7, 5, 2, 1, 3],
    'edge_permutation': [1, 9, 7, 0, 8, 3, 4, 11, 6, 10, 5, 2],
    'corner_orientation': [1, 2, 2, 0, 0, 2, 1, 1],
    'edge_orientation': [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1]
}

RUru = { # maybe name it in full
    'corner_permutation': [7, 1, 2, 6, 4, 5, 3, 0],
    'edge_permutation': [0, 1, 2, 6, 4, 5, 11, 7, 8, 9, 10, 3],
    'corner_orientation': [2, 0, 0, 2, 0, 0, 0, 2],
    'edge_orientation': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
}

stages = ['stage_0', 'stage_1']  # rename to stage 0

# g0 = {'R', 'B', 'D'}
# g0 = {'R', 'B', 'D', 'U', 'L'}
# g0 = {'L', 'R', 'F', 'B', 'U', 'D'}
# g0 = ['L', 'R', 'F', 'B', 'U', 'D']  # anke more notations
g0 = ['L', 'R', 'F', 'B', 'U', 'D']  # anke more notations
# g0 = ['L', 'R', 'F', 'B', 'U', 'D', 'L\'', 'R\'', 'F\'', 'B\'', 'U\'', 'D\'']  # anke more notations

config_dict = {
    '3x3x3': {
        # goal state ??
        # 'subgroup_0_moves': ['U', 'D', 'L', 'R', 'F', 'B'],
        'subgroup_0_moves': ['L', 'R', 'F', 'B', 'U', 'D'],
    }
}


class Solver:
    def __init__(self, shuffled_node):  # it is the biging state
        self.start_node = shuffled_node # this node will be over init for each stage
        self.open_list = PriorityQueue()
        self.solution_path = list()

        # for stage in ['stage_0', 'stage_1', 'stage_2', 'stage_3']:
        # for stage in ['stage_1']:
        for stage in ['stage_0']:
            pass
        self.start_solve() # start solves group
        # обновить старт ноду для исполнения
        print('end')
        print(self.solution_path)

    def start_solve(self):
        threshold = self.start_node.f_cost()
        solved = False  # solved state
        ii = 0
        while solved is False:
            print(ii)
            self.open_list.put(self.start_node)
            thresholds = list()

            print('threshold for children', threshold)
            while self.open_list.qsize():
                lowest_node = self.open_list.get()

                if lowest_node.is_goal_stage('stage_0'):
                    print(gre('BiNGO! the answer is here'))
                    print(gre(lowest_node.notation))
                    print(gre(lowest_node.notation_history))
                    print()
                    for k, v in lowest_node.properties.items():
                        print(k, v)
                    self.solution_path += lowest_node.notation_history
                    solved = True
                    break

                for notation in g0:
                    new_state = State(lowest_node.properties, notation, # rename move history
                                      copy.deepcopy(lowest_node.notation_history))
                    # print(f'node cost {new_state.f_cost()}, '
                    #       f'{new_state.notation}, {new_state.notation_history}')
                    if new_state.f_cost() <= threshold:
                        self.open_list.put(new_state)
                    else:
                        thresholds.append(new_state.f_cost())
            if solved:
                break
            print()
            log(f"thresholds {thresholds}")
            # log(f'end while | size que {self.open_list.qsize()}')
            threshold = min(thresholds)
            log(f"threshold after all : {threshold}")
            log('')
            # if ii > 7:
            #     exit()

            ii += 1
        print('NUM ITERS IS', ii)


shuf = State(qwerty, None, None)
# shuf = State(test, None, None)
# print(shuf.h_cost())

solv = Solver(shuf)
