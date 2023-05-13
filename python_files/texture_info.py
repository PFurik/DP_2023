import numpy as np

'''
"Lacerta agilis female": 0,
"Lacerta agilis male": 1, green coloring

"Podarcis muralis female": 2,
"Podarcis muralis male": 3, they have more elaborate spot pattern on their belies, irrelevant

"Lacerta viridis female": 4,
"Lacerta viridis male": 5, blue necks

"Zootoca vivipara female": 6,
"Zootoca vivipara male": 7, again belies 

"Podarcis tauricus female": 8,
"Podarcis tauricus male": 9
'''

class Skin_params:
    def __init__(self, species):
        
        self.spot_map = []
        self.do_sin_blob = 1
        self.do_sin_dot = 1
        self.do_erode= 1
        self.do_dilate = 1
        self.rgb = [50, 50, 50] #base body color
        self.rgb_stripes = [255, 0, 0] # does not get randomized in texture shuffle 
        self.rgb_blob = [0, 255, 0]
        self.rgb_dots = [0, 0, 255]

        if species == 0:
            self.rgb = [51, 45, 45]
            self.rgb_stripes = [76,64,53]
            self.rgb_blob = [18,18,18]
            self.rgb_dots = [90,85,85]
            self.size_dots = 20
            self.size_blobs = 28
            self.spot_map = "placeholder.png"
        elif species == 1:
            self.rgb = [50, 65, 23]
            self.rgb_stripes = [76, 64, 53]
            self.rgb_blob = [19, 19, 19]
            self.rgb_dots = [90, 85, 85]
            self.size_dots = 20
            self.size_blobs = 25
            self.spot_map = "placeholder.png"
        elif species == 2:
            self.rgb = [47, 38, 25]
            self.rgb_stripes = [47, 43, 29]
            self.rgb_blob = [19, 19 , 19]
            self.rgb_dots = [75, 70, 60]
            self.size_dots = 10
            self.size_blobs = 15
            self.do_sin_blob = 0
            self.spot_map = "placeholder.png"
        elif species == 3:
            self.rgb = [47, 38, 25]
            self.rgb_stripes = [47, 43, 29]
            self.rgb_blob = [19, 19, 19]
            self.rgb_dots = [75, 70, 60]
            self.size_dots = 20
            self.size_blobs = 50
            self.do_sin_blob = 1
            self.spot_map = "placeholder.png"
        elif species == 4:
            self.rgb = [90, 97, 52]
            self.rgb_stripes = [89, 91, 87]
            self.rgb_blob = [22, 25, 23]
            self.rgb_dots = [88, 98, 62]
            self.size_dots = 5
            self.size_blobs = 1
            self.do_sin_blob = 0
            self.do_sin_dot = 0
            self.do_erode = 0
            self.do_dilate = 0
            self.spot_map = "placeholder.png"
        elif species == 5:
            self.rgb = [90, 97, 52]
            self.rgb_stripes = [0, 75, 89]
            self.rgb_blob = [22, 25, 23]
            self.rgb_dots = [88, 98, 62]
            self.size_dots = 5
            self.size_blobs = 1
            self.do_sin_blob = 0
            self.do_sin_dot = 0
            self.do_erode = 0
            self.do_dilate = 0
            self.spot_map = "placeholder.png"
        elif species == 6:
            self.rgb = [71, 60, 45]
            self.rgb_stripes = [65, 42, 32]
            self.rgb_blob = [14, 12, 9]
            self.rgb_dots = [91, 81, 53]
            self.size_dots = 15
            self.size_blobs = 10
            self.do_sin_blob = 0
            self.do_sin_dot = 0
            self.do_erode = 0
            self.do_dilate = 0
            self.spot_map = "placeholder.png"
        elif species == 7:
            self.rgb = [71, 60, 45]
            self.rgb_stripes = [65, 42, 32]
            self.rgb_blob = [91, 81, 53]
            self.rgb_dots = [14, 12, 9]
            self.size_dots = 15
            self.size_blobs = 10
            self.do_sin_blob = 0
            self.do_sin_dot = 1
            self.spot_map = "placeholder.png"
        elif species == 8:
            self.rgb = [56, 29, 6]
            self.rgb_stripes = [47, 51, 20]
            self.rgb_blob = [3, 3, 2]
            self.rgb_dots = [95, 82, 60]
            self.size_dots = 10
            self.size_blobs = 10
            self.do_sin_blob = 0
            self.do_sin_dot = 0
            self.do_erode = 0
            self.do_dilate = 0
            self.spot_map = "placeholder.png"
        elif species == 9:
            self.rgb = [71, 60, 45]
            self.rgb_stripes = [65, 42, 32]
            self.rgb_blob = [91, 81, 53]
            self.rgb_dots = [14, 12, 9]
            self.size_dots = 15
            self.size_blobs = 10
            self.do_sin_blob = 0
            self.do_sin_dot = 1
            self.spot_map = "placeholder.png"

        self.species_color = [self.rgb, self.rgb_stripes,
                              self.rgb_blob, self.rgb_dots]
        self.shuffle_params = [self.size_blobs, self.size_dots,
                                self.do_sin_blob, self.do_sin_dot, 
                                self.do_dilate, self.do_erode]
        self.species_color = [np.array(x)/100 for x in self.species_color]


    
