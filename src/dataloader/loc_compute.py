import cv2
import numpy as np
from skimage.io import imsave, imread
import os
import numpy as np
import json

#variables
img_data_path = os.getcwd()[:os.getcwd().index("PlzenskyPoharPravdy") + len("PlzenskyPoharPravdy")] + "/data/img_data/"
czech_rep_config_path = os.getcwd()[:os.getcwd().index("PlzenskyPoharPravdy") + len("PlzenskyPoharPravdy")] + "/data/other_data/czech_rep_config.json"
pix_to_m = 100 #taken from data.gov.cz

class MapDataManipulator:
    #
    # function that reads whole files, stores them into RAM and the processes data as web send requests
    #
    def __init__(self):
        self.GRA = None #Grasslands
        self.IBU = None #Concrete places (i am tired :D)
        self.TCD = None #Forests
        self.WAW = None #Water

        #read
        img_path_GRA = os.path.join(img_data_path, "GRA_2018_010m_CR_mod.tif")
        self.GRA = imread(img_path_GRA).astype(np.uint8)

        img_path_IBU = os.path.join(img_data_path, "IBU_2018_010m_CR_mod.tif")
        self.IBU = imread(img_path_IBU).astype(np.uint8)

        img_path_TCD = os.path.join(img_data_path, "TCD_2018_010m_CR_mod.tif")
        self.TCD = imread(img_path_TCD).astype(np.uint8)

        img_path_WAW = os.path.join(img_data_path, "WAW_2018_010m_CR_mod.tif")
        self.WAW = imread(img_path_WAW).astype(np.uint8)

        czech_rep_config = open(czech_rep_config_path)
        self.czech_rep_config_data = json.load(czech_rep_config)

        #compute lat_to_pix and lon_to_pix
        lat_diff = self.czech_rep_config_data["points"][0]["lat"] - self.czech_rep_config_data["points"][1]["lat"]
        lon_diff = self.czech_rep_config_data["points"][3]["lon"] - self.czech_rep_config_data["points"][2]["lon"]

        self.lat_to_pix = self.GRA.shape[0] / lat_diff
        self.lon_to_pix = self.GRA.shape[1] / lon_diff

    def ProcessPoI(self, longitude, latitude, radius):
        # process Point-of-Impact (where the nuke lands)       

        long_diff = longitude - self.czech_rep_config_data["points"][2]["lon"]
        lat_diff = latitude - self.czech_rep_config_data["points"][1]["lat"]

        x_impact = round((self.czech_rep_config_data["points"][2]["lon"] * long_diff) + (self.lon_to_pix * long_diff))
        y_impact = self.GRA.shape[0] - round((self.czech_rep_config_data["points"][1]["lat"] * lat_diff) + (self.lat_to_pix * lat_diff))

        print(x_impact)
        print(y_impact)

        radius = radius * 1000
        pix_radius = round(radius / 100)

        PAD = 500

        crop_x1 = (x_impact - pix_radius) - PAD
        crop_x2 = (x_impact + pix_radius) + PAD

        crop_y1 = (y_impact - pix_radius) - PAD
        crop_y2 = (y_impact + pix_radius) + PAD
        
        #create a mask
        mask_image = np.full(self.GRA[crop_y1:crop_y2, crop_x1: crop_x2].shape, 255, dtype=np.uint8)
        cv2.circle(mask_image, (int(x_impact - crop_x1), int(y_impact - crop_y1)), pix_radius, 0, -1)

        #mask every data image
        #GRA - Grasslands
        result_GRA = cv2.bitwise_and(self.GRA[crop_y1:crop_y2, crop_x1: crop_x2], self.GRA[crop_y1:crop_y2, crop_x1: crop_x2], mask=mask_image) * 255

        #IBU - Concrete places
        result_IBU = cv2.bitwise_and(self.IBU[crop_y1:crop_y2, crop_x1: crop_x2], self.IBU[crop_y1:crop_y2, crop_x1: crop_x2], mask=mask_image) * 255

        #TCD - Forests
        result_TCD = cv2.bitwise_and(self.TCD[crop_y1:crop_y2, crop_x1: crop_x2], self.TCD[crop_y1:crop_y2, crop_x1: crop_x2], mask=mask_image) * 255

        #WAW - Water
        result_WAW = cv2.bitwise_and(self.WAW[crop_y1:crop_y2, crop_x1: crop_x2], self.WAW[crop_y1:crop_y2, crop_x1: crop_x2], mask=mask_image) * 255

        #TODO masking does not work that well

        contours, _ = cv2.findContours(result_GRA, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        max_contour = max(contours, key=cv2.contourArea)
        contours_GRA = [cnt for cnt in contours if cnt is not max_contour]

        contours, _ = cv2.findContours(result_IBU, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        max_contour = max(contours, key=cv2.contourArea)
        contours_IBU = [cnt for cnt in contours if cnt is not max_contour]

        contours, _ = cv2.findContours(result_TCD, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        max_contour = max(contours, key=cv2.contourArea)
        contours_TCD = [cnt for cnt in contours if cnt is not max_contour]

        contours, _ = cv2.findContours(result_WAW, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        max_contour = max(contours, key=cv2.contourArea)
        contours_WAW = [cnt for cnt in contours if cnt is not max_contour]

        area_all_GRA = 0
        area_all_IBU = 0
        area_all_TCD = 0
        area_all_WAW = 0

        for contour in contours_GRA:
            contour_area = round(cv2.contourArea(contour))
            area_all_GRA += contour_area

        for contour in contours_IBU:
            contour_area = round(cv2.contourArea(contour))
            area_all_IBU += contour_area

        for contour in contours_TCD:
            contour_area = round(cv2.contourArea(contour))
            area_all_TCD += contour_area

        for contour in contours_WAW:
            contour_area = round(cv2.contourArea(contour))
            area_all_WAW += contour_area

        #calucate are and convert to km squared
        area_all_GRA = (area_all_GRA * 100 * 100) / 1000000
        area_all_IBU = (area_all_IBU * 100 * 100) / 1000000
        area_all_TCD = (area_all_TCD * 100 * 100) / 1000000
        area_all_WAW = (area_all_WAW * 100 * 100) / 1000000

        return area_all_GRA, area_all_IBU, area_all_TCD, area_all_WAW