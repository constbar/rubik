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