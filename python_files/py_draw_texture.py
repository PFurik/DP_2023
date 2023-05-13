import numpy as np
from PIL import Image
import cv2 as cv
import os
import time 
from math import sqrt
from glob import glob
from wand.image import Image as WandImage
from multiprocessing.pool import ThreadPool
from queue import Queue
from functools import partial
from config import Flags
import random as rng


# some kind of blue for segmentation color
color = (255, 50, 25, 255)
color_line_y = (0, 50, 255, 255)
color_line_x = (0, 250, 25, 255)
# number of contours that require separate drawing function
n_draw = 2
#path to file
path = r"textures/lizard_4k.png"
#path = r'brushes/brush1.png'

def cv2PIL(img: np.ndarray):
    #img = cv.cvtColor(img, cv.COLOR_BGRA2RGBA)
    return Image.fromarray(img)

def get_half(minmax: np.array):
    return (minmax[1] - minmax[0])*0.5

def save_image(image: np.array, index = 0, img_type = ".png"):
    save_path = r"C:/Users/student/Desktop/data"
    cv.imwrite(os.path.join(save_path,f'waka{index}{img_type}'),image)   


def show_image(img: np.ndarray, name='Image', scale=1):
    cv.imshow(name, cv.resize(img, (0, 0), fx=scale, fy=scale))
    k = cv.waitKey(0)

