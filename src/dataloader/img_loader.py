import cv2
import imageio
import numpy as np
from skimage.io import imsave
import os
import numpy as np
import math

img_data_path = os.getcwd()[:os.getcwd().index("PlzenskyPoharPravdy") + len("PlzenskyPoharPravdy")] + "/data/img_data/"
slice_fact = 1000

#
# FOR VISUALISATION
#
"""
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
                contours, _ = cv2.findContours(img_slice, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                max_contour = max(contours, key=cv2.contourArea)
                filtered_contours = [cnt for cnt in contours if cnt is not max_contour]

                #testing
                contour_image = np.zeros((img_slice.shape[0], img_slice.shape[1], 3), dtype=np.uint8)

                approx_contours = []

                eps = 0.001
                for contour in filtered_contours:
                    peri = cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, eps * peri, True)
                    approx_contours.append(approx)

                cv2.drawContours(contour_image, approx_contours, -1, (0, 255, 0), 2)  # -1: Draw all contours

                cv2.imshow("test", img_slice)
                cv2.imshow("contour", contour_image)
                cv2.waitKey(0)
"""

#
# Get image cropping data
#
img_path = os.path.join(img_data_path, "TCD_2018_010m_CR.tif")
img = imageio.imread(img_path).astype(np.uint8)

new_pix = 1000
r = new_pix / img.shape[1]
dim = (new_pix, int(img.shape[0] * r))

resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

threshold_value = 150
binary_image = np.where(resized < threshold_value, 0, 255).astype(np.uint8)

coordinates = np.column_stack(np.where(binary_image == 0))
leftmost = tuple(coordinates[0])[0]
rightmost = tuple(coordinates[-1])[0]
topmost = tuple(np.min(coordinates, axis=0))[1]
botmost = tuple(np.max(coordinates, axis=0))[1]

cropped_img = img[leftmost:rightmost, topmost:botmost]
print(cropped_img.shape)

#TODO: does not seem to work, showing too small pixels
threshold_value = 150
cropped_img = np.where(cropped_img < threshold_value, 0, 255).astype(np.uint8)

print(cropped_img.dtype)
print(img.dtype)

imsave("test.tif", np.array(cropped_img).astype(np.uint8))
exit()

cv2.imshow("test", cropped_img)
cv2.waitKey(0)

for filename in os.listdir(img_data_path):
    if filename == ".gitkeep":
        continue
    abs_path = os.path.join(img_data_path, filename)
    img = imageio.imread(abs_path).astype(np.uint8)

    img[img >= 250] = 255
    img[img < 150] = 0

    new_pix = 1000
    r = new_pix / img.shape[1]
    dim = (new_pix, int(img.shape[0] * r))

    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    cv2.imshow("test", resized)
    cv2.waitKey(0)