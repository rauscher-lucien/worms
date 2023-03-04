import matplotlib.pyplot as plt

from image_exc import *
from thresholding import *
from delete_bad_pics import *
from find_head import *
from get_angles import *
from eigenworms import *

video_number = 1  # number of the video
path = r'C:\Users\rausc\code_project'  # your path
# inside your path you need a folder called 'files' where the videos are saved
# the videos need to be called 'video_i' where 'i' is the number of the video
# make sure you have enough space

# get singular images from the video and save them
print("starting image extraction")
image_extraction(video_number, path)

# create new folder without camera jumps and bad skels
print("deleting bad pics")
delete_bad_pics(video_number, path)

# calculate all angular distributions
all_angles = get_angles(video_number, path)
# print(all_angles)
# calculating covariance matrix
print("getting covariance matrix")
cov_angles = np.cov(all_angles.T, bias=1)
# print(cov_angles)
np.save(os.path.join(path, 'video_'+str(video_number)+r'_files\cov_angles_'+str(video_number)+'.npy'), cov_angles)

# getting eigenworms
print("getting eigenworms")
eigenworms(video_number, path, cov_angles, 4)
plt.show()
