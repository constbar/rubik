# if shuffled state starts - dont write the turns to somewhere

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

RUru = { # maybe name it in full
    'corner_permutation': [7, 1, 2, 6, 4, 5, 3, 0],
    'edge_permutation': [0, 1, 2, 6, 4, 5, 11, 7, 8, 9, 10, 3],
    'corner_orientation': [2, 0, 0, 2, 0, 0, 0, 2],
    'edge_orientation': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
}



stages = ['stage_1', 'stage_2']
shuf = State(test)
shuf.moves('U')

# solver:
# if last turn was in the same coordinate axis ?
# if last was repeated with this turn -> continue
# print(st)

start_time = timeit.default_timer()
properties_shuffled_state = shuf.properties

root_state = State(properties_shuffled_state)  # begin state
solution_state = None
if root_state.is_goal_stage(stages[0]) is True:

    # need to break here

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