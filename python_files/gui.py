from sys import exit as sys_exit
from functools import partial
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, 
                             QWidget, QVBoxLayout,
                             QPushButton, QCheckBox, QComboBox,
                             QSpinBox, QLabel, QListWidget, QAbstractItemView,
                             QTabWidget, QListWidgetItem, QLineEdit,
                            )
from PySide6.QtGui import QPalette, QColor, QBrush
from PySide6.QtTest import QTest
import configparser
import config
from Simulator import Breathing_simulator
from Generator_thread import ImageGenerator
from codecs import open as codecs_open

from threading import Thread
from queue import Queue as Buff_queue
from time import sleep as time_sleep



WINDOW_SIZE = [420,500]
resolutions = [
    [2560,	1600],
    [2048,	1536],
    [2560,	1440],
    [3440,	1440],
    [1920,	1200],
    [2048,	1152],
    [1920,	1080],
    [2560,	1080],
    [1680,	1050],
    [1280,	1024],
    [1440,	900],
    [1600,	900],
    [1536,	864],
    [1280,	800],
    [1024,	768],
    [1360,	768],
    [1366,	768],
    [1280,	720],
    [800,	600],
    [640,   480],
    [640,	360]

]
img_types = ['.png','.jpg', '.bmp', '.exr'

]

def task(i: int):
    print(f'Starting a task {i}...')
    time_sleep(1)
    print(f'done {i}')

class QT_app(QApplication):

    def __init__(self, argv):
        super(QT_app, self).__init__(argv)
        self.state = Simulation_running()
        
    def run_generator(self, window):
        # task(1)
        # new_task = Thread(target=task(2))
        # new_task.start()
        # new_task.join()
        self.state.start()
        status = window.get_features()[0][0]
        
        # #create buffer for our images
        self.buffer_queue = Buff_queue()
        # # RUN GENERATOR
        self.App = Breathing_simulator(status)
        # # PROCESS IMAGES
        # #images = self.App.screen_capture.full_img
        Screenshot_generator = ImageGenerator(status)
        # #Screenshot_generator.buffer_loop(self.buffer_queue, status)
        generator_thread = Thread(target=Screenshot_generator.buffer_loop, args=(self.buffer_queue, status, self.state, self.App.flags))
        generator_thread.start()
        self.App.mainLoop(status, self.buffer_queue, self.state)
        generator_thread.join()


    def quit_app(self, window) -> int:
        if self.state.running == False:
            return 0 
        status = window.get_features()[0][0]
        self.App.flags.run_flag = False
        return self.App.quit(status, self.state)
    
class Simulation_running():
    def __init__(self):
        self.running = False

    def stop(self):
        self.running = False

    def start(self):
        self.running = True


