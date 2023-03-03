import matplotlib.pyplot as plt

from image_exc import *
from thresholding import *
from delete_cam_jumps import *
from get_angles import *
from eigenworms import *

video_number = 2  # number of the video
path = r'C:\Users\rausc\code_project'  # your path
# inside your path you need a folder called 'files' where the videos are saved
# the videos need to be called 'video_i' where 'i' is the number of the video
# make sure you have enough space

# get singular images from the video and save them
print("starting image extraction")
image_extraction(video_number, path)

# create folder with binary images
print("starting thresholding")
thresholding(video_number, path)

# create new folder without camera jumps
print("deleting camera jumps")
delete_cam_jumps(video_number, path)

# calculate all angular distributions
print("getting angles")
image_number = 0  # number of the image
segmented_path = os.path.join(path, 'video_'+str(video_number)+r'_files\segmented_pics')
all_angles = get_angles(video_number, image_number, path)
while os.path.exists(os.path.join(segmented_path, 'seg_worms_'+str(image_number)+'.jpg')):
    # print(image_number)
    angles_arr = get_angles(video_number, image_number, path)
    # print(all_angles.shape, angles_arr.shape)
    # print(angles_arr)
    all_angles = np.concatenate((all_angles, angles_arr), axis=0)
    image_number += 1

# calculating covariance matrix
print("getting covariance matrix")
cov_angles = np.cov(all_angles.T, bias=1)
np.save(os.path.join(path, 'video_'+str(video_number)+r'_files\cov_angles_'+str(video_number)+'.npy'), cov_angles)
# plt.imshow(cov_angles)
# plt.colorbar()
# plt.show()

# cov_angles = np.load(os.path.join(path, 'video_'+str(video_number)+r'_files\cov_angles.npy'))

# getting eigenworms
print("getting eigenworms")
eigenworms(video_number, path, cov_angles, 4)
plt.show()
