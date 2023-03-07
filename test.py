import numpy as np

a = np.array([[0, 1], [2, 1]])
b = np.array([[1, 1], [2, 3]])
c = np.stack((a, b, a), axis=2)
print(c)


