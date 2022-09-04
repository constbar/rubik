#!/usr/bin/python3
import sys
import argparse
from rubik_ursina import RubikVisualizer

# $>./rubik "F R U2 B' L' D'" | cat -e
# $> ./rubik "F R U2 B' L' D'" | wc -w


from termcolor import colored
gre = lambda i: colored(i, 'green')   # del this block
yll = lambda i: colored(i, 'yellow')

from rubik_state import RubikState
from rubik_solver import RubikSolver
# split by tabs spaces and other

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
    """
    print('args.moves =', args.notations)  # to del all block
    print('args.shuffle =', args.shuffle)
    print('args.verbose =', args.verbose)
    print('args.visualize =', args.visualize)
    """
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

    print_solution = lambda: colored(' '.join([i for i in solved_rubik_state.notation_path]), 'green')
    if args.visualize:
        rubik_visualizer = RubikVisualizer(shuffled_notations, solved_rubik_state.notation_path)
        rubik_visualizer.run()
        sys.exit()

    elif args.shuffle:
        print('notations for cube shuffling:', colored(' '.join([i for i in shuffled_notations]), 'yellow'))
        print('notations for solving the cube:', print_solution())
    else:
        print(gre(solved_rubik_state.notation_path)) # del !
        print(print_solution())

    if args.verbose:
        print('number of moves to solve:', colored(str(len(solved_rubik_state.notation_path)), 'green'), 'moves')
        print('rubik\'s solution time:', colored(round(solver.solution_time, 3), 'green'), 'secs')
