import numpy as np

clear_state = {
    'cepo': { # name cepo better
        'corner_permutation': list(range(8)),
        'edge_permutation': list(range(12)),
        'corner_orientation': [0] * 8,
        'edge_orientation': [0] * 12
    },
    'faces': 'w' * 9 + 'o' * 9 + 'g' * 9 + 'r' * 9 + 'b' * 9 + 'y' * 9,
    'old_f': {   # target faces
        'top': np.full((3, 3), 'w', dtype=str)
        # , 'left': np.full((3, 3), 'o', dtype=str),
        # 'front': np.full((3, 3), 'g', dtype=str), 'right': np.full((3, 3), 'r', dtype=str),
        # 'back': np.full((3, 3), 'b', dtype=str), 'bottom': np.full((3, 3), 'y', dtype=str)
    }
}
# size_c = 3
# print(clear_state['faces'])
# print(size_c)
# # print(np.full((0, 9), clear_state['faces'][0:19]))
# print(np.array(list(clear_state['faces'][0:9])).reshape(3, 3))
# print(clear_state['old_f']['top'])

# exit()
test1 = {  # maybe name it in full
    'corner_permutation': [4, 1, 2, 7, 3, 5, 6, 0],
    'edge_permutation': [8, 1, 2, 11, 4, 5, 6, 7, 3, 9, 10, 0],
    'corner_orientation': [1, 0, 0, 1, 2, 0, 0, 2],
    'edge_orientation': [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1]
}

test2 = { # maybe name it in full # RUru
    'corner_permutation': [7, 1, 2, 6, 4, 5, 3, 0],
    'edge_permutation': [0, 1, 2, 6, 4, 5, 11, 7, 8, 9, 10, 3],
    'corner_orientation': [2, 0, 0, 2, 0, 0, 0, 2],
    'edge_orientation': [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
}

test3 = {  # 'U','R2','U','R','U','B2','R','B\'','R','U','L','D','L','D2'
    'corner_permutation': [4, 6, 0, 7, 5, 2, 1, 3],
    'edge_permutation': [1, 9, 7, 0, 8, 3, 4, 11, 6, 10, 5, 2],
    'corner_orientation': [1, 2, 2, 0, 0, 2, 1, 1],
    'edge_orientation': [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1]
}