class MainWindow(QMainWindow):

    def __init__(self, filename: str, app: QT_app):
        super(MainWindow, self).__init__()
        self.Settings = self.App_Settings(filename)
        self.setWindowTitle("Some Type of Image Generator")
        self.setFixedSize(QSize(*WINDOW_SIZE))
        self.run_app = False
        self.Qt_app = app

        self.all_features = []

        features_save = [
            Title("Number of strips from single image", pos='b'),
            ValueBox(10, self.Settings.file_locations,
                     self.Settings.partions),
            Title("Save images to this location",pos='b'),
            Line_input(self.Settings.file_locations, self.Settings.generate_to),
            Title("Image type", pos='b'),
            Img_type_box(img_types, self.Settings.file_locations,
                         self.Settings.img_type),
            Button("Save settings", self.Settings.config, self.Settings.variables)

        ]

        features_execution = [
            Title('Status', pos='b'),
            Button("Run", [self.Settings.resolution,
                           self.Settings.breath_variable,
                           self.Settings.file_locations,
                           self.Settings.species,
                           self.Settings.species_include,
                           self.Settings.run_settings,
                           self.Settings.animation_params,
                           self.Settings.postprocessing,
                           self.Settings.flags], self),
            Button("Quit", self),
            Title('Number of cycles, i.e. how many times we run through selected species', pos='b'),
            ValueBox(100, self.Settings.run_settings,
                     self.Settings.number_of_cycles),
            
        ]

        features_species = [
            List(self.Settings.species, self.Settings.species_include),
            Button("Save settings", self.Settings.config, self.Settings.variables)

        ]
        features = [
            Title("Resolution", pos='b'),
            Box(resolutions, self.Settings.resolution,
                 [self.Settings.image_width, self.Settings.image_height]),
            Title("Breath half period, max 1000", pos='b'),
            ValueBox(1000, self.Settings.breath_variable, 
                     self.Settings.breath_half_period),
            CheckBox(self.Settings.breath_variable,
                     self.Settings.breath_half_period_randomize),
            Title("Number of half breath periods, max 100", pos='b'),
            ValueBox(100, self.Settings.breath_variable, 
                     self.Settings.number_of_periods),
            CheckBox(self.Settings.breath_variable, 
                     self.Settings.number_of_periods_randomize),
            Title("Breath volume, percentage, max 100",pos='b'),
            ValueBox(100, self.Settings.breath_variable,
                     self.Settings.breath_volume),
            CheckBox(self.Settings.breath_variable,
                     self.Settings.breath_volume_randomize),
            Title("Breath increment per frame, max 100",pos='b'),
            ValueBox(100, self.Settings.breath_variable,
                     self.Settings.per_frame_increment),
            CheckBox(self.Settings.breath_variable,
                     self.Settings.per_frame_increment_randomize),
            Button("Save settings",self.Settings.config,self.Settings.variables)
        ]

        self.all_features = [
                        features_execution,
                        features_species,
                        features,
                        features_save
        ]

        layout1 = QVBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        layout4 = QVBoxLayout()
        layout1.setContentsMargins(35, 5, 35, 35)
        layout2.setContentsMargins(35, 25, 35, 35)
        layout3.setContentsMargins(100, 50, 100, 100)
        layout4.setContentsMargins(25, 100, 25, 35)
        layout1.setSpacing(0)      
        layout2.setSpacing(20)  
        layout3.setSpacing(50)
        layout4.setSpacing(25)

        for x in features_species:
            layout2.addWidget(x)
        for x in features:
            layout1.addWidget(x)
        for x in features_execution:
            layout3.addWidget(x)
        for x in features_save:
            layout4.addWidget(x)
    
        widget1 = QWidget()
        widget2 = QWidget()
        widget3 = QWidget()
        widget4 = QWidget()
        widget1.setLayout(layout1)
        widget2.setLayout(layout2)
        widget3.setLayout(layout3)
        widget4.setLayout(layout4)

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.TabPosition.North)
        tabs.addTab(widget1, "Settings")
        tabs.addTab(widget2, "Species")
        tabs.addTab(widget4, "Save location")
        tabs.addTab(widget3, "Execute")

        self.setCentralWidget(tabs)

    def get_features(self):
            return self.all_features
    
    class App_Settings():

        def __init__(self, filename):
            config, var_list = self.load_ini(filename)
            self.config = config
            # self.variables = var_list[0] + var_list[1]  + var_list[2]
            # self.new_variables = var_list[0] + var_list[1] + var_list[2]
            self.variables = var_list
            self.resolution = var_list[0]
            self.breath_variable = var_list[1]
            self.file_locations = var_list[2]
            self.species = var_list[3]
            self.species_include = var_list[4]
            self.run_settings = var_list[5]
            self.animation_params = var_list[6]
            self.postprocessing = var_list[7]
            self.flags = var_list[8]

            #indices in above lists
            self.image_width = 0
            self.image_height = 1
            self.breath_half_period = 0
            self.breath_half_period_randomize = 1
            self.number_of_periods = 2
            self.number_of_periods_randomize = 3
            self.breath_volume = 4
            self.breath_volume_randomize = 5
            self.per_frame_increment = 6
            self.per_frame_increment_randomize = 7
            self.partions = 0
            self.generate_to = 1
            self.img_type = 2
            self.number_of_cycles = 0
            ###### THE REST 


        def load_ini(self, filename):
            path = f"settings/{filename}"
            config = Configuration(path)
            config.read(path, encoding="utf8")

            sections_check = [
                            'RESOLUTION',
                            'BREATH VARIABLES',
                            'FILE LOCATIONS',
                            'SPECIES',
                            'INCLUDE SPECIES',
                            'RUN SETTINGS',
                            'ANIMATION PARAMETERS',
                            'POSTPROCESSING',
                            'FLAGS'
                            ]
            variables_check = [
                ['image_width', 'image_height'
                 
                ],
                ['breath_half_period',
                'breath_half_period_randomize',
                'number_of_periods',
                'number_of_periods_randomize',
                'breath_volume',
                'breath_volume_randomize',
                'per_frame_increment',
                'per_frame_increment_randomize',
                

                ],
                ['partions', 'generate_to', 'img_type',
                 
                ],
                ['species0', 'species1',
                 'species2', 'species3',
                 'species4', 'species5',
                 'species6', 'species7',
                 'species8', 'species9',
                 
                ],
                ['include0', 'include1',
                 'include2', 'include3',
                 'include4', 'include5',
                 'include6', 'include7',
                 'include8', 'include9',
                
                ],
                ['number_of_cycles'],
                [
                'breath_volume_max', 
                'original_breath_volume_min',
                'breath_volume_min', 
                'exhale_increment', 
                'inhale_increment', 
                'middle_point_change',
                'first_point_change', 
                'second_point_change' 

                ],
                [
                'posprocessing_kernel_size',
                'posprocessing_contour_kernel_size',
                'posprocessing_std_deviation',
                'posprocessing_mean' 

                ],
                [
                'use_threads_flag', 
                'use_cython_flag', 
                'hide_window_flag',
                'disable_cursor_flag',
                'render2fbo_flag',
                'save_images_flag',
                'use_postprocessing_flag'
                ],


            ]
            
            variables = []
            resolution=[]
            breat_variable= []
            file_locations= []
            list_species = []
            list_include_species = []
            run_settings = []
            animation_params = []
            postprocessing = []
            flags = []

            complete = True
            for i, section in enumerate(config.sections()):
                if section != sections_check[i]:
                    print("Settings section %s missing" % (section))
                    complete = False
                    break
                else:
                    for j, variable in enumerate(config.items(section)):
                        if variable[0] != variables_check[i][j]:
                            print("Settings section %s missing variable %s." %
                                (section, variable))
                            complete = False
                            break
                        else:
                            if section == 'RESOLUTION':
                                resolution.append(variable[1])
                            elif section == 'BREATH VARIABLES':
                                breat_variable.append(variable[1])
                            elif section == 'RUN SETTINGS':
                                run_settings.append(variable[1])
                            elif section == 'FILE LOCATIONS':
                                file_locations.append(variable[1])
                            elif section == 'SPECIES':
                                list_species.append(variable[1])
                            elif section == 'INCLUDE SPECIES':
                                list_include_species.append(variable[1])
                            elif section == 'ANIMATION PARAMETERS':
                                animation_params.append(variable[1])
                            elif section == 'POSTPROCESSING':
                                postprocessing.append(variable[1])
                            elif section == 'FLAGS':
                                flags.append(variable[1])
                            else:
                                variables.append(variable[1])

            if complete == True:
                return config, [
                    resolution,
                    breat_variable,
                    file_locations,
                    list_species,
                    list_include_species,
                    run_settings,
                    animation_params,
                    postprocessing,
                    flags
                    ]
            else:
                return None, None, None


