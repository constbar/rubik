# if shuffled state starts - dont write the turns to somewhere
# solver:
# if last turn was in the same coordinate axis ?
# if last was repeated with this turn -> continue
# print(st)
# add timer
# make in rubik moves in good order like subgroup state
# try solved orientaion to solve

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

target = {  # maybe name it in full
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

stages = ['stage_0']#, 'stage_1']#, 'stage_2']  # rename to stage 0
# stages = ['stage_0', 'stage_1']#, 'stage_2']  # rename to stage 0

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

# n = {
#     'corner_permutation': [7, 6, 4, 1, 3, 2, 0, 5],
#     'edge_permutation': [3, 5, 2, 6, 0, 9, 10, 11, 4, 7, 8, 1],
#     'corner_orientation': [0, 0, 1, 1, 0, 1, 0, 0],
#     'edge_orientation': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# }
# kek = State(n, None, None, 'stage_0')
# kek.moves('L')
# print(kek)

# print(int('011000000110', 2))

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


shuf = State(qwerty, None, None, None)
# shuf = State(RUru, None, None, None)
# shuf = State(test, None, None)
# print(shuf.h_cost())

solv = Solver(shuf)




"""
exit()
import queue


table0 = [0] * 2048
# print(table0)
ini = State(target, None, None, None)
parents = queue.Queue()
parents.put(ini)
# print(parents.qsize())
# depth = 6
# print('\nstart')
# for depth in range(1, 6):
#     print('depth', depth)
#
#     new_node = parents.get()
#     for notation in g0:
#         new_state = State(new_node.properties, None, notation,
#                           copy.deepcopy(new_node.notation_history))
#         parents.put(new_state)
#         # print(new_state)
#         # print(new_state.eo)
#         prep_str = ''.join(map(str, new_state.eo[:-1]))
#         # print('prep_str =', prep_str)
#         str_eo = int(prep_str, 2)
#         # print(str_eo)
#         if str_eo != 0:
#             print(str_eo)
#         if not table0[str_eo]:
#             table0[str_eo] = depth
#         # print(type(new_state.eo))
# print(table0)
for depth in range(1, 171):
    parent = parents.get()
    for move in g0:
        child = State(
            copy.deepcopy(parent.properties),
            None, move, None  #parent.notation_history
        )
        index = int(''.join(map(str, child.eo[:-1])), 2)
        # print(index)
        if index != 0 and table0[index] == 0:
            table0[index] = depth
        parents.put(child)
    # print('size', parents.qsize())
    # parents = children
# }
# for i, depth := range table {
#     if i > 0 && depth == 0 {
#         table[i] = 7
#     }
# }
# print(table0)
# print(table0.count(1))
# print(set(table0))
func tableG0() [2048]uint8 {
    fmt.Printf("\nGenerating pruning table for G0")
    var table [2048]uint8
    var parents []cepo
    parents = append(parents, *initCube())
    var depth uint8
    for depth < 6 {
        var children []cepo
        depth++
        for _, parent := range parents {
            for _, move := range listMoves(&parent, 0) {
                child := newNode(&parent, move)
                spin(move, child)
                index := binaryToDecimal(child.eO)
                if index != 0 && table[index] == 0 {
                    table[index] = depth
                }
                children = append(children, *child)
            }
        }
        parents = children
        fmt.Printf(".")
    }
    for i, depth := range table {
        if i > 0 && depth == 0 {
            table[i] = 7
        }
    }
    return table
}
"""

