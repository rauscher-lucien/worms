import os
from PIL import Image

from binarize import *
from make_skel import *

# a prompt is gonna appear that is gonna show two coordinates with the numbers 0 and 1; the coordinates are the
# coordinates of the two endpoints of the skeleton; you now need to manually open the first raw image of the set;
# the coordinates work in a way that the origin is in the upper left corner and the y axis is horizontal and the x axis
# goes downwards; the only acceptable inputs are 0 or 1 and you need to choose which one of the two coordinates
# represents the head


def find_head(video_number, path):

    # open image
    image_number = 0
    pic_path = os.path.join(path, 'video_' + str(video_number) + r'_files\segmented_pics')
    img = Image.open(os.path.join(pic_path, 'seg_worms_' + str(image_number) + '.jpg')).convert("L")
    image = np.array(img)

    # make binary
    binary = binarize(image)

    # make skel
    _, skel_ends, skel = make_skel(binary)

    # plt.imshow(skel)
    # plt.show()

    y = int(input("0: "+str(skel_ends[0, :])+" or 1: "+str(skel_ends[1, :])+" -> "))
    return skel_ends[y, :]
