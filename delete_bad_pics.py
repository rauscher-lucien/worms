import os
import numpy as np
import scipy.ndimage
from PIL import Image
from skimage import morphology

from binarize import *
from make_skel import *


def delete_bad_pics(video_number, path):

    if not os.path.exists(os.path.join(path, 'video_'+str(video_number)+r'_files\segmented_pics')):
        os.mkdir(os.path.join(path, 'video_'+str(video_number)+r'_files\segmented_pics'))

    raw_path = os.path.join(path, 'video_'+str(video_number)+r'_files\raw_pics')
    segmented_path = os.path.join(path, 'video_'+str(video_number)+r'_files\segmented_pics')

    # delete jumps
    i = 1
    list_of_diffs = []
    new_img = Image.open(os.path.join(raw_path, 'raw_worms_'+str(i)+'.jpg')).convert("L")
    new_image = np.array(new_img)
    new_image = binarize(new_image)
    i += 1

    while os.path.exists(os.path.join(raw_path, 'raw_worms_'+str(i)+'.jpg')):  # loop over all pics

        old_image = new_image
        new_img = Image.open(os.path.join(raw_path, 'raw_worms_'+str(i)+'.jpg')).convert("L")
        new_image = np.array(new_img)
        new_image = binarize(new_image)
        diff = np.sum(np.sum(new_image-old_image))  # calculate binary difference between images
        list_of_diffs.append(diff)

        i += 1

    d = np.abs(list_of_diffs - np.median(list_of_diffs))  # get how much each value is away from the median
    mdev = np.median(d)  # get median of the distance of each value from the mean
    s = d / mdev if mdev else np.zero(len(d))  # normalize
    list_of_jumps = []
    for i in range(len(s)):
        if s[i] > 10:
            # print(i)
            list_of_jumps.append(i)

    frames_to_delete = []
    for i in list_of_jumps:
        for j in range(i-2, i+2):
            frames_to_delete.append(j)

    # delete all worms that dont have a good skel
    while os.path.exists(os.path.join(raw_path, 'raw_worms_' + str(i) + '.jpg')):  # loop over all pics

        img = Image.open(os.path.join(raw_path, 'raw_worms_' + str(i) + '.jpg')).convert("L")
        image = np.array(img)

        # make binary
        binary = binarize(image)

        # get info out of skel
        _, skel_ends, _ = make_skel(binary)

        if len(skel_ends) != 2:
            frames_to_delete.append(i)

        i += 1

    i = 0
    j = 0
    while os.path.exists(os.path.join(raw_path, 'raw_worms_'+str(i)+'.jpg')):  # loop over all pics
        if i not in frames_to_delete:
            img = Image.open(os.path.join(raw_path, 'raw_worms_' + str(i) + '.jpg')).convert("L")
            img.save(os.path.join(segmented_path, 'seg_worms_' + str(j) + '.jpg'))
            j += 1
        i += 1

    # plt.plot(list_of_diffs)
    # plt.show()
