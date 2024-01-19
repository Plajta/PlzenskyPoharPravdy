import cv2
import imageio
import numpy as np
from skimage.io import imsave
import os
import numpy as np
import math

img_data_path = os.getcwd()[:os.getcwd().index("PlzenskyPoharPravdy") + len("PlzenskyPoharPravdy")] + "/data/img_data/"
slice_fact = 1000

for filename in os.listdir(img_data_path):
    if filename == ".gitkeep":
        continue
    abs_path = os.path.join(img_data_path, filename)
    img = imageio.imread(abs_path).astype(np.uint8)

    img[img == 250] = 255
    img[img == 1] = 0

    for slice_idx_y in range(math.floor(img.shape[0] / slice_fact)):
        for slice_idx_x in range(math.floor(img.shape[1] / slice_fact)):

            slice_num_x = (slice_idx_x * slice_fact) + 1000
            slice_num_y = (slice_idx_y * slice_fact) + 1000

            slice_num_x_last = slice_num_x - slice_fact
            slice_num_y_last = slice_num_y - slice_fact

            img_slice = img[slice_num_y_last:slice_num_y, slice_num_x_last:slice_num_x]

            if img_slice.min() == 0:
                cv2.imshow("test", img_slice)
                cv2.waitKey(0)

"""
img_all = imageio.imread('/media/work/Workspace/staz_OV/napari_test/model_output_test.tif')
out_file = "contour_div.tif"

slices = []
for i in range(img_all.shape[0]):
    img = img_all[i, ...].astype(np.uint8)

"""