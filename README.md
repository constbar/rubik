## rubik

* нам без разницы какие где цвета находятся в решении и инициализация решения куба
* параметры к кубу можно хранить в конфиг файле
* добавить время выполнения
* make __slots__
* make good naming in .mtl fornmat and replace in ok order colors


* make F R U B L D
* R2 D’ B’ D F2 R F2 R2 U L’ F2 U’ B’ L2 R D B’ R’ B2 L2 F2 L2 R2 U2 D2


bonus
* visualization
* make 2 algo, god number + any other
* random generator shuffle
* 4x4x4, 2x2x2

* An algorithm that goes lower than the most optimized solutions in a reasonable
time (beyond a few seconds is not considered reasonable).
* A choice between several algorithms, or a selection of the best solution between
several algorithms


In general, the Thistlethwaite’s algorithms divides the problem into four
independent subproblems by using the following four nested groups Gi:

# another way to init
# this init can be thu iteration [r, b, y, g ...etc]
# {}, * 9 [:-1].format(w) -> [w w w w w w w ww w].reshape 3 x 3

# for init by numbers
# 'top': np.arange(cb_sz ** 2 * 0, cb_sz ** 2 * 1).reshape(cb_sz, cb_sz),
# 'left': np.arange(cb_sz ** 2 * 1, cb_sz ** 2 * 2).reshape(cb_sz, cb_sz),
# 'front': np.arange(cb_sz ** 2 * 2, cb_sz ** 2 * 3).reshape(cb_sz, cb_sz),
# 'right': np.arange(cb_sz ** 2 * 3, cb_sz ** 2 * 4).reshape(cb_sz, cb_sz),
# 'back': np.arange(cb_sz ** 2 * 4, cb_sz ** 2 * 5).reshape(cb_sz, cb_sz),
# 'bottom': np.arange(cb_sz ** 2 * 5, cb_sz ** 2 * 6).reshape(cb_sz, cb_sz),


self.faces = {   # target faces
            'top': np.full((3, 3), 'w', dtype=str), 'left': np.full((3, 3), 'o', dtype=str),
            'front': np.full((3, 3), 'g', dtype=str), 'right': np.full((3, 3), 'r', dtype=str),
            'back': np.full((3, 3), 'b', dtype=str), 'bottom': np.full((3, 3), 'y', dtype=str)
        }

a12 = ['R2', 'D', 'B', 'F\'', 'R2', 'B\'', 'F', 'D', 'R2']
        acw12 = ['B2', 'D', 'L', 'R\'', 'B2', 'L\'', 'R', 'D', 'B2']
        a13 = ['R2', 'D\'', 'B', 'F\'', 'R2', 'B\'', 'F', 'D\'', 'R2']
        acw13 = ['B2', 'D\'', 'L', 'R\'', 'B2', 'L\'', 'R', 'D\'', 'B2']
last layer



# test = tests.clear_state
#
# kek = RubikState(test['cepo'], test['faces'], None, notation_path=None)
# randm = make_random_state()
# kek.make_move(randm)
# solv = RubikSolver(kek)
# print(gre(solv.rubik_state))

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