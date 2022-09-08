#!/usr/bin/python3
import argparse
import subprocess

from termcolor import colored

from rubik_solver import RubikSolver
from rubik_state import RubikState

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
        parser.error('need to specify the correct number of times to shuffle')
    elif not args.notations and not args.shuffle or args.notations and args.notations.isspace():
        parser.error('input cannot be empty')

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

    green_solution = colored(' '.join([i for i in solved_rubik_state.notation_path]), 'green')
    if args.visualize:
        subprocess.run(['python3', 'rubik_ursina.py',
                        ' '.join(shuffled_notations), ' '.join(solved_rubik_state.notation_path)])
    elif args.shuffle:
        print('notations for cube shuffling:', colored(' '.join([i for i in shuffled_notations]), 'yellow'))
        print('notations for solving the cube:', green_solution)
    else:
        print(green_solution)

    if args.verbose:
        print('number of moves to solve:', colored(str(len(solved_rubik_state.notation_path)), 'green'), 'moves')
        print('rubik\'s solution time:', colored(str(round(solver.solution_time, 3)), 'green'), 'secs')
