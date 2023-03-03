import os
import numpy as np
from PIL import Image
import scipy.ndimage
from skimage import morphology
import math
import matplotlib.pyplot as plt


def get_angles(video_number, image_number, path, head_pos):

    # open image
    pic_path = os.path.join(path, 'video_'+str(video_number)+r'_files\segmented_pics')
    img = Image.open(os.path.join(pic_path, 'seg_worms_'+str(image_number)+'.jpg')).convert("L")
    image = np.array(img)

    # thresholding, closing and skeleton
    thresh = 90
    binary = image <= thresh
    binary = morphology.binary_closing(binary, morphology.disk(10))
    binary = morphology.remove_small_objects(binary, min_size=100, connectivity=8, out=None)
    skel = np.array(morphology.skeletonize(binary))
    skel = skel.astype(int)

    # get coordinates of skeleton
    ind1 = np.where(skel != [0])
    coord1 = np.array(list(zip(ind1[0], ind1[1])))

    # find endpoints of skeleton through convolution
    kernel = np.array([[1, 1, 1],
                       [1, 1, 1],
                       [1, 1, 1]])
    ind2 = np.where((scipy.ndimage.convolve(skel, kernel, mode='constant', cval=0, origin=0) == 2) & (skel == 1))
    end_points = np.array(list(zip(ind2[0], ind2[1])))

    # sort all skel points
    # - idea is to start at one end of the worm and then find the next skeleton point that is nearest to that end,
    #   this point will be our new reference point, then we find the next point on the skeleton that is nearest
    #   to our new reference point and make that the reference, while we do that we save all coordinates and by that
    #   we get a sequence of coordinates that symbolizes the worm
    # - we want an ordered list of all points of the skeleton so we can place evenly spaced points
    skel_list = np.array([[0, 0]])  # make empty list where we will save all coordinates of the skeleton in order
    coordinates = coord1

    # get new head pos from previous head pos
    end_distances = np.array(list(map(lambda x: np.sqrt((x[0]-head_pos[0])**2+(x[1]-head_pos[1])**2), end_points)))
    ind = np.argsort(end_distances)
    end_points = [end_points[i] for i in ind]
    head_pos = end_points[0]
    # print(head_pos)

    # delete endpoint so we dont add it twice to the list of skel points
    distances_arr = np.array(list(map(lambda x: np.sqrt((x[0]-head_pos[0])**2+(x[1]-head_pos[1])**2), coordinates)))
    ind = np.argsort(distances_arr)
    coordinates = [coordinates[i] for i in ind]
    coordinates = coordinates[1:]
    reference = head_pos

    while np.size(coordinates) != 0:  # we loop until all coordinates have been used
        # make an array of all distances to the reference point
        distances_arr = np.array(list(map(lambda x: np.sqrt((x[0]-reference[0])**2+(x[1]-reference[1])**2), coordinates)))
        ind = np.argsort(distances_arr)  # argsort the distances...
        coordinates = [coordinates[i] for i in ind]  # ...and sort the coordinates by their distance to the ref
        reference = coordinates[0]  # make new ref point the nearest point
        skel_list = np.concatenate((skel_list, [reference]))  # add new point to the sorted list of coordinates
        coordinates = coordinates[1:]  # remove the added coordinate so it doesnt get added again

    skel_list = skel_list[1:]  # remove the zero at the beginning
    number_of_points = 30  # number of points we want on the skeleton
    dots_list = skel_list[0::(len(skel_list)//number_of_points)]  # get evenly spaced points
    dots_list = dots_list[:number_of_points]

    # for i in dots_list:
    #     print(i)
    # skel_rgb = np.dstack([skel * 255, skel*255, skel*255])
    # for i in dots_list:
    #     skel_rgb[i[0], i[1], 1:2] = 0
    # print(skel_rgb.shape)
    #
    # skel_rgb = skel_rgb.astype('uint8')
    # im = Image.fromarray(skel_rgb, 'RGB')
    # im.show()
    # print(dots_list.shape)

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

    return angles_arr, head_pos



