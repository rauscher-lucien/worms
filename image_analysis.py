import os
import numpy as np
import matplotlib.pyplot as plt

video_number = 5  # number of the video
path = r'C:\Users\rausc\code_project'  # your path

# work with the matrix

cov_mat = np.load(os.path.join(path, 'video_'+str(video_number)+r'_files\cov_angles_'+str(video_number)+'.npy'))

plt.imshow(cov_mat, origin='lower')
plt.show()

# work with the eigenworms ################################

# e_vals = np.load(os.path.join(path, 'video_' + str(video_number) + r'_files\e_vals_'+str(video_number)+'.npy'))
# eigen_worms = np.load(os.path.join(path, 'video_' + str(video_number) + r'_files\eigen_worms_'+str(video_number)+'.npy'))
#
# num_eig_worms = 4
#
# print(eigen_worms)
#
# fig, ax = plt.subplots()
# ax.plot(np.cumsum(e_vals) / np.sum(e_vals), 'o', markeredgecolor=[1, 0.5, 0.1], markerfacecolor=[1, 0.5, 0.1],
#         markersize=8)
# ax.set_xlabel('Number of eigenworms')
# ax.set_ylabel('Fraction of variance explained')
# ax.set_xlim(0, num_eig_worms)
# ax.set_ylim(0, 1)
# ax.set_title('Variance explained by eigenworms')
#
# # Plot the eigenworms
# fig, axs = plt.subplots(nrows=num_eig_worms, ncols=1, figsize=(5, 10))
# for i in range(num_eig_worms):
#     axs[i].plot(eigen_worms[i, :], color=[1, 0.5, 0.1], linewidth=2)
#     # axs[i].set_xlim(0, numPixels)
#     # axs[i].set_ylim(0, eigenWorms)
#
# plt.show()

# plot superposition of eigenworms

num_eigenworms = 4
fig, axs = plt.subplots(nrows=num_eigenworms, ncols=1, figsize=(5, 10))
eigenworms_sum = np.zeros((4, 29))
index = 1
while os.path.exists(os.path.join(path, r'all_eigenworms\eigen_worms_'+str(index)+'.npy')):  # loop over all pics

    eigenworms = np.load(os.path.join(path, r'all_eigenworms\eigen_worms_'+str(index)+'.npy'))
    eigenworms_sum += eigenworms
    # print(eigenworms_sum[3, :])
    for i in range(num_eigenworms):
        axs[i].plot(eigenworms[i, :], color='black', linewidth=1, linestyle='dashed')
        # axs[i].set_xlim(0, numPixels)
        # axs[i].set_ylim(0, eigenWorms)

    index += 1

for i in range(num_eigenworms):
    axs[i].plot(eigenworms_sum[i, :]/(index-1), color='red', linewidth=1)
    # axs[i].set_xlim(0, numPixels)
    # axs[i].set_ylim(0, eigenWorms)

# print(eigenworms_sum[3, :]/(index-1))

plt.show()
