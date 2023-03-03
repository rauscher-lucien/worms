import os
import numpy as np
from PIL import Image
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

        # thresholding, closing and removing small objects
        thresh = 90
        binary = image <= thresh
        binary = morphology.binary_closing(binary, morphology.disk(5))
        binary = morphology.remove_small_objects(binary, min_size=100, connectivity=8, out=None)

        im = Image.fromarray(binary)
        im.save(os.path.join(binary_path, 'bin_worms_'+str(i)+'.jpg'))
        i += 1
        # print(i)