class Img_type_box(QComboBox):
    def __init__(self, img_types: list[str], settings, idx):
        super(Img_type_box, self).__init__()
        
        self.addItems(img_types)
        self.setCurrentText(settings[idx])

        self.currentIndexChanged.connect(
            partial(self.update_value, settings, idx))

    def update_value(self, bind, bind_index, curr_idx):
        bind[bind_index] = img_types[curr_idx]



class Line_input(QLineEdit):
    def __init__(self, settings, idx):
        super(Line_input, self).__init__()
        self.setText(settings[idx])
        self.textChanged.connect(partial(self.update, settings, idx))
    def update(self, settings, bind_idx, curr_idx):
        settings[bind_idx] = self.text()

    #  self.currentIndexChanged.connect(
    #         partial(self.update_value, settings, idx))

      

class List(QListWidget):
    def __init__(self, items, include = None):
        super(List, self).__init__()
        #self.addItems(items)
        self.mouse_pressed = False
            
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        for idx, item in enumerate(items):
            item = QListWidgetItem(item)
            self.addItem(item)
            if include[idx] == 'True':
                self.setCurrentItem(item)
                item.setForeground(QBrush(QColor("red")))
            else:
                item.setForeground(QBrush(QColor("gray")))
        #temporary solution for double click on the same item
        last_item = QListWidgetItem('')
        self.addItem(last_item)
        
        self.setCurrentItem(last_item)

        self.currentTextChanged.connect(partial(self.update_value, items, include))

    def update_value(self, items: list[str], include, item):
        if item == '':
            pass
        else:
            test = self.findItems(item, Qt.MatchFlag.MatchExactly)
            empty = self.findItems('', Qt.MatchFlag.MatchExactly)
            #self.mouse_pressed = True
            idx = items.index(item)
        
            if include[idx] == 'False':
                include[idx] = 'True'
                for x in test:
                    x.setForeground(QBrush(QColor("red")))
            else:
                include[idx] = 'False'
                for x in test:
                    x.setForeground(QBrush(QColor("gray")))

            empty[0].setFlags(empty[0].flags() & ~
                               Qt.ItemFlag.ItemIsSelectable)
            self.setCurrentItem(empty[0])

            

    def mouseMoveEvent(self, e) -> None:
        #block click and drag 
        pass

    def select_all(self):
        #self.update_value(self.species, self.include, 'All')
        self.selectAll

    def select_none(self):
        self.selectionModel().clear()
    
     
