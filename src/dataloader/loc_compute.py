import cv2
import numpy as np
from skimage.io import imsave, imread
import os
import numpy as np
import json

#variables
img_data_path = os.getcwd()[:os.getcwd().index("PlzenskyPoharPravdy") + len("PlzenskyPoharPravdy")] + "/data/img_data/"
czech_rep_config_path = os.getcwd()[:os.getcwd().index("PlzenskyPoharPravdy") + len("PlzenskyPoharPravdy")] + "/data/other_data/czech_rep_config.json"

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
        lon_diff = self.czech_rep_config_data["points"][2]["lon"] - self.czech_rep_config_data["points"][3]["lon"]

        self.lat_to_pix = self.GRA.shape[0] / lat_diff
        self.lon_to_pix = self.GRA.shape[1] / lon_diff

    def ProcessPoI(self, longitude, latitude):
        # process Point-of-Impact (where the nuke lands)       

        long_diff = (latitude - self.czech_rep_config_data["points"][2]["lon"])
        lat_diff = (longitude - self.czech_rep_config_data["points"][0]["lat"])

        print(long_diff)
        print(lat_diff)

        x_impact = round(self.lon_to_pix * long_diff)
        y_impact = round(self.lat_to_pix * lat_diff)
        print(x_impact)
        print(y_impact)

