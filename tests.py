import numpy as np
make_commmas = lambda i: list(map(int, i.split()))

clear_state = {
    'cepo': { # name cepo better
        'corner_permutation': list(range(8)),
        'edge_permutation': list(range(12)),
        'corner_orientation': [0] * 8,
        'edge_orientation': [0] * 12
    },
    'faces': 'wwwwwwwwwgggggggggrrrrrrrrrbbbbbbbbboooooooooyyyyyyyyy'
}

test1 = {
    'cepo': {  # U
        'corner_permutation': [4, 1, 2, 7, 3, 5, 6, 0],
        'edge_permutation': [8, 1, 2, 11, 4, 5, 6, 7, 3, 9, 10, 0],
        'corner_orientation': [1, 0, 0, 1, 2, 0, 0, 2],
        'edge_orientation': [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1]
    },
    'faces': 'wwwwwwwwwrrrggggggbbbrrrrrrooobbbbbbgggooooooyyyyyyyyy'
}

test2 = {  # RUru
    'cepo': {
        'corner_permutation': [7, 1, 2, 6, 4, 5, 3, 0],
        'edge_permutation': [0, 1, 2, 6, 4, 5, 11, 7, 8, 9, 10, 3],
        'corner_orientation': [2, 0, 0, 2, 0, 0, 0, 2],
        'edge_orientation': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    },
    'faces': 'wwgwwrwwroggggggggrryrrwrrrbbwobbwbbobbooooooyybyyyyyy'
}
test3 = {  # 'U','R2','U','R','U','B2','R','B\'','R','U','L','D','L','D2'
    'cepo': {
        'corner_permutation': [4, 6, 0, 7, 5, 2, 1, 3],
        'edge_permutation': [1, 9, 7, 0, 8, 3, 4, 11, 6, 10, 5, 2],
        'corner_orientation': [1, 2, 2, 0, 0, 2, 1, 1],
        'edge_orientation': [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1]
    },
    'faces': 'ryrywggrbggowgwyryybobroryrwwbgboybowbwworwgobogyyobrg'
}

# random start
test4 = {  # "F' D R F2 U' L2 R B D B2 F U L2 B2 F D2 U' R2 U' L' B2 F U2 F2 D' L2 R' B2 D' F'"
    'cepo': {
        'corner_permutation': make_commmas('2 4 3 7 0 6 5 1'),
        'edge_permutation': make_commmas('0 2 6 3 4 11 10 1 7 8 5 9'),
        'corner_orientation': make_commmas('2 0 1 1 1 0 1 0'),
        'edge_orientation': make_commmas('0 0 0 0 1 1 0 0 1 0 1 0')
    },
    'faces': 'byrwwwgboogwogwybwooworyrwobbgobggbryryyogwgbgryyyrrrb'
}

test5 = {  # "U' F' D L' R' D' R F' L R' B2 L' R F L2 F2 U' L D U F' L' B2 D2 L2 F U' B L' D'"
    'cepo': {
        'corner_permutation': make_commmas('4 2 0 6 1 3 7 5'),
        'edge_permutation': make_commmas('10 2 3 7 1 9 11 4 6 0 8 5'),
        'corner_orientation': make_commmas('1 2 1 1 1 0 2 1'),
        'edge_orientation': make_commmas('0 0 0 1 0 1 0 1 1 1 0 1')
    },
    'faces': 'gryowbgbywyyggrrborrbyrwywbrogobgwwoogrooywwbbgoyybwrg'
}

test6 = {  # "B U2 B2 F D' L2 D' F' U B2 F D F R B U L D U L F' D' R2 D2 L F2 L U2 F' R' D2 R' D B2 F D2 R B' F2 L' R' B' R' D R2 B2 R' U F2 D2 R' D2 U L2 D2 F' D U2 R2 D B2 U' B' R' F' U F' L2 D' U' R2 F D U' B2 R2 D' F2 D U' B U L D' R D2 U2 F U F' D' U F R B' F R' F2 R2 B'"
    'cepo': {
        'corner_permutation': make_commmas('7 4 6 0 5 3 1 2'),
        'edge_permutation': make_commmas('5 7 9 8 4 6 2 10 0 11 1 3'),
        'corner_orientation': make_commmas('2 1 0 2 1 1 1 1'),
        'edge_orientation': make_commmas('0 1 0 0 1 1 1 1 1 1 0 1')
    },
    'faces': 'bbogwwogowryogrwowgwgbryrwgwrbbbyrryywooogrgrgoybyybyb'
}