class Title(QLabel):
    def __init__(self, title, bind=None, pos = None):
        super(Title, self).__init__()
        self.setWordWrap(True)
        self.setText(title)
        if pos == 'L' or pos == 'l':
            self.setAlignment(Qt.AlignmentFlag.AlignLeft)
        elif pos == 'R' or pos == 'r':
            self.setAlignment(Qt.AlignmentFlag.AlignRight)
        elif pos == 'T' or pos == 't':
            self.setAlignment(Qt.AlignmentFlag.AlignTop)
        elif pos == 'B' or pos == 'b':
            self.setAlignment( Qt.AlignmentFlag.AlignBottom)
        


class ValueBox(QSpinBox):
    def __init__(self, max_value, bind, bind_index):
        max_value = int(max_value)
        load_value = int(bind[bind_index])
        super(ValueBox, self).__init__()
        self.setRange(1,max_value)
        self.setValue(load_value)
        self.valueChanged.connect(
            partial(self.update_value, bind, bind_index))
        self.value = load_value

    def update_value(self, bind, bind_index, new_values):
        bind[bind_index] = str(new_values)


class Button(QPushButton):
    def __init__(self, text="Placeholder", config = None, bind = None):
        super(Button, self).__init__()
        self.setText(text)
        # if text == "Select species, all":
        #     self.clicked.connect(partial(self.list_select_all, config))
        # if text == "Select species, none":
        #     self.clicked.connect(partial(self.list_select_none, config))
        if text == "Save settings":
            self.clicked.connect(partial(self.update_value, config, bind))
        elif text == "Run":
            self.clicked.connect(partial(self.pass_values, config, bind))
        elif text == "Stop":
            pass
        elif text == "Quit":
           self.clicked.connect(partial(self.stop_exec, config))
    

    def list_select_all(self, window: MainWindow):
        window.get_features()[1][0].select_all()
      

    def list_select_none(self, window: MainWindow):
        window.get_features()[1][0].select_none()


    def update_value(self, config , bind):
        for i, section in enumerate(config.sections()):
            for j, item in enumerate(config.items(section)):
                test = bind[i][j]
                config[section][item[0]] = bind[i][j]

        for i, section in enumerate(config.sections()):
            for j, item in enumerate(config.items(section)):
                test = config[section][item[0]] 

        #workaround for unicode path
        config.write(codecs_open(config.path, 'wb+', 'utf-8'))
    

    def pass_values(self, bind: list, window: MainWindow):
        features = window.get_features()
        app = window.Qt_app
        config.SCREEN_WIDTH = int(bind[0][0])
        config.SCREEN_HEIGHT = int(bind[0][1])
        
        config.BREATH_HALF_PERIOD = int(bind[1][0])
        config.BREATH_HALF_PERIOD_RANDOMIZE = False if bind[1][1] == "False" else True
        config.NUMBER_OF_PERIODS = int(bind[1][2])
        config.NUMBER_OF_PERIODS_RANDOMIZE = False if bind[1][3] == "False" else True
        config.BREATH_VOLUME = float(bind[1][4])/100
        config.BREATH_VOLUME_RANDOMIZE = False if bind[1][5] == "False" else True
        config.PER_FRAME_INCREMENT = float(bind[1][6])
        config.PER_FRAME_INCREMENT_RANDOMIZE = False if bind[1][7] == "False" else True

        config.PARTIONS = int(bind[2][0])
        config.SAVE_PATH = bind[2][1]
        config.IMG_TYPE = bind[2][2]

 
        config.SPECIES_IN_ROTATION = []
        for i,species in enumerate(bind[4]):
            if species == 'True':
                config.SPECIES_IN_ROTATION.append(i)

        config.NUMBER_OF_CYCLES = int(bind[5][0])

        #ANIMATION PARAMETERS
        #Breath volume adjustment parameters
        config.BREATH_VOLUME_MAX = float(bind[1][4])/100 #bind[6][0]
        config.ORIGINAL_BREATH_VOLUME_MIN = float(bind[6][1])
        config.BREATH_VOLUME_MIN = float(bind[6][2])
        config.EXHALE_INCREMENT = float(bind[1][6])
        config.INHALE_INCREMENT = float(bind[1][6])
        #interpolation variables for animation, cubic bezier has 2 inbetween points, 
        # but we calculate third as the "middle " between the two
        config.MIDDLE_POINT_CHANGE = float(bind[6][5])
        config.FIRST_POINT_CHANGE = float(bind[6][6])
        config.SECOND_POINT_CHANGE = float(bind[6][7])

        #POSTPROCESSING
        #gaussian noise kernel size
        config.POSPROCESSING_KERNEL_SIZE = int(bind[7][0])
        config.POSPROCESSING_CONTOUR_KERNEL_SIZE = int(bind[7][1])
        #random noise standart deviation and mean
        config.POSPROCESSING_STD_DEVIATION = float(bind[7][2])
        config.POSPROCESSING_MEAN = float(bind[7][3])
                                            
        #FLAGS                               
        # Should we try to run on multiple threads 
        config.Flags.use_threads_flag = False if bind[8][0] == "False" else True
        # some load_mask has cython variant
        config.Flags.use_cython = False if bind[8][1] == "False" else True
        #hide window glfw
        config.Flags.hide_window_flag = False if bind[8][2] == "False" else True
        #hide cursor for glfw window
        config.Flags.disable_cursor_flag = False if bind[8][3] == "False" else True
        # render to invisible framebuffer, can render larger than monitor image
        config.Flags.render2fbo_flag = False if bind[8][4] == "False" else True
        # tell Generator_thread to save images or just pop the queue
        config.Flags.save_images_flag = False if bind[8][5] == "False" else True
        #use postprocessing in Screen_capture
        config.Flags.use_postprocessing_flag = False if bind[8][6] == "False" else True
    

        self.disable_ui(features)
 
        app.run_generator(window)
        
      
    def disable_ui(self, features: list[list[QWidget]]):
        for widgets in features:
            for w in widgets:
                if isinstance(w, Button) and w.text() == 'Quit':
                    pass
                else:
                    w.setEnabled(False)

        QTest.qWait(50)

    
    def stop_exec(self, window:MainWindow):

        if window.Qt_app.quit_app(window) == 0:
            window.Qt_app.quit()
            sys_exit()
        else:
            print("Simulator didn't quit properly")
      


