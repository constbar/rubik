# if shuffled state starts - dont write the turns to somewhere
import copy

from rubik import State
import os
import re
import time
import timeit
from queue import PriorityQueue
from typing import Optional, Dict, Any
from termcolor import colored

gre = lambda i: colored(i, 'green')
yll = lambda i: colored(i, 'yellow')

test = { # maybe name it in full
    'corner_permutation': list(range(8)),
    'edge_permutation': list(range(12)),
    'corner_orientation': [0] * 8,
    'edge_orientation': [0] * 12
}

U = { # maybe name it in full
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

# g0 = {'L', 'R', 'F', 'B', 'U', 'D'}
g0 = ['L', 'R', 'F', 'B', 'U', 'D']  # anke more notations
# g0 = ['L', 'R', 'F', 'B', 'U', 'D', 'L\'', 'R\'', 'F\'', 'B\'', 'U\'', 'D\''] # anke more notations

stages = ['stage_1', 'stage_2']

# solver:
# if last turn was in the same coordinate axis ?
# if last was repeated with this turn -> continue
# print(st)
shuf = State(qwerty, None, None)
start_time = timeit.default_timer()
properties_shuffled_state = shuf.eo
solution_state = None
# print(work)
open_list = PriorityQueue()  # rename

if shuf.is_goal_stage(stages[0]) is True:
    exit()  # need to break here


open_list.put(shuf)

print()

# just = []
# just.append(work)
# for i in g0:
#     just.append(State(work.properties, i))
#
# print('len of list', len(just))
# for i in just:
#     print(i.properties['edge_orientation'])
#     print(i.cost('stage_1'))
# exit()

ii = 0
o = 0
count = 0
while not open_list.empty():
    lowest_cost_node = open_list.get()
    print('cst', lowest_cost_node.cost())
    # print('eo', lowest_cost_node.eo)
    # print()
    if lowest_cost_node.is_goal_stage('stage_1'):
        print(gre('BiNGO!'))
        print('fin cost', lowest_cost_node.cost())
        print('fin eo', lowest_cost_node.eo)
        exit()

    # print('cost() =', lowest_cost_node.cost())
    # if lowest_cost_node.is_goal_stage('stage_1'):
    #     print(123)
    #     print(lowest_cost_node.properties)
    #     break

    for nota in g0:
        get_history = copy.deepcopy(lowest_cost_node.notation_history)
        print(get_history)
        print(nota)
        print(id(get_history))
        new_state = State(lowest_cost_node.properties, nota, get_history)
        print('history', new_state.notation_history)
        # print(new_state.notation_history)
        # print(new_state.eo)
        # print('cost', new_state.cost())
        open_list.put(new_state)

        # new_state.id = o
        # o += 1
        # print('id', new_state.id)
        # print(new_state.cost())

    if ii > 100:
        break
    ii += 1
    # exit()
    print('SIZE', open_list.qsize())

# print(count)
# del open_list
exit()
print('SIZE', open_list.qsize())
while not open_list.empty():
    node = open_list.get()
    print(node.cost())

"""
def __get_solution_node(self) -> Optional[Node | None]:
    start_time = timeit.default_timer()
    solution_node = None
    root_node = Node(self.__init_state, father=None)
    if root_node.is_goal_state() is True:
        solution_node = root_node
        self.__search_time = timeit.default_timer() - start_time
        return solution_node

    self.__open_list.put(root_node)
    while not self.__open_list.empty():
        lowest_cost_node = self.__open_list.get()
        self.__selected_states += 1
        children = lowest_cost_node.make_children()
        self.__closed_list.add(lowest_cost_node.__hash__())
        sum_memory_states = self.__open_list.qsize() + len(
            self.__closed_list) + len(children)
        if self.__size_complexity < sum_memory_states:
            self.__size_complexity = sum_memory_states
        for child in children:
            if child.is_goal_state():
                solution_node = child
                break
            elif child.__hash__() not in self.__closed_list:
                self.__open_list.put(child)
        else:
            continue
        break
    self.__search_time = timeit.default_timer() - start_time
    return
"""