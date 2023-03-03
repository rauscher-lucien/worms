from skimage import morphology


def binarize(image):

    # thresholding
    thresh = 90
    binary = image <= thresh
    binary = binary.astype(int)

    # binary closing for holes inside the worm
    binary = morphology.binary_closing(binary, morphology.disk(5))

    # remove edges
    binary[0, :] = 0
    binary[-1, :] = 0
    binary[:, 0] = 0
    binary[:, -1] = 0

    # remove all small objects
    binary = morphology.remove_small_objects(binary, min_size=100, connectivity=8, out=None)
    binary = binary.astype(int)

    return binary
