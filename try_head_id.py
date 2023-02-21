import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from skimage.filters import threshold_otsu
from scipy.ndimage import binary_fill_holes, binary_closing
from skimage import morphology

video_number = 1  # number of the video
path = r'C:\Users\rausc\code_project'  # your path
pic_path = os.path.join(path, 'video_'+str(video_number)+r'_files\raw_pics')

i = 0

img = Image.open(os.path.join(pic_path, 'raw_worms'+str(i)+'.jpg')).convert("L")
image = np.array(img)

thresh = 90
binary = image <= thresh

binary_no_holes_closed = morphology.binary_closing(binary, morphology.disk(6))

skel = morphology.skeletonize(binary_no_holes_closed)

obj = skel

im = Image.fromarray(obj)

im.show()
