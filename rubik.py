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
    parser.add_argument('moves', type=str, help='notations for shuffling')  # re notations
    parser.add_argument('-s', '--shuffle', required=False,
                        type=int, help='set number of shuffles')
    parser.add_argument('-v', '--verbose', action='store_true',
                        required=False, help='show solution details')
    parser.add_argument('-vis', '--visualize', action='store_true',
                        required=False, help='visualize кubik\'s solution')
    args = parser.parse_args()

    print('args.moves =', args.moves)
    print('args.shuffle =', args.shuffle)
    print('args.verbose =', args.verbose)
    print('args.visualize =', args.visualize)

    # if random -> cant be moves

    notations = args.moves.split()
    if not all(nt in RubikState.possible_notations for nt in set(notations)):
        sys.exit(f"possible notations: {' '.join([i for i in RubikState.possible_notations])}")

    if args.shuffle: # ant chech < 0 or == 0 # try with 0
        random_notations = RubikState.make_random_notations(args.shuffle)

    print(random_notations) # check if all notations get in random state
    exit()

    shuffled_rubik = RubikState(None, None, notations, None)
    shuffled_rubik.notation_path = list()
    solved_rubik = RubikSolver(shuffled_rubik)# .get sol_solution

    from termcolor import colored
    gre = lambda i: colored(i, 'green')
    yll = lambda i: colored(i, 'yellow')
    print(yll(shuffled_rubik))
    print(gre(solved_rubik))

    '''
    test = tests.clear_state
    # test = tests.test6

    kek = RubikState(test['cepo'], test['faces'], None, None)
    randm = make_random_state()
    # randm = ['U2', "U'", "R'", 'U2', "B'", 'F', 'U', 'L2', 'D2', 'F', 'B', 'L2', "B'", "F'", 'R', "L'", 'L', 'F', 'L', 'U2', "L'", "L'", 'B', "D'", 'D', 'F2', "R'", 'B2', 'U', 'B', 'D2', 'D', "F'", 'L', 'U', 'R', 'D2', 'U2', 'U2', "F'"]
    # randm = ['D2', 'F', "R'", "L'", "L'", 'F', "D'", 'L2', 'L2', 'U', 'U2', 'L', 'F2', "D'", 'D2', "D'", 'D', 'U', "L'", 'F', 'D', "D'", 'F', "D'", 'D', "F'", 'D', 'B2', 'D2', 'F2', "F'", "L'", 'U2', 'D', 'F2', 'U', 'F2', 'R', "D'", 'D']
    # randm = ["L'", "R'", 'R', 'F', 'L', 'D', 'F', "F'", "R'", 'R', 'D', 'D', 'D2', "F'", "D'", 'R2', 'U2', 'B', "B'", "U'", 'B2', 'R', 'R2', 'F', 'B', "L'", 'D', "R'", "L'", 'B2', "B'", 'R', 'R2', 'L2', "L'", 'F2', "F'", "U'", 'B2', "B'"]
    # randm = ['R', 'U', 'R', "B'", 'D', "U'", 'R', 'D', "F'", 'B', "U'", 'F2', 'F', "D'", "U'", "B'", 'D2', "L'", 'B2', 'R2', 'R2', 'D', 'F', 'F2', "B'", 'U', "L'", 'U', 'U', 'F', 'B2', 'L', 'R2', 'D', "D'", "D'", "U'", "B'", "D'", 'D2']
    # randm = ['F', "L'", 'L2', 'B', "D'", 'U', "U'", "D'", 'D2', "F'", "R'", 'U2', "L'", 'L2', 'D2', "U'", 'R', 'B2', 'R', "B'", 'F', "R'", 'F', 'R', 'U', "B'", 'U2', "B'", 'R2', "F'", "U'", "R'", 'D2', "B'", "R'", "U'", 'B', "B'", "L'", "B'"]
    # randm = ['F', "B'", "B'", 'F2', "D'", 'U2', 'F2', 'F', "F'", 'B', 'U', 'B', 'L', "B'", 'U2', 'D', 'U2', "F'", 'F', 'U', "L'", 'B', 'R', 'L', "F'", 'B2', 'R', 'D', "L'", 'B2', 'L2', 'R', "U'", "B'", "B'", "B'", 'F2', 'U', 'F', 'U2']
    # randm = ['F', 'B', "U'", "B'", 'F2', "U'", 'F', 'D2', "D'", 'U', "U'", 'B', 'B', "F'", 'L', 'U', 'B2', "U'", "U'", 'D', 'L', "L'", 'U', 'U2', 'R', 'B2', 'U2', 'L', 'D', "D'", 'F2', 'B', 'L', 'D', "F'", 'U2', "F'", "D'", 'F2', 'R']
    # randm = ['L', 'R', "B'", "F'", 'R2', "D'", 'D', 'F', 'D2', "B'", 'U', 'B2', "B'", 'B2', 'L', "F'", 'L2', 'D', 'R', "F'", "F'", "D'", 'F', 'D']
    # randm = ["U'", 'F2', 'D', 'L', "D'", 'D2', "B'", "R'", "D'", "B'", "L'", 'U', 'L2', "B'", 'B', "R'", "D'", 'F', 'R', 'F', "L'"]
    # randm = ["U'", 'D', 'D', 'R2', "U'", "U'", 'D', "D'", 'B2', "L'", 'U', 'D', "B'", 'R', 'F2', 'U2', 'L2', 'D2', 'B2', 'F']
    # randm = ['R2', "R'", 'D2', 'R2', 'D2', 'F', 'R2', "U'", 'L', 'F2', 'U', "L'", 'R', 'R', "D'", 'L2', "F'", 'R', 'D', 'R2', 'B2', 'B', 'D', "B'", "D'", 'B', 'D', "B'", "D'", "B'", 'D', 'B', 'D', 'R', 'D', "R'", "D'", 'R', 'D', "R'", "D'", "R'", 'D2', 'R', 'D', "R'", "D'", 'R', 'D', 'B', "D'", "B'", 'L', "B'", "L'", 'B', "D'", 'B', "D'", "B'", 'L', "B'", "L'", 'B', "D'", "D'", "B'", 'D', 'B', 'D', 'R', "D'", "R'", 'D', 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", 'D', 'B', 'D', 'R', "D'", "R'", "B'"]
    # randm = ['R2', 'D', "F'", 'U', 'F2', 'U2', 'U', 'L', "U'", 'D2', 'U2', 'B2', "B'", "D'", "L'", 'F2', 'R2', 'F', 'D', "R'", 'B2', "L'", 'D2', 'L', 'D', "L'", "D'", 'L', 'R', 'D', "R'", "D'", 'R', 'D', "R'", "D'", "R'", 'D', 'R', 'D', "R'", "D'", 'R', 'D', "D'", "L'", 'D', 'L', 'D', 'B', "D'", "B'", 'D', 'R', "D'", "R'", "D'", "B'", 'D', 'B', 'F', "D'", "F'", 'R', "F'", "R'", 'F', "D'", 'F', "D'", "F'", 'R', "F'", "R'", 'F', "D'", 'D', 'D', 'D', 'B', 'D', 'R', "D'", "R'", "B'"]
    # randm = ['U', "D'", 'B', 'U', "L'", 'F2', "D'", 'L', "B'", 'D2', 'D2', 'U', "R'", 'B2', 'R2', "F'", 'B', 'R', "D'", "F'", 'R', "L'", 'L', 'D', "L'"]
    # randm = ["B'", 'U', 'D2', 'L2', "D'", "F'", 'F2', "F'", 'F2', 'L2', 'D2', 'R', 'U', "R'", "R'", 'R', 'F2', "L'", "D'", 'B', 'R2', "B'", "D'", 'B', 'D', "B'", "D'", 'B', 'D', "L'", 'D', 'L', 'D', "L'", 'D', 'L', 'D', "L'", 'D', 'L', 'D', "R'", 'D2', 'R', 'D', "R'", "D'", 'R', "L'", 'D', 'L', 'D', "F'", 'D2', 'F', 'D', "F'", "D'", 'F', "L'", 'D', 'L', 'D', 'B', 'D', "B'", "D'", 'B', 'D', "B'", "D'", 'D', 'D', 'D', "D'", "L'", 'D', 'L', 'D', 'B', "D'", "B'", 'D', 'R', "D'", "R'", "D'", "B'", 'D', 'B', "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", 'R', "D'", "R'", 'B', "R'", "B'", 'R', "D'", "D'", "F'", 'D', 'F', 'D', 'L', "D'", "L'", 'D', 'D', "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", "D'", "R'", 'D', 'R', 'D', 'F', "D'", "F'", 'D']
    print(randm)
    kek.make_move(randm)
    # kek.moves(["D'", 'U', 'B', 'D2', 'D2', "D'", "L'", "R'", "L'", 'L2', "D'", 'L', "B'", "U'", 'F2', 'L', 'F', "D'", "L'", 'F', 'B2'])
    # print(kek)
    # exit()

    solv = Solver(kek)
    # print(kek)
    print(gre(solv.rubik_state))
    # if d2 and d2 - del all in history
    '''