#USE .ini file instead for making changes !!!
# RESOLUTION
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
# BREATH VARIABLES
BREATH_HALF_PERIOD = 25
BREATH_HALF_PERIOD_RANDOMIZE = False
NUMBER_OF_PERIODS = 3
NUMBER_OF_PERIODS_RANDOMIZE = False
BREATH_VOLUME = 1  # 1 = 100%
BREATH_VOLUME_RANDOMIZE = False
PER_FRAME_INCREMENT = 1
PER_FRAME_INCREMENT_RANDOMIZE = False
PARTIONS = 3  # how many partions from one image
SAVE_PATH = r"C:/Users/student/Desktop/data"
IMG_TYPE = '.png'
SPECIES_IN_ROTATION = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
NUMBER_OF_CYCLES = 1

#ANIMATION PARAMETERS
#Breath volume adjustment parameters
BREATH_VOLUME_MAX = BREATH_VOLUME
ORIGINAL_BREATH_VOLUME_MIN = -0.35
BREATH_VOLUME_MIN = -0.35
FULL_BREATH = 0
EXHALE_INCREMENT = PER_FRAME_INCREMENT #* 1.75
INHALE_INCREMENT = PER_FRAME_INCREMENT #* 0.75
#interpolation variables for animation, cubic bezier has 2 inbetween points, 
# but we calculate third as the "middle " between the two
MIDDLE_POINT_CHANGE = 0.5
FIRST_POINT_CHANGE = -0.25
SECOND_POINT_CHANGE = 0.65

#POSTPROCESSING
#gaussian noise kernel size
POSPROCESSING_KERNEL_SIZE = 11
POSPROCESSING_CONTOUR_KERNEL_SIZE = 51
#random noise standart deviation and mean
POSPROCESSING_STD_DEVIATION = 30
POSPROCESSING_MEAN = 0


#FLAGS
# Should we try to run on multiple threads 
USE_THREADS_FLAG = True
# some load_mask has cython variant
USE_CYTHON_FLAG = True
#hide window glfw
HIDE_WINDOW_FLAG = True
#hide cursor for glfw window
DISABLE_CURSOR_FLAG = True
# render to invisible framebuffer, can render larger than monitor image
RENDER2FBO_FLAG = False
# tell Generator_thread to save images or just pop the queue
SAVE_IMAGES_FLAG = True
#use postprocessing in Screen_capture
USE_POSTPROCESSING_FLAG = True

class Flags:
    def __init__(self):
        # Should we try to run on multiple threads 
        self.use_threads_flag = USE_THREADS_FLAG
        # finished with single species breathing animation
        self.period_flag = False
        # ran through every species in cycle,
        self.cycle_flag = False
        # maniloop variable
        self.pause_flag = False
        # maniloop variable
        self.continue_flag = False
        # maniloop variable
        self.quit_flag = False
        # maniloop variable
        self.run_flag = False
        #finished simulating
        self.done_flag = False
        # some load_mask has cython variant
        self.use_cython = USE_CYTHON_FLAG
        #hide window glfw
        self.hide_window_flag = HIDE_WINDOW_FLAG
        #hide cursor for glfw window
        self.disable_cursor_flag = DISABLE_CURSOR_FLAG
        # render to invisible framebuffer, can render larger than monitor image
        self.render2fbo_flag = RENDER2FBO_FLAG
        # we just overriden every line in deformed image reaching it's end
        self.lines_full_flag = False
        # we are at first frame 
        self.first_frame_flag = True
        # we are currently at last frame before new period starts
        self.last_frame_flag = False
        ''' 
        Used by rendered to to tell the screen cap what to do, screen_cap_flag
        0 - scan line, regular behavior capture single line
        1 - first frame, whole screen capture
        2 - cycle frame, whole screen capture
        3 - period frame, whole screen capture
        4 - last frame capture the rest of the screen 
        ''' 
        self.screen_cap_flag = 1
        # tell Generator_thread to save images or just pop the queue
        self.save_images_flag = SAVE_IMAGES_FLAG
        #use postprocessing in Screen_capture
        self.use_postprocessing_flag = USE_POSTPROCESSING_FLAG