def get_masks(image, original):
    #image should be only one compoment image, on of these R,G,B,A
    # original has all of the components
    masks = []
    #find the countours within texture
    contours, hierarchy = cv.findContours(image,
        cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    #get the two biggest ones
    cnt = sorted(contours, key = lambda x: (x.size), reverse= True)
    if len(cnt) > 25:
        print("Warning: Number of contours exceeds 25")
    #create mask for each contour 

    for i, cnt in enumerate(cnt):
        mask = original[:,:,:] * 0
        cv.drawContours(mask, cnt, 0, color, 8)
        cv.fillPoly(mask, pts = [cnt], color=(color))
        masks.append(mask)

    return masks
    

# weight function
def weight_fun(val, min_val, max_val):
    new_val = (val - max_val) / (min_val - max_val) * 1
    p = 1.5
    value = sqrt(((1 + 0.1) - new_val)) * p
    #some parabola that ends around 1 mark, therefore normalize input bewtween 0 and 1
    return value

def find_extremes(A: np.array):
    A_val = []
   # [A_val.append(np.unique(x)) for x in np.nonzero(A[:,:,-1])]
    [A_val.append(x) for x in np.nonzero(A[:,:,0])]
    max_val_y = max(A_val[1])
    min_val_y = min(A_val[1])
    max_val_x = max(A_val[0])
    min_val_x = min(A_val[0])

    # [check_val(x,y,A[x,y]) for x,y in zip(A[0],A[1])]
    return [min_val_x,max_val_x],[min_val_y,max_val_y], A_val


def load_skin(path: str):
    #pick from filenames in path folder, should be pngs
    filenames = sorted(glob(os.path.join(path, '*.dds')))
    # random choice
    choice = rng.randint(0,len(filenames) - 1)
    print(filenames[choice])
    with WandImage(filename=os.path.join(os.getcwd(), filenames[choice])) as img:
        img.compression = "no"
        image = cv.cvtColor(np.asarray(img), cv.COLOR_RGB2BGR)
    #image = Image.open(os.path.join(os.getcwd(), filenames[choice]), 'r')
    
    return image


def init_worker(q: Queue, s: np.ndarray):
    # init global variable for worker inside Process pool
    global queue, skin
    queue = q
    skin = s


def fill_skin(queue: Queue, skin: np.ndarray, mask_list: list,):
    
    idx, mask = mask_list
 
    # find size of mask non zero pixels
    minmax_x, minmax_y, mask_no_zeros = find_extremes(mask)
    # also get only the zero elements
    mask_zeros = np.nonzero(mask[:,:,0] == 0)

    #get size of brush,rectangle ... maybe
    skin_x, skin_y = skin.shape[:2]
    #get indices without zero values, and are one half
    #minmax_x, minmax_y, mask_no_zeros = find_extremes(mask)

    segment_height, segment_width = int(2*get_half(minmax_x)), int(2*get_half(minmax_y))
    if (skin_x < segment_height) or (skin_y <  segment_width):
        #print(f"loaded texture {skin_x} x {skin_y} smaller than one to be replaced {segment_height} x {segment_width} resizing")
        s = segment_height if segment_height > segment_width else segment_width
        skin = cv.resize(skin, (s + 5,s + 5), interpolation=cv.INTER_LANCZOS4)

    mask[minmax_x[0]:minmax_x[1], minmax_y[0]:minmax_y[1], :3] = cv.medianBlur(skin[ 0:segment_height, 0:segment_width], 3)
    #show_image(mask, scale = 0.1)

    mask[mask_zeros[0], mask_zeros[1]] = 0
    # add the mask together to blank image
    #queue.put([mask, idx])

 
    return [idx, mask]


def get_height_map(rgba_image: Image):

    # source https://forums.developer.nvidia.com/t/algorithm-behind-converting-a-diffuse-texture-to-a-normal-texture/203220/2
    #as it turns out the greyscale source image is good estimate for 2d height map, maybe we should just use opencv to conver to greyscale ?
    #rgba_image = np.asarray(rgba_image)
    R, G, B, _ = cv.split(rgba_image)
    #H = np.zeros(rgba_image.shape[:2])
    #H = (R + G + B) // 3
    #test = cv.normalize( rgba_image[:,:,:3], None, 255, 0, cv.NORM_INF)
    H = cv.max(R,cv.max(G,B))
    #H = 255 - (255 - R)*(255 - G)*(255 - B)
    #H = cv.GaussianBlur(H,(3,3),0)
    H = H.astype(dtype = np.uint8)
    
    return H

# a function that takes a vector - three numbers - and normalize it, i.e make it's length = 1


def normalizeRGB(vec):
    length = np.sqrt(vec[:, :, 0]**2 + vec[:, :, 1]**2 + vec[:, :, 2]**2)
    vec[:, :, 0] = vec[:, :, 0] / length
    vec[:, :, 1] = vec[:, :, 1] / length
    vec[:, :, 2] = vec[:, :, 2] / length
    return vec

def gradient(img, dx, dy, ksize):
    
    deriv_filter = cv.getDerivKernels(dx=dx, dy=dy, ksize=ksize, normalize=True)
    return cv.sepFilter2D(img, -1, deriv_filter[0], deriv_filter[1])

def get_normal_map(height_map: np.ndarray, rgba_image: np.ndarray):
    scale = 1
    delta = 0
    ddepth = cv.CV_16S
    grad_x = gradient(height_map, 1, 0, ksize=cv.FILTER_SCHARR)
    #grad_x = cv.Scharr(height_map,ddepth,1,0, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    #grad_x = cv.Sobel(height_map, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    # Gradient-Y
    grad_y = gradient(height_map, 0, 1, cv.FILTER_SCHARR) 
    #grad_y = cv.Scharr(height_map, ddepth, 0, 1, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    #grad_y = cv.Sobel(height_map, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)


    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)
    
    normal_map = np.zeros(rgba_image.shape, dtype = np.uint8)
    normal_map[:,:,3] =  rgba_image[:,:,3]
    zeros = np.where(height_map <= 0)
    #BGR !!!
    normal_map[:,:,0] = 255
    normal_map[:,:,1] = -abs_grad_y
    normal_map[:, :, 2] = -abs_grad_x

    normal_map[:,:,:2]  = 0.5 * normal_map[:,:,:2] + 0.5
    normal_map[:,:,:2] = cv.normalize( normal_map[:,:,:2], None, 0, 1, cv.NORM_MINMAX)
    normal_map[zeros[0],zeros[1],:] = 0
    normal_map[:,:,:2] = normal_map[:,:,:2] * 255
    normal_map = cv.GaussianBlur(normal_map,(3,3),0)
    normal_map = normal_map.astype(dtype=np.uint8)

    return normal_map

def get_specular_map(height_map: np.ndarray, rgba_img: np.ndarray):
    
    gray = cv.cvtColor(rgba_img[:, :, :3], cv.COLOR_BGR2GRAY)
    max_gray_value = np.max(gray)
    around_gray = np.where(gray >= (max_gray_value * 0.95))
    below_grey = np.where(gray <= (max_gray_value * 0.5))
    gray[below_grey[0],below_grey[1]] += int(255*0.1)
    gray[around_gray[0],around_gray[1]] = 255
    gray = gray.astype(dtype= np.uint8)
    specular_map = np.zeros(shape=rgba_img.shape, dtype=np.uint8)
    specular_map[:, :,  3] = rgba_img[:, :, 3]
    specular_map[:, :, 0] = gray
    specular_map[:, :, 1] = gray
    specular_map[:, :, 2] = gray
    #specular_map = cv.GaussianBlur(specular_map,(3,3),0)
    specular_map = specular_map.astype(dtype= np.uint8)

    return specular_map

