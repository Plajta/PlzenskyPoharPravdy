import cv2
import numpy as np
from skimage.io import imsave, imread
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
    if filename == "README.txt":
        continue
    abs_path = os.path.join(img_data_path, filename)
    img = imread(abs_path).astype(np.uint8)

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

def normalize_and_modify():
    #
    # Get image cropping data
    #
    img_path = os.path.join(img_data_path, "TCD_2018_010m_CR.tif")
    img = imread(img_path).astype(np.uint8)

    for slice_idx_y in range(math.floor(img.shape[0] / slice_fact)):
        for slice_idx_x in range(math.floor(img.shape[1] / slice_fact)):

            slice_num_x = (slice_idx_x * slice_fact) + 1000
            slice_num_y = (slice_idx_y * slice_fact) + 1000

            slice_num_x_last = slice_num_x - slice_fact
            slice_num_y_last = slice_num_y - slice_fact

            threshold_value = 150
            binary_image = np.where(img[slice_num_y_last:slice_num_y, slice_num_x_last:slice_num_x] < threshold_value, 0, 255).astype(np.uint8)
            img[slice_num_y_last:slice_num_y, slice_num_x_last:slice_num_x] = binary_image

            #cv2.imshow("test", img[slice_num_y_last:slice_num_y, slice_num_x_last:slice_num_x])
            #cv2.waitKey(0)

    new_pix = 1000
    r = new_pix / img.shape[1]
    dim = (new_pix, int(img.shape[0] * r))

    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    contours, _ = cv2.findContours(resized, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=cv2.contourArea)
    filtered_contours = [cnt for cnt in contours if cnt is not max_contour]

    contour_data = []
    for contour in filtered_contours:
        extLeft = tuple(contour[contour[:, :, 0].argmin()][0])[0]
        extRight = tuple(contour[contour[:, :, 0].argmax()][0])[0]
        extTop = tuple(contour[contour[:, :, 1].argmin()][0])[1]
        extBot = tuple(contour[contour[:, :, 1].argmax()][0])[1]
        contour_data.append([extLeft, extRight, extTop, extBot])
        
    np_cnt_data = np.array(contour_data)

    leftmost = round((np_cnt_data[:, 0].min() / resized.shape[0]) * img.shape[0])
    rightmost = round((np_cnt_data[:, 1].max() / resized.shape[0]) * img.shape[0])
    topmost = round((np_cnt_data[:, 2].min() / resized.shape[1]) * img.shape[1])
    botmost = round((np_cnt_data[:, 3].max() / resized.shape[1]) * img.shape[1])

    #cropped_img = img[topmost:botmost, leftmost:rightmost]
    #imsave("test.tif", cropped_img)
    #exit()

    for filename in os.listdir(img_data_path):
        if filename == "README.txt" and ".gitkeep":
            continue
        abs_path = os.path.join(img_data_path, filename)
        img = imread(abs_path).astype(np.uint8)

        cropped_img = img[topmost:botmost, leftmost:rightmost]
        imsave(abs_path.replace(".tif", "_mod.tif"), cropped_img)
        #saving modified files which are binary and fixed size

if __name__ == "__main__":
    normalize_and_modify()