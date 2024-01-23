import cv2
import numpy as np
from skimage.io import imsave, imread
import os
import numpy as np
import json

#variables
main_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
img_data_path = os.path.join(main_dir,"data/img_data/")
czech_rep_config_path = os.path.join(main_dir, "data/other_data/czech_rep_config.json")
pix_to_m = 100 #taken from data.gov.cz
threshold_value = 150

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

        radius = radius * 1000
        pix_radius = round(radius / 100)

        PAD = 500

        crop_x1 = (x_impact - pix_radius) - PAD
        crop_x2 = (x_impact + pix_radius) + PAD

        crop_y1 = (y_impact - pix_radius) - PAD
        crop_y2 = (y_impact + pix_radius) + PAD
        
        result_GRA = self.GRA[crop_y1:crop_y2, crop_x1:crop_x2]
        result_IBU = self.IBU[crop_y1:crop_y2, crop_x1:crop_x2]
        result_TCD = self.TCD[crop_y1:crop_y2, crop_x1:crop_x2]
        result_WAW = self.WAW[crop_y1:crop_y2, crop_x1:crop_x2]

        binary_image = np.where(result_GRA < threshold_value, 0, 255).astype(np.uint8)
        result_GRA = binary_image
        binary_image = np.where(result_IBU < threshold_value, 0, 255).astype(np.uint8)
        result_IBU = binary_image
        binary_image = np.where(result_TCD < threshold_value, 0, 255).astype(np.uint8)
        result_TCD = binary_image
        binary_image = np.where(result_WAW < threshold_value, 0, 255).astype(np.uint8)
        result_WAW = binary_image

        area_all_GRA = np.sum(result_GRA == 0) 
        area_all_IBU = np.sum(result_IBU == 0) 
        area_all_TCD = np.sum(result_TCD == 0) 
        area_all_WAW = np.sum(result_WAW == 0) 

        #calucate are and convert to km squared
        area_all_GRA = (area_all_GRA * 100 * 100) / 1000000
        area_all_IBU = (area_all_IBU * 100 * 100) / 1000000
        area_all_TCD = (area_all_TCD * 100 * 100) / 1000000
        area_all_WAW = (area_all_WAW * 100 * 100) / 1000000

        return area_all_GRA, area_all_IBU, area_all_TCD, area_all_WAW