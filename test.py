import numpy as np

k = ['1', '2', '3',
     '4', '5', '6',
     '7', '8', '9']

k = np.array(k)
k = k.reshape(3, 3)

l = ['a', 'b', 'c',
     'd', 'e', 'f',
     'g', 'h', 'i']

l = np.array(l)
l = l.reshape(3, 3)


k[:,[2]], l[:,[2]],  = l[:,[2]], k[:,[2]]


# print('L')
# print(l)
# print()
# print('K')
# print(k)

a = np.full((3, 3), 'w') # fils with smt to all matrix
print(a)



# init 3 x 3 matrix. like
# {}, * 9 [:-1].format(w) -> [w w w w w w w ww w].reshape 3 x 3
# what is np . flip
# can check movements by compare it with rubik library

# if need side is L[:, [1:2]] == www and L[[1:2], :] -> means cross for example

# if self.name == 'WUR' or self.name == 'WRU' or self.name == 'RUW' or self.name == 'RWU' or self.name == 'UWR' or self.name == 'URW':
# can make all kind of combinations with collections


# (-1, -1, -1) if all means - vertex