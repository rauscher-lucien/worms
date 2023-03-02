import os
import numpy as np
from PIL import Image
from scipy.ndimage import binary_fill_holes, binary_closing
from skimage import morphology


def thresholding(video_number, path):

    pic_path = os.path.join(path, 'video_'+str(video_number)+r'_files\raw_pics')

    # create folder where we'll save the binary pics
    if not os.path.exists(os.path.join(path, 'video_'+str(video_number)+r'_files\binary_pics')):
        os.mkdir(os.path.join(path, 'video_'+str(video_number)+r'_files\binary_pics'))

    binary_path = os.path.join(path, 'video_'+str(video_number)+r'_files\binary_pics')

    i = 0
    while os.path.exists(os.path.join(pic_path, 'raw_worms_'+str(i)+'.jpg')):

        img = Image.open(os.path.join(pic_path, 'raw_worms_'+str(i)+'.jpg')).convert("L")
        image = np.array(img)

        thresh = 90
        binary = image <= thresh

        # Fills the holes in binary objects
        binary_no_holes = binary_fill_holes(binary)
        # Apply closing operation
        binary_no_holes_closed = morphology.binary_closing(binary_no_holes, morphology.disk(6))

        im = Image.fromarray(binary_no_holes_closed)
        im.save(os.path.join(binary_path, 'bin_worms_'+str(i)+'.jpg'))
        i += 1
        # print(i)