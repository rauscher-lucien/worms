import os
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt


def eigenworms(video_number, path, cov_mat, num_eig_worms, verbose=True):

    # Get the eigenvectors and eigenvalues of the covariance matrix
    e_vals, e_vecs = la.eigh(cov_mat)

    # Sort the eigenvalues and eigenvectors
    idx = np.argsort(e_vals)[::-1]
    e_vals = e_vals[idx]
    np.save(os.path.join(path, 'video_' + str(video_number) + r'_files\e_vals'), e_vals)
    e_vecs = e_vecs[:, idx]

    # Keep the numEigWorms dimensions that capture most of the variance
    eigen_worms = e_vecs[:, :num_eig_worms].T
    np.save(os.path.join(path, 'video_' + str(video_number) + r'_files\eigen_worms'), eigen_worms)
    eigen_vals = e_vals[:num_eig_worms]
    # print(eigen_worms)
    if verbose:
        # Plot eigenvalues to show fraction of variance explained

        fig, ax = plt.subplots()
        ax.plot(np.cumsum(e_vals) / np.sum(e_vals), 'o', markeredgecolor=[1, 0.5, 0.1], markerfacecolor=[1, 0.5, 0.1],
                markersize=8)
        ax.set_xlabel('Number of eigenworms')
        ax.set_ylabel('Fraction of variance explained')
        ax.set_xlim(0, num_eig_worms)
        ax.set_ylim(0, 1)
        ax.set_title('Variance explained by eigenworms')

        # Plot the eigenworms
        fig, axs = plt.subplots(nrows=num_eig_worms, ncols=1, figsize=(5, 10))
        for i in range(num_eig_worms):
            axs[i].plot(eigen_worms[i, :], color=[1, 0.5, 0.1], linewidth=2)
            # axs[i].set_xlim(0, numPixels)
            # axs[i].set_ylim(0, eigenWorms)