import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage
from skimage import morphology


def make_skel(binary):

    # make skel
    skel = np.array(morphology.skeletonize(binary))
    skel = skel.astype(int)

    # get coordinates of skeleton
    ind1 = np.where(skel != [0])
    skel_coords = np.array(list(zip(ind1[0], ind1[1])))

    # find endpoints of skeleton through convolution
    kernel = np.array([[1, 1, 1],
                       [1, 1, 1],
                       [1, 1, 1]])
    ind2 = np.where((scipy.ndimage.convolve(skel, kernel, mode='constant', cval=0, origin=0) == 2) & (skel == 1))
    skel_ends = np.array(list(zip(ind2[0], ind2[1])))

    # print(skel_coords)
    # print(skel_ends)
    # print(skel_ends.shape)
    # plt.imshow(skel)
    # plt.show()

    return skel_coords, skel_ends, skel
