import numpy as np

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
test3 = { # 'U','R2','U','R','U','B2','R','B\'','R','U','L','D','L','D2'
    'cepo': {
        'corner_permutation': [4, 6, 0, 7, 5, 2, 1, 3],
        'edge_permutation': [1, 9, 7, 0, 8, 3, 4, 11, 6, 10, 5, 2],
        'corner_orientation': [1, 2, 2, 0, 0, 2, 1, 1],
        'edge_orientation': [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1]
    },
    'faces': 'ryrywggrbggowgwyryybobroryrwwbgboybowbwworwgobogyyobrg'
}