def get_new_skin(skins_queue: Queue, o_texture: np.ndarray, number_of_cycles: int, flags: Flags):

    #called from simulator for new textures
    image = np.asarray(o_texture) 
    #get the alpha channel
    image_split = cv.split(image) #RGBA
    alpha = image_split[3] # Alpha
    alpha = cv.medianBlur(alpha, 11) # blur any small holes
    masks = get_masks(alpha, image)

    workers = 3
    Pool = ThreadPool(workers)
 
    for cycle in range(1,number_of_cycles):

        if not flags.run_flag:
            # if interrupt from mainloop try to break
            break
        start = time.time()
        new_image = np.zeros(image.shape, dtype=np.uint8)

        #pick a brush
        skin = load_skin(r'drawn_textures')
        queue = Queue()
        q = partial(fill_skin, queue, skin)


        if len(masks) > 2:
            ## spread accross Pool
            result = Pool.map(q, [[idx, mask] for idx, mask in enumerate(masks)])
        else:
            #get the patches from output texture
            result = [q([idx, mask]) for idx, mask in enumerate(masks)]
        
        end = time.time()
        print(f"new skin generated in {end - start} seconds")
            
        #add those masks together to form original image with different texture
        for val in result:
            idx, mask = val
            new_image += mask
        
        height_map = get_height_map(new_image)
        normal_map = get_normal_map(height_map, new_image)
        specular_map = get_specular_map(height_map,new_image)
        normal_map = cv2PIL(normal_map)
        specular_map = cv2PIL( specular_map )
        #so far we only paint on greyscale image 
        BGR = cv.cvtColor(new_image[:,:,:3], cv.COLOR_BGR2GRAY)
        new_image[:,:,0] = BGR
        new_image[:,:,1] = BGR
        new_image[:,:,2] = BGR
        new_image = Image.fromarray(new_image)
        
        skins_queue.put([new_image, normal_map, specular_map])


def get_new_skin_main( o_texture: np.ndarray):

    #used for testing in this file by main function
    image = np.asarray(o_texture)
    # get the alpha channel
    image_split = cv.split(image)  # RGBA
    alpha = image_split[3]  # Alpha
    alpha = cv.medianBlur(alpha, 11)  # blur any small holes
    masks = get_masks(alpha, image)

    workers = 5
    Pool = ThreadPool(workers)


    start = time.time()
    new_image = np.zeros(image.shape, dtype=np.uint8)
  

    # pick a brush
    skin = load_skin(r'drawn_textures')
    queue = Queue()
    q = partial(fill_skin, queue, skin)

    if len(masks) > 2:
        # spread accross Pool
        result = Pool.map(q, [[idx, mask]
                            for idx, mask in enumerate(masks)])
    else:
        # get the patches from output texture
        result = [q([idx, mask]) for idx, mask in enumerate(masks)]

    end = time.time()
    print(f"new skin generated in {end - start} seconds")

    # add those masks together to form original image with different texture
    for val in result:
        idx, mask = val
        new_image += mask

    # so far we only paint on greyscale image
    new_image[:, : ,3] = alpha

    height_map = get_height_map(new_image)
    normal_map = get_normal_map(height_map, new_image)
    specular_map = get_specular_map(height_map,new_image)
    
    BGR = cv.cvtColor(new_image[:, :, :3], cv.COLOR_BGR2GRAY)
    new_image[:, :, 0] = BGR
    new_image[:, :, 1] = BGR
    new_image[:, :, 2] = BGR
    maps = np.concatenate((new_image,normal_map,specular_map), 1, dtype=np.uint8)
    save_image(maps,'all')
    new_image = Image.fromarray(new_image)

    return new_image


def main():
    #PIL has rgb format 
    image = Image.open(path)
    image = np.asarray(image)
    get_new_skin_main(image)


if __name__ == '__main__':
    main()
