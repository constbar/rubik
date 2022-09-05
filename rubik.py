#!/usr/bin/python3
import argparse

from termcolor import colored

from rubik_ursina import RubikVisualizer


from rubik_state import RubikState
from rubik_solver import RubikSolver

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='solving a rubik\'s cube according to '
                    'the provided notations for shuffling')
    required = parser.add_mutually_exclusive_group()
    required.add_argument('notations', nargs='?', type=str,
                          help='notations for shuffling')
    required.add_argument('-s', '--shuffle', required=False,
                          type=int, help='set number of shuffles')
    optional = parser.add_mutually_exclusive_group()
    optional.add_argument('-v', '--verbose', action='store_true',
                          required=False, help='show solution time')
    optional.add_argument('-vis', '--visualize', action='store_true',
                          required=False, help='visualize rubik\'s solution')
    args = parser.parse_args()

    if args.shuffle and args.shuffle < 1:
        parser.error('need to specify the number of times to shuffle')

    if args.notations:
        shuffled_notations = args.notations.split()
        if not all(nt in RubikState.possible_notations for nt in set(shuffled_notations)):
            parser.error(f"possible notations: {' '.join([i for i in RubikState.possible_notations])}")
    else:
        shuffled_notations = RubikState.make_random_notations(args.shuffle)

    shuffled_rubik_state = RubikState(None, None, shuffled_notations, None)
    shuffled_rubik_state.notation_path = list()
    solver = RubikSolver(shuffled_rubik_state)
    solved_rubik_state = solver.rubik_state

    make_green_solution = lambda: colored(' '.join([i for i in solved_rubik_state.notation_path]), 'green')
    if args.visualize:
        rubik_visualizer = RubikVisualizer(shuffled_notations, solved_rubik_state.notation_path)
        rubik_visualizer.run()

    elif args.shuffle:
        print('notations for cube shuffling:', colored(' '.join([i for i in shuffled_notations]), 'yellow'))
        print('notations for solving the cube:', make_green_solution())
    else:
        print(make_green_solution())

    if args.verbose:
        print('number of moves to solve:', colored(str(len(solved_rubik_state.notation_path)), 'green'), 'moves')
        print('rubik\'s solution time:', colored(round(solver.solution_time, 3), 'green'), 'secs')
