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
    np.save(os.path.join(path, 'video_' + str(video_number) + r'_files\e_vals_'+str(video_number)+'.npy'), e_vals)
    e_vecs = e_vecs[:, idx]

    # Keep the numEigWorms dimensions that capture most of the variance
    eigen_worms = e_vecs[:, :num_eig_worms].T
    np.save(os.path.join(path, 'video_' + str(video_number)
                         + r'_files\eigen_worms_'+str(video_number)+'.npy'), eigen_worms)
    eigen_vals = e_vals[:num_eig_worms]
