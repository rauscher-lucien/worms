import os
import numpy as np
from PIL import Image
import scipy.ndimage
from skimage import morphology
import math
import matplotlib.pyplot as plt

from find_head import *
from binarize import *
from make_skel import *
from make_ordered_skel import *


def get_angles(video_number, path):

    # identifying the head
    print("finding the head")
    image_number = 0  # number of the image
    head_pos = find_head(video_number, path)

    segmented_path = os.path.join(path, 'video_'+str(video_number)+r'_files\segmented_pics')
    number_of_points = 30  # number of points we want on the skeleton
    all_angles = np.array([np.empty((number_of_points-1, ))])
    # print(all_angles.shape)

    while os.path.exists(os.path.join(segmented_path, 'seg_worms_' + str(image_number) + '.jpg')):

        img = Image.open(os.path.join(segmented_path, 'seg_worms_'+str(image_number)+'.jpg')).convert("L")
        image = np.array(img)

        # make binary
        binary = binarize(image)

        # make skel
        skel_coords, skel_ends = make_skel(binary)

        # make ordered skeleton
        # print(image_number)
        ordered_skel, head_pos = make_ordered_skel(skel_coords, skel_ends, head_pos)

        dots_list = ordered_skel[0::(len(ordered_skel)//number_of_points)]  # get evenly spaced points
        dots_list = dots_list[:number_of_points]  # make sure you only keep the right number

        # straightforward angle calculation
        angles_arr = np.empty((1, dots_list.shape[0]-1))  # where we save the angles
        for i in range(dots_list.shape[0]-1):
            vec0 = [1, 0]
            vec1 = [dots_list[i+1, 0]-dots_list[i, 0], dots_list[i+1, 1]-dots_list[i, 1]]
            # print(vec1)
            angle = np.dot(vec1, vec0)/(np.linalg.norm(vec1)*np.linalg.norm(vec0))
            if math.isnan(angle):
                angle = 0
            # print(angle)
            angles_arr[0, i] = angle

        angles_arr -= angles_arr.mean()
        # print(angles_arr.shape)
        all_angles = np.concatenate((all_angles, angles_arr), axis=0)

        image_number += 1

    return all_angles
