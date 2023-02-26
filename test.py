import numpy as np
import scipy.ndimage

a = np.array([[0, 0, 0, 0],
              [0, 0, 0, 0],
              [0, 0, 0, 0]])

b = np.array([[1, 2], [2, 2]])

for i in b:
    a[i[0], i[1]] = 1

print(a)

