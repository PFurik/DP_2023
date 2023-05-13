import cv2 as cv
import numpy as np
from time import strftime
from os import path
from copy import deepcopy
import config

def set_globals():
    global PARTIONS
    global SAVE_PATH
    global IMG_TYPE
    SAVE_PATH = config.SAVE_PATH
    IMG_TYPE = config.IMG_TYPE
    PARTIONS = config.PARTIONS


PARTIONS = config.PARTIONS
PATH = config.PARTIONS
IMG_TYPE = config.IMG_TYPE

class ScreenShotBuffer:
    def __init__(self) -> None:
        #self.img_data = []
        self.species_data = []


class ImageGenerator():
    def __init__(self, image_list: list[np.array], status) -> None:
        
        status.setText("Saving images")
        set_globals()
        # certain part of frame
        self.skip = 0 # height/PARTIONS

        self.height, self.width, self.rgba = image_list[0].shape
        self.skip = self.height//PARTIONS
        self.low_range_x = 0
        self.upper_range_x = self.width
        self.low_range_y = 0
        self.upper_range_y = self.skip
        self.deformed_img = []
        self.base_img = []
        self.first_image = True
        self.path = SAVE_PATH
        self.img_type = IMG_TYPE

      
    def buffer_loop(self, image_list: list[np.array], status):
        for i, image in enumerate(image_list):
            partioned_img = self.partion_img(image)
            if not i % 2: #every base image
                self.save_images(partioned_img, "b", i)
            else:
                self.save_images(partioned_img, "d", i)
        status.setText("Done")
        

    def save_images(self, image_list: list[np.array], type:str, i:int):
        for j, image in enumerate(image_list):
            filename = self.get_filename(f"{type}{j}{i}")
            self.write2file(filename, image)


    def partion_frames(self, img_data: np.array, iter: int):

        insert = img_data[iter]*0
        self.deformed_img.index(iter, insert)

    def partion_img(self, img_data: np.array):
        
        new_data = []
        for i in range(PARTIONS):
            partion = img_data[self.low_range_y: self.upper_range_y,
                            self.low_range_x: self.upper_range_x]
            self.low_range_y += self.skip
            self.upper_range_y += self.skip
            new = deepcopy(partion)
            new_data.append(new)

        self.low_range_x = 0
        self.upper_range_x = self.width
        self.low_range_y = 0
        self.upper_range_y = self.skip
        return new_data
  
    
    def write2file(self, filename: str, img_data: np.array):
        #The sacrifices we make for non ASCII characters cv.imread,write has issues with them
        # pillow uses BGR or is Opencv ??
        img_data = cv.cvtColor(img_data, cv.COLOR_BGRA2RGB)
        #encode into .jpg, png ...
        succes, img_buffered = cv.imencode(self.img_type, img_data)
        if not succes:
            print("OpenCV couldn't encode file to: ", self.img_type)
        test = path.join(self.path,filename)
        try:
            with open(test, mode="w", encoding="utf-8") as fp: 
                #create file if it doesn't exist, also utf-8
                pass
            img_buffered.tofile(test)
        except:
            print("file or directories in path don't exist")

            

    def get_filename(self,  name: str):
        timestr = strftime("%d %m %Y-%H-%M-%S")
        filename = r"{}-{}{}".format(name, timestr, self.img_type)
        return filename


    def pop_buffer(self,buffer: ScreenShotBuffer, index):
        to_return = buffer.species_data[0]
        del buffer.species_data[0]
        return to_return


