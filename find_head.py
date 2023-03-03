import matplotlib.pyplot as plt
import numpy as np
import os
from skimage import morphology
from PIL import Image
import scipy.ndimage

# a prompt is gonna appear that is gonna show two coordinates with the numbers 0 and 1; the coordinates are the
# coordinates of the two endpoints of the skeleton; you now need to manually open the first raw image of the set;
# the coordinates work in a way that the origin is in the upper left corner and the y axis is horizontal and the x axis
# goes downwards; the only acceptable inputs are 0 or 1 and you need to choose which one of the two coordinates
# represents the head


def find_head(video_number, image_number, path):

    # open image
    pic_path = os.path.join(path, 'video_' + str(video_number) + r'_files\segmented_pics')
    img = Image.open(os.path.join(pic_path, 'seg_worms_' + str(image_number) + '.jpg')).convert("L")
    image = np.array(img)

    # thresholding, closing and skeleton
    thresh = 90
    binary = image <= thresh
    binary = morphology.binary_closing(binary, morphology.disk(10))
    binary = morphology.remove_small_objects(binary, min_size=100, connectivity=8, out=None)
    skel = np.array(morphology.skeletonize(binary))
    skel = skel.astype(int)
    plt.imshow(skel)
    plt.show()

    # get coordinates of skeleton
    ind1 = np.where(skel != [0])
    coord1 = np.array(list(zip(ind1[0], ind1[1])))

    # find endpoints of skeleton through convolution
    kernel = np.array([[1, 1, 1],
                       [1, 1, 1],
                       [1, 1, 1]])
    ind2 = np.where((scipy.ndimage.convolve(skel, kernel, mode='constant', cval=0, origin=0) == 2) & (skel == 1))
    coord2 = np.array(list(zip(ind2[0], ind2[1])))
    y = int(input("0: "+str(coord2[0])+" or 1: "+str(coord2[1])))
    return coord2[y]
