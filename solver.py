import numpy as np

cb_sz = 3
clockwise = (1, 0)
counterclockwise = (0, 1)


class Cube:
    def __init__(self, shuffled_cube):
        self.faces = {   # target faces
            'top': np.full((3, 3), 'w', dtype=str),
            'left': np.full((3, 3), 'o', dtype=str),
            'front': np.full((3, 3), 'g', dtype=str),
            'right': np.full((3, 3), 'r', dtype=str),
            'back': np.full((3, 3), 'b', dtype=str),
            'bottom': np.full((3, 3), 'y', dtype=str)

            # 'top': np.full((3, 3), 'w', dtype=str),
            # 'left': np.full((3, 3), 'g', dtype=str),
            # 'front': np.full((3, 3), 'r', dtype=str),
            # 'right': np.full((3, 3), 'b', dtype=str),
            # 'back': np.full((3, 3), 'o', dtype=str),
            # 'bottom': np.full((3, 3), 'y', dtype=str)

            # 'top': np.arange(cb_sz ** 2 * 0, cb_sz ** 2 * 1).reshape(cb_sz, cb_sz),
            # 'left': np.arange(cb_sz ** 2 * 1, cb_sz ** 2 * 2).reshape(cb_sz, cb_sz),
            # 'front': np.arange(cb_sz ** 2 * 2, cb_sz ** 2 * 3).reshape(cb_sz, cb_sz),
            # 'right': np.arange(cb_sz ** 2 * 3, cb_sz ** 2 * 4).reshape(cb_sz, cb_sz),
            # 'back': np.arange(cb_sz ** 2 * 4, cb_sz ** 2 * 5).reshape(cb_sz, cb_sz),
            # 'bottom': np.arange(cb_sz ** 2 * 5, cb_sz ** 2 * 6).reshape(cb_sz, cb_sz),
        }

        self.shuffled_cube = shuffled_cube
        print(shuffled_cube)


        self.moves = list()

    """ U notation """
    def u_clockwise(self):
        # pass
        self.faces['top'] = np.rot90(self.faces['top'], axes=clockwise)
        self.faces['front'][[0]], self.faces['right'][[0]], \
            self.faces['back'][[0]], self.faces['left'][[0]] \
            = self.faces['right'][[0]], self.faces['back'][[0]], \
            self.faces['left'][[0]], self.faces['front'][[0]]
        self.moves.append('U')

    def u_double_clockwise(self):
        self.u_clockwise()
        self.u_clockwise()
        # self.moves.append('U2')

    def u_counterclockwise(self):
        self.u_clockwise()
        self.u_clockwise()
        self.u_clockwise()
        # self.moves.append('U\'')

    """ D notation """
    def d_clockwise(self):
        self.faces['bottom'] = np.rot90(self.faces['bottom'], axes=clockwise)
        self.faces['front'][[2]], self.faces['right'][[2]], \
            self.faces['back'][[2]], self.faces['left'][[2]] \
            = self.faces['left'][[2]], self.faces['front'][[2]], \
            self.faces['right'][[2]], self.faces['back'][[2]]
        self.moves.append('D')

    def d_double_clockwise(self):
        self.d_clockwise()
        self.d_clockwise()
        # self.moves.append('D2')

    def d_counterclockwise(self):
        self.d_clockwise()
        self.d_clockwise()
        self.d_clockwise()
        # self.moves.append('D\'')

    """ L notation """
    def l_clockwise(self):
        self.faces['left'] = np.rot90(self.faces['left'], axes=clockwise)
        self.faces['front'][:, [0]], self.faces['top'][:, [0]], \
            self.faces['back'][:, [2]], self.faces['bottom'][:, [0]] \
            = self.faces['top'][:, [0]], self.faces['back'][:, [2]][::-1], \
            self.faces['bottom'][:, [0]][::-1], self.faces['front'][:, [0]]
        self.moves.append('L')

    def l_double_clockwise(self):
        self.l_clockwise()
        self.l_clockwise()
        # self.moves.append('L2')

    def l_counterclockwise(self):
        self.l_clockwise()
        self.l_clockwise()
        self.l_clockwise()
        # self.moves.append('L\'')

    """ R notation """
    def r_clockwise(self):
        self.faces['right'] = np.rot90(self.faces['right'], axes=clockwise)
        self.faces['front'][:, [2]], self.faces['top'][:, [2]], \
            self.faces['back'][:, [0]], self.faces['bottom'][:, [2]] \
            = self.faces['bottom'][:, [2]], self.faces['front'][:, [2]], \
            self.faces['top'][:, [2]][::-1], self.faces['back'][:, [0]][::-1]
        self.moves.append('R')

    def r_double_clockwise(self):
        self.r_clockwise()
        self.r_clockwise()
        # self.moves.append('R2')

    def r_counterclockwise(self):
        self.r_clockwise()
        self.r_clockwise()
        self.r_clockwise()
        # self.moves.append('R\'')

    """ F notation """
    def f_clockwise(self):
        self.faces['front'] = np.rot90(self.faces['front'], axes=clockwise)
        self.faces['top'][[2]], self.faces['right'][:, [0]], \
            self.faces['bottom'][[0]], self.faces['left'][:, [2]] \
            = np.rot90(self.faces['left'][:, [2]][::-1]),\
            np.rot90(self.faces['top'][[2]])[::-1], \
            np.rot90(self.faces['right'][:, [0]][::-1]),\
            np.rot90(self.faces['bottom'][[0]])[::-1]
        self.moves.append('F')

    def f_double_clockwise(self):
        self.f_clockwise()
        self.f_clockwise()
        # self.moves.append('F2')

    def f_counterclockwise(self):
        self.f_clockwise()
        self.f_clockwise()
        self.f_clockwise()
        # self.moves.append('F\'')

    """ B notation """
    def b_clockwise(self):
        self.faces['back'] = np.rot90(self.faces['back'], axes=clockwise)
        self.faces['top'][[0]], self.faces['right'][:, [2]], \
            self.faces['bottom'][[2]], self.faces['left'][:, [0]] \
            = np.rot90(self.faces['right'][:, [2]]), \
            np.rot90(self.faces['bottom'][[2]]), \
            np.rot90(self.faces['left'][:, [0]]), \
            np.rot90(self.faces['top'][[0]])
        self.moves.append('B')

    def b_double_clockwise(self):
        self.b_clockwise()
        self.b_clockwise()
        # self.moves.append('B2')

    def b_counterclockwise(self):
        self.b_clockwise()
        self.b_clockwise()
        self.b_clockwise()
        # self.moves.append('B\'')

    def __str__(self):
        state = ''
        # for v in self.faces.values():
        for k, v in self.faces.items():
            # print(k)
            # print(v)
            # print()

            state += ''.join(sum(v.tolist(), []))

        # """ # block printing
        for i in range(len(state)):
            if i % 3 == 0:
                print('')
            if i % 9 == 0:
                print()
            print(state[i], end='')
        # """
        # return state
        return ''


    # def random_moves(self):
    #     pass

kek = Cube("B U' B' F' D B2 L2 U2 L' R' D L2 U2 R' F' L2 R' B2 D2 U L' D' U' B F2 L' R2 U R2 D2")

"""
print(kek.faces['top'])
print(kek.faces['left'])
print(kek.faces['front'])
print(kek.faces['right'])
print(kek.faces['back'])
print(kek.faces['bottom'])
"""
kek.u_clockwise(); kek.r_clockwise(); kek.u_clockwise(); kek.r_clockwise()
kek.d_clockwise(); kek.r_clockwise(); kek.r_clockwise(); kek.r_clockwise()
kek.l_clockwise(); kek.f_clockwise(); kek.l_double_clockwise(); kek.f_clockwise()
kek.r_double_clockwise(); kek.r_clockwise(); kek.f_clockwise()
kek.f_counterclockwise(); kek.b_clockwise(); kek.r_clockwise()
kek.f_double_clockwise(); kek.r_clockwise(); kek.d_clockwise()
kek.r_clockwise(); kek.u_clockwise(); kek.r_clockwise(); kek.u_clockwise()

print(kek)
print(' '.join(kek.moves))


