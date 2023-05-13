import cv2 as cv
import numpy as np
from os import path
from copy import deepcopy
import config
from queue import Queue as Buff_queue
from time import sleep as time_sleep
from time import time

#I/O for saving screenshots, started in main App GUi

class ScreenShotBuffer:
    def __init__(self) -> None:
        #self.img_data = []
        self.species_data = []


class ImageGenerator():
    def __init__(self, status) -> None:
        
        status.setText("Saving images")
        #set_globals()
        # certain part of frame
        self.skip = 0 # height/PARTIONS
        self.count = 0
    
        #self.deformed_img = []
        #self.base_img = []
        #self.first_image = True
        self.path = config.SAVE_PATH
        self.img_type = config.IMG_TYPE

      
    def buffer_loop(self, queue: Buff_queue, status, state, flags: config.Flags):
        start_time = time()
        while (state.running) or (not queue.empty()):
        
            if queue.empty():
                #print("sleeping")
                time_sleep(1)
            else:

                image = queue.get()
                if not flags.save_images_flag:
                    continue
                
                self.height, self.width, self.rgba = image.shape
                self.skip = self.height//config.PARTIONS
                self.low_range_x = 0
                self.upper_range_x = self.width
                self.low_range_y = 0
                self.upper_range_y = self.skip

                partioned_img = self.partion_img(image)
                
                if not self.count % 2: #every base image
                    self.save_images(partioned_img, "b", self.count)
                else:
                    self.save_images(partioned_img, "d", self.count)

                self.count += 1
                print("image saved on disk")

        end_time = time()
        queue.task_done()
        status.setText(f"Done, time elapsed: {round((end_time - start_time),3)} seconds")
        
            

    def save_images(self, image_list: list[np.array], type:str, count:int):
        for partion, image in enumerate(image_list):
      
            filename = self.get_filename(f"{count}_{partion}_{type}_")
            self.write2file(filename, image)


    def partion_frames(self, img_data: np.array, iter: int):

        insert = img_data[iter]*0
        self.deformed_img.index(iter, insert)

    def partion_img(self, img_data: np.array):
        
        new_data = []
        for i in range(config.PARTIONS):
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
        #timestr = strftime("%d %m %Y-%H-%M-%S")
        
        add_str = r"HP{}_NP{}_BV{}_PI{}_P{}_NC{}_".format(
            config.BREATH_HALF_PERIOD,
            config.NUMBER_OF_PERIODS,
            int(config.BREATH_VOLUME),
            int(config.PER_FRAME_INCREMENT * 100),
            config.PARTIONS,
            config.NUMBER_OF_CYCLES
            )
            # HP
            # NP
            # BV
            # PI
            # P
            # NC
        filename = r"{}{}{}".format(name, add_str, self.img_type)
        return filename


    def pop_buffer(self,buffer: ScreenShotBuffer, index):
        to_return = buffer.species_data[0]
        del buffer.species_data[0]
        return to_return


