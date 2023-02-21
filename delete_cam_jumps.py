import os
import numpy as np
import scipy.ndimage as ndimage
from PIL import Image
from matplotlib import pyplot as plt

video_number = 1
path = r'C:\Users\rausc\code_project'  # your path
binary_path = os.path.join(path, 'video_'+str(video_number)+r'_files\binary_pics')

if not os.path.exists(os.path.join(path, 'video_'+str(video_number)+r'_files\segmented_pics')):
    os.mkdir(os.path.join(path, 'video_'+str(video_number)+r'_files\segmented_pics'))

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
list_of_jumps.append(0)
for i in range(len(s)):
    if s[i] > 10:
        print(i)
        list_of_jumps.append(i)

plt.plot(list_of_diffs)
plt.show()
