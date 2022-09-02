#!/usr/bin/python3
import sys
import argparse

# make flag verbose for timing / visual and smth

# $>./rubik "F R U2 B' L' D'" | cat -e
# $> ./rubik "F R U2 B' L' D'" | wc -w
#

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
                          required=False, help='show solution details')
    optional.add_argument('-vis', '--visualize', action='store_true',
                          required=False, help='visualize rubik\'s solution')
    args = parser.parse_args()

    print('args.moves =', args.notations)  # to del all block
    print('args.shuffle =', args.shuffle)
    print('args.verbose =', args.verbose)
    print('args.visualize =', args.visualize)

    if args.shuffle and args.shuffle < 1:
        parser.error('need to specify the number of times to shuffle')

    if args.notations:
        notations = args.notations.split()
        if not all(nt in RubikState.possible_notations for nt in set(notations)):
            parser.error(f"possible notations: {' '.join([i for i in RubikState.possible_notations])}")
    else:
        notations = RubikState.make_random_notations(args.shuffle)

    shuffled_rubik = RubikState(None, None, notations, None)
    shuffled_rubik.notation_path = list()
    solved_rubik = RubikSolver(shuffled_rubik).rubik_state

    if args.visualize:
        print('make visualization and exit')

    print('all turns')

    if args.verbose:
        print('time - maybe steps')

    from termcolor import colored
    gre = lambda i: colored(i, 'green')
    yll = lambda i: colored(i, 'yellow')
    print(yll(shuffled_rubik))
    print(gre(solved_rubik))
