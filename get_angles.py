import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.filters import threshold_otsu
import scipy.ndimage
from skimage import morphology
import cv2
import math

video_number = 1  # number of the video
path = r'C:\Users\rausc\code_project'  # your path
pic_path = os.path.join(path, 'video_'+str(video_number)+r'_files\raw_pics')

i = 0

img = Image.open(os.path.join(pic_path, 'raw_worms'+str(i)+'.jpg')).convert("L")
image = np.array(img)

# thresholding, closing and skeleton
thresh = 90
binary = image <= thresh
binary_no_holes_closed = morphology.binary_closing(binary, morphology.disk(6))
skel = np.array(morphology.skeletonize(binary_no_holes_closed))
skel = skel.astype(int)

# get coordinates of skeleton
ind1 = np.where(skel != [0])
coord1 = np.array(list(zip(ind1[0], ind1[1])))

# find endpoints of skeleton through convolution
kernel = np.array([[1, 1, 1],
                   [1, 1, 1],
                   [1, 1, 1]])
ind2 = np.where((scipy.ndimage.convolve(skel, kernel, mode='constant', cval=0, origin=0) == 2) & (skel == 1))
coord2 = np.array(list(zip(ind2[0], ind2[1])))

# sort all skel points
# - idea is to start at one end of the worm and then find the next skeleton point that is nearest to that end,
#   this point will be our new reference point, then we find the next point on the skeleton that is nearest
#   to our new reference point and make that the reference, while we do that we save all coordinates and by that
#   we get a sequence of coordinates that symbolizes the worm
# - we want an ordered list of all points of the skeleton so we can place evenly spaced points
skel_list = np.array([[0, 0]])  # make empty list where we will save all coordinates of the skeleton in order
coordinates = coord1
reference = coord2[0]

distances_arr = np.array(list(map(lambda x: np.sqrt((x[0]-reference[0])**2+(x[1]-reference[1])**2), coordinates)))
ind = np.argsort(distances_arr)
coordinates = [coordinates[i] for i in ind]
coordinates = coordinates[1:]

while np.size(coordinates) != 0:  # we loop until all coordinates have been used
    # make an array of all distances to the reference point
    distances_arr = np.array(list(map(lambda x: np.sqrt((x[0]-reference[0])**2+(x[1]-reference[1])**2), coordinates)))
    ind = np.argsort(distances_arr)  # argsort the distances...
    coordinates = [coordinates[i] for i in ind]  # ...and sort the coordinates by their distance to the ref
    reference = coordinates[0]  # make new ref point the nearest point
    skel_list = np.concatenate((skel_list, [reference]))  # add new point to the sorted list of coordinates
    coordinates = coordinates[1:]  # remove the added coordinate so it doesnt get added again

skel_list = skel_list[1:]  # remove the zero at the beginning
dots_list = skel_list[0::10]  # get evenly spaced points

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
print(dots_list.shape)

# straightforward angle calculation
angles_list = []  # where we save the angles
for i in range(dots_list.shape[0]-1):
    vec0 = [1, 0]
    vec1 = [dots_list[i+1, 0]-dots_list[i, 0], dots_list[i+1, 1]-dots_list[i, 1]]
    print(vec1)
    angle = np.dot(vec1, vec0)/(np.linalg.norm(vec1)*np.linalg.norm(vec0))
    if math.isnan(angle):
        angle = 0
    print(angle)
    angles_list.append(angle)

plt.plot(angles_list)
plt.show()
