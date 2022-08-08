# if shuffled state starts - dont write the turns to somewhere
# solver:

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



stages = ['stage_0']#, 'stage_1']#, 'stage_2']  # rename to stage 0

# g0 = {'R', 'B', 'D'}
# g0 = {'R', 'B', 'D', 'U', 'L'}
# g0 = {'L', 'R', 'F', 'B', 'U', 'D'}
# g0 = ['L', 'R', 'F', 'B', 'U', 'D']  # anke more notations
# g0 = ['L', 'R', 'F', 'B', 'U', 'D']  # anke more notations
# g0 = ['L', 'R', 'F', 'B', 'U', 'D', 'L\'', 'R\'', 'F\'', 'B\'', 'U\'', 'D\'']  # anke more notations
# g0 =["U", "U'", "U2", "D", "D'", "D2", "R", "R'", "R2", "L", "L'", "L2", "F", "F'", "F2", "B", "B'", "B2"]

config_dict = {
    '3x3x3': {
        # goal state ??
        # 'subgroup_0_moves': ['U', 'D', 'L', 'R', 'F', 'B'],
        # 'subgroup_0_moves': ['L', 'R', 'F', 'B', 'U', 'D'],
        # 'stage_0_moves': ['L', 'R', 'F', 'B', 'U', 'D'],
        'stage_0_moves': ["U", "U'", "U2", "D", "D'", "D2", "R", "R'", "R2", "L", "L'", "L2", "F", "F'", "F2", "B", "B'", "B2"],
        'stage_1_moves': ['L', 'R', 'F', 'B', 'U2', 'D2'],
        'stage_2_moves': ['L', 'R', 'F', 'B', 'U2', 'D2'],
    }
}

class Solver:
    def __init__(self, shuffled_node):  # it is the biging state
        self.start_node = shuffled_node  # this node will be over init for each stage
        self.open_list = PriorityQueue()
        self.solution_path = list()

        # for stage in ['stage_0', 'stage_1', 'stage_2', 'stage_3']:
        # for stage in ['stage_1']:
        # for stage in ['stage_0', 'stage_1']:
        for stage in range(len(stages)):  # num stage
            self.start_solve(stage)  # start solves group
            # print('SIZe OF QUE', self.open_list.qsize())
            self.open_list = PriorityQueue()
            # print('SIZe OF QUE', self.open_list.qsize())
            # exit()

        # обновить старт ноду для исполнения
        print('end')
        print(self.solution_path)

    def start_solve(self, stage):
        threshold = self.start_node.f_cost()
        self.open_list = PriorityQueue()  # need i?
        solved = False  # solved state
        ii = 0
        while solved is False:
            print(ii)
            self.open_list.put(self.start_node)
            thresholds = list()

            print('threshold for children', threshold)
            while self.open_list.qsize():
                lowest_node = self.open_list.get()

                if lowest_node.is_goal_stage():
                    print(gre('BiNGO! the answer is here'))
                    print(gre(lowest_node))
                    print(gre(lowest_node.notation))
                    print(gre(lowest_node.notation_history))
                    print()
                    # for k, v in lowest_node.properties.items():
                    #     print(k, v)
                    self.solution_path += lowest_node.notation_history
                    solved = True
                    # print('id of lowest', id(lowest_node))
                    self.start_node = State(
                        # copy.deepcopy(lowest_node.properties), f'stage_{stage + 1}', None, None
                        lowest_node.properties, f'stage_{stage + 1}', None, None
                    )
                    break

                # for notation in g0:
                for notation in config_dict['3x3x3'][f'stage_{stage}_moves']:
                    # print(stage)
                    # print(config_dict['3x3x3'][f'{stage}_moves'])
                    new_state = State(lowest_node.properties, stages[stage], notation,  # rename move history
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
            # if ii > 7:
            #     exit()
            ii += 1
            # if stage == 'stage_1':
            #     exit()
        print('NUM ITERS IS', ii)


kek = State(tests.clear_state['cepo'],
            'w' * 9 + 'o' * 9 + 'g' * 9
            + 'r' * 9 + 'b' * 9 + 'y' * 9,
            None, None, None)

print(kek.top)

# shuf = State(qwerty, None, None, None)
# shuf = State(RUru, None, None, None)
# shuf = State(test, None, None)
# print(shuf.h_cost())

# solv = Solver(shuf)
# solv = Solver(kek)
# print('kek.faces')