class CheckBox(QCheckBox):
    def __init__(self, bind, bind_index, label="Randomize"):
        super(CheckBox, self).__init__()
        state = 2 if bind[bind_index] == 'True' else 0
        self.setChecked(state)
        self.setText(label)
        self.stateChanged.connect(partial(self.update_value, bind, bind_index))
        self.value = 0

    def update_value(self, bind, bind_index, new_state):
        bind[bind_index] = 'True' if new_state == 2 else 'False'


class Box(QComboBox):
    def __init__(self, resolutions: list[list[int]], bind , bind_index: list[int]):
        super(Box, self).__init__()
        resolutions_strings = []
        for values in resolutions:
            string = "%d%s%d" % (values[0], "x", values[1])
            resolutions_strings.append(string)
        self.addItems(resolutions_strings)
        try:
            # idx = resolutions.index([bind[bind_index[0]],bind[bind_index[1]]])
            idx = resolutions.index([int(bind[x]) for x in bind_index])
        except:
            print(
                f"Could not find specified resolution: {tuple(bind[x] for x in bind_index)}.")
            print(f"Replacing with: {resolutions_strings[-1]}.")
            idx = -1
        self.setCurrentText(resolutions_strings[idx])
        self.update_value(bind,bind_index,idx)
        self.currentIndexChanged.connect(partial(self.update_value, bind, bind_index))
       
    def update_value(self, bind, bind_index, idx):
        new_values = [str(x) for x in resolutions[idx]]
        for idx in bind_index:
            bind[idx] = new_values[idx]
        
        
class Color(QWidget):

    def __init__(self, color, bind=None):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)
        pass
        

class Configuration(configparser.ConfigParser):
    def __init__(self, path):
        super(Configuration, self).__init__()
        self.path = path



