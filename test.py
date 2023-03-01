import numpy as np
import matplotlib.pyplot as plt

a = np.array([[1, 1, 1]])
b = np.array([[2, 3, 1]])
a = np.concatenate((a, b), axis=0)
print(a, a.shape)
