import numpy as np

a = np.array([0, 0])
# print(a)
c = np.array([[1, 1]])
print(a.shape)
b = np.concatenate((c, [a]))
print(b)


