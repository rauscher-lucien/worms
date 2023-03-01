import matplotlib.pyplot as plt

from get_angles import *
from eigenworms import *

video_number = 1  # number of the video
image_number = 0  # number of the image
path = r'C:\Users\rausc\code_project'  # your path
#
# segmented_path = os.path.join(path, 'video_'+str(video_number)+r'_files\segmented_pics')
# all_angles = get_angles(video_number, image_number, path)
# while os.path.exists(os.path.join(segmented_path, 'seg_worms_'+str(image_number)+'.jpg')):
#     print(image_number)
#     angles_arr = get_angles(video_number, image_number, path)
#     # print(all_angles.shape, angles_arr.shape)
#     # print(angles_arr)
#     all_angles = np.concatenate((all_angles, angles_arr), axis=0)
#     image_number += 1
#
# # print(all_angles)
#
#
# cov_angles = np.cov(all_angles.T, bias=1)
# np.save(os.path.join(path, 'video_'+str(video_number)+r'_files\cov_angles'), cov_angles)
# # plt.imshow(cov_angles)
# # plt.colorbar()
# # plt.show()

cov_angles = np.load(os.path.join(path, 'video_'+str(video_number)+r'_files\cov_angles.npy'))
eigenworms(cov_angles, 4)
plt.show()