test7 = {  # "R B2 F2 U' L2 R U2 R' B F R B' D2 U' L2 R D' R D U' L2 B' F2 D' R D R2 D U2 F' L' F' D L2 U F' L D U2 L B F' D B F D' U' B2 F2 D B F2 R2 U2 L' F2 D2 U2 R B2 F' D' L D B' F' D' R2 U R2 U L' D2 B2 L2 F' U2 B F' L' F U2 B U2 F' U2 B D2 L R2 B2 F L2 B D F2 R2 U2 L U R' D U R B L' R' D U2 B2 L2 R U' B' D2 U' R2 U' B F"
    'cepo': {
        'corner_permutation': make_commmas('2 0 7 4 1 6 5 3'),
        'edge_permutation': make_commmas('5 4 11 1 10 6 3 9 0 8 7 2'),
        'corner_orientation': make_commmas('2 1 2 1 0 2 2 2'),
        'edge_orientation': make_commmas('1 0 1 0 0 0 1 0 0 1 0 0')
    },
    'faces': 'oywrwyywrygrygrrgwggwbrwgryggrbbrowobbbyooboyowgoyobbw'
}

test8 = {  # "L F' D U2 B D2 L B2 R2 D"
    'cepo': {
        'corner_permutation': make_commmas('1 4 2 0 3 5 7 6'),
        'edge_permutation': make_commmas('6 7 1 10 2 3 0 9 11 8 4 5'),
        'corner_orientation': make_commmas('2 2 1 0 2 1 0 1'),
        'edge_orientation': make_commmas('1 1 1 0 1 1 0 1 1 0 1 0')
    },
    'faces': 'rryrwyrwoybbygbyorwogwrggwbwobwbywyorggrobyggwrobygoob'
}

test9 = {  # "B' F R B U' L2 D' U L' U L2 R D U2 B F' U B F D'"
    'cepo': {
        'corner_permutation': make_commmas('5 4 0 7 6 3 2 1'),
        'edge_permutation': make_commmas('10 5 8 1 2 0 9 6 4 11 3 7'),
        'corner_orientation': make_commmas('0 1 2 0 0 2 1 0'),
        'edge_orientation': make_commmas('0 1 1 0 1 1 1 1 0 1 0 1')
    },
    'faces': 'yoyowgroooyyyggbrgbgwwrywwobyrrbrywggbgbobowwrobgyrrbw'
}

test10 = {  # "B R' F D L2 R' U2 L' B' F' U L F2 D2 L' F' L2 R2 D2 L2 D2 U' B U F' L2 U B D L'"
    'cepo': {
        'corner_permutation': make_commmas('3 6 1 2 0 5 7 4'),
        'edge_permutation': make_commmas('7 1 0 11 5 10 8 6 3 2 9 4'),
        'corner_orientation': make_commmas('2 2 0 0 2 0 2 1'),
        'edge_orientation': make_commmas('1 0 0 1 0 1 1 1 0 1 0 0')
    },
    'faces': 'wggbwogwybowrgyggroboorrbybbwrwbrwwyworboggyoyboyygyrr'
}

# checklist test

test11 = {  # "U R2 F B R B2 R U2 L B2 R U' D' R2 F R' L B2 U2 F2"
    'cepo': {
        'corner_permutation': make_commmas('0 1 2 3 4 5 6 7'),
        'edge_permutation': make_commmas('0 1 2 3 4 5 6 7 8 9 10 11'),
        'corner_orientation': make_commmas('0 0 0 0 0 0 0 0'),
        'edge_orientation': make_commmas('1 1 1 1 1 1 1 1 1 1 1 1')
    },
    'faces': 'wowgwbwrwgwgogrgygrwrgrbryrbwbrbobybowobogoyoyrygybyoy'
}