import os
import numpy as np
import scipy.ndimage as ndimage
from PIL import Image
from matplotlib import pyplot as plt


def delete_cam_jumps(video_number, path):

    if not os.path.exists(os.path.join(path, 'video_'+str(video_number)+r'_files\segmented_pics')):
        os.mkdir(os.path.join(path, 'video_'+str(video_number)+r'_files\segmented_pics'))

    pic_path = os.path.join(path, 'video_'+str(video_number)+r'_files\raw_pics')
    binary_path = os.path.join(path, 'video_'+str(video_number)+r'_files\binary_pics')
    segmented_path = os.path.join(path, 'video_'+str(video_number)+r'_files\segmented_pics')

    # prepare the loop
    i = 1
    list_of_diffs = []
    new_img = Image.open(os.path.join(binary_path, 'bin_worms_'+str(i)+'.jpg')).convert("L")
    new_image = np.array(new_img)
    i += 1
    while os.path.exists(os.path.join(binary_path, 'bin_worms_'+str(i)+'.jpg')):  # loop over all pics

        old_image = new_image
        new_img = Image.open(os.path.join(binary_path, 'bin_worms_'+str(i)+'.jpg')).convert("L")
        new_image = np.array(new_img)
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

    # print(frames_to_delete)

    i = 0
    j = 0
    while os.path.exists(os.path.join(binary_path, 'bin_worms_'+str(i)+'.jpg')):  # loop over all pics
        if i not in frames_to_delete:
            img = Image.open(os.path.join(pic_path, 'raw_worms_' + str(i) + '.jpg')).convert("L")
            img.save(os.path.join(segmented_path, 'seg_worms_' + str(j) + '.jpg'))
            j += 1
        i += 1

    # plt.plot(list_of_diffs)
    # plt.show()
