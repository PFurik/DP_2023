from imports_simulator import *


def randomf_range(min, max):
    rnd = min + (max - min) * np.random.random_sample()
    return rnd



def set_globals():

    def randomize(min, max, val):
        
        return val + np.random.random_integers(min,max) #random.randint(min,max)

    if config.BREATH_HALF_PERIOD_RANDOMIZE == True:
        config.BREATH_HALF_PERIOD = randomize(-config.BREATH_HALF_PERIOD //
                                              2, config.BREATH_HALF_PERIOD//2, config.BREATH_HALF_PERIOD)
    if config.NUMBER_OF_PERIODS_RANDOMIZE == True:
        config.NUMBER_OF_PERIODS = randomize(-config.NUMBER_OF_PERIODS//2, config.NUMBER_OF_PERIODS//2, config.NUMBER_OF_PERIODS)
    if config.BREATH_VOLUME_RANDOMIZE == True:
        config.BREATH_VOLUME = randomize(-config.BREATH_VOLUME/2,
                  config.BREATH_VOLUME/2, config.BREATH_VOLUME)
    if config.PER_FRAME_INCREMENT_RANDOMIZE == True:
        config.PER_FRAME_INCREMENT = randomize(-config.PER_FRAME_INCREMENT//2,
                                        config.PER_FRAME_INCREMENT//2, config.PER_FRAME_INCREMENT)



# create context for gl
class Glfw_window(glfw_GLFWwindow):
    def __init__(self, flags: config.Flags) -> None:
        super(Glfw_window, self, ).__init__()
        self.initialize_glfw()
        if flags.render2fbo_flag == False:

            if flags.hide_window_flag == True:
                self.hide_window()

            self.create_window()

            if flags.disable_cursor_flag == True:
                self.disable_cursor()

        else:
            self.hide_window()
            self.create_window()
            
            self.create_fbo()


    def initialize_glfw(self):

        glfw_init()
        glfw_window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw_window_hint(GLFW_CONSTANTS.GLFW_CONTEXT_VERSION_MINOR, 3)

  
        glfw_window_hint(
            GLFW_CONSTANTS.GLFW_OPENGL_PROFILE,
            GLFW_CONSTANTS.GLFW_OPENGL_CORE_PROFILE
        )
        glfw_window_hint(
            GLFW_CONSTANTS.GLFW_OPENGL_FORWARD_COMPAT,
            GLFW_CONSTANTS.GLFW_TRUE
        )
        glfw_window_hint(GLFW_CONSTANTS.GLFW_DOUBLEBUFFER, GL_FALSE)


    def create_window(self):
        self.window = glfw_create_window(
            config.SCREEN_WIDTH, config.SCREEN_HEIGHT, "TEST", None, None)
        glfw_make_context_current(self.window)
        glViewport(0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        

    def create_fbo(self):
        # set this for future frame buffer, we need the buffer to generate resolutions larger than monitor
        # create frame buffer
        self.fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)

        self.colorBuffer = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.colorBuffer)
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGB,
            config.SCREEN_WIDTH, config.SCREEN_HEIGHT,
            0, GL_RGB, GL_UNSIGNED_BYTE, None
        )
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glBindTexture(GL_TEXTURE_2D, 0)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0,
                               GL_TEXTURE_2D, self.colorBuffer, 0)

        self.depthStencilBuffer = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, self.depthStencilBuffer)
        glRenderbufferStorage(
            GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, config.SCREEN_WIDTH, config.SCREEN_HEIGHT
        )
        glBindRenderbuffer(GL_RENDERBUFFER, 0)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT,
                                  GL_RENDERBUFFER, self.depthStencilBuffer)


    def hide_window(self):

        glfw_window_hint(
            GLFW_CONSTANTS.GLFW_VISIBLE,
            GLFW_CONSTANTS.GLFW_FALSE
        )


    def disable_cursor(self):
            glfw_set_input_mode(self.window,
            GLFW_CONSTANTS.GLFW_CURSOR,
            GLFW_CONSTANTS.GLFW_CURSOR_HIDDEN
        )


    def quit(self, flags: config.Flags):
        if flags.render2fbo_flag == True:
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            glDeleteFramebuffers(1, [self.fbo,])
            glDeleteTextures(1, [self.colorBuffer,])
            glDeleteRenderbuffers(1, [self.depthStencilBuffer,])
        else:
            glfw_destroy_window(self.window)




class Object:

    def __init__(self, position, eulers, upscale = 1.0):

        self.position = upscale * np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

    def update(self, frametime, flags: config.Flags):
        pass

    def draw(self):
        pass

    def destroy(self):
        pass
    



class Breathing_lizard:

    def __init__(self, position, eulers, upscale):
        self.model = 0
        self.position = upscale * np.array(position, dtype=np.float32)
        self.original_position = upscale * np.array(deepcopy(position))
        self.eulers = np.array(eulers, dtype=np.float32)

    def set_animation_model(self, animateModel):
        self.model = animateModel

    def update(self, frametime, flags: config.Flags):
        self.model.update(frametime, flags)

    def draw(self, scale, flags):
        self.model.draw(scale, flags)

    def destroy(self):
        self.model.destroy()


class Light:


    def __init__(self, direction, color, strength):

        self.direction = np.array(direction, dtype=np.float32)
        self.color = np.array(color, dtype=np.float32)
        self.color_original = np.array(color, dtype=np.float32)
        self.strength = strength


class Scene:

    def __init__(self):
        self.direction = [-0.2, -0.5, -1],
        self.orig_light_strenght = 5

        self.objects = [

            Breathing_lizard(
                position = [-0.2, -0.5, -1],
                eulers = [0, 0, 0],
                upscale = 1.0
            ),
            Object (
                position = [-0.2, -0.5, -1],
                eulers = [0, 0, 0],
                upscale = 1.0
            )
        ]

        self.lights = [
            Light(
                direction=[-0.2, -0.5, -1],
                color = [0.5, 0.47, 0.32],
                strength =  5
            )
        ]

    def update(self, rate, flags: config.Flags):

        for object in self.objects:
            object.update(rate, flags)
            #object.update(rate)
            #object.eulers[1] += 0.25 * rate
            #if object.eulers[1] > 360:
                #object.eulers[1] -= 360
    
    def destroy(self):
        for object in self.objects:
            object.destroy()




class Breathing_simulator:
    def __init__(self, status):

        set_globals()
        self.scene = Scene()
        self.flags = config.Flags()
        self.window = Glfw_window(self.flags)
        self.assets_deleted = False

        
        self.renderer = GraphicsEngine(self.scene, self.flags)
        self.screen_capture = Screen_capture()
      
        #calc framerate vars
        self.frame_index = int(0) 
        self.lastTime = glfw_get_time()
        self.currentTime = 0
        self.frame_counter = 0
        self.frameTime = 0

        #self.mainLoop(status)

    def mainLoop(self, status, queue: Buff_queue, run_simulation) -> int:
        self.flags.run_flag = True
        self.renderer.material.load_alternate.start()
        status.setText("Simulation started...")
        while (self.flags.run_flag):
            if not(self.screen_capture.curr_frame % 10):
                status.setText(f"Simulation started...Line: {self.screen_capture.curr_frame}")
            self.flags.period_flag = False
            # check events
            if glfw_window_should_close(self.window) \
                    or glfw_get_key(self.window, GLFW_CONSTANTS.GLFW_KEY_ESCAPE) == GLFW_CONSTANTS.GLFW_PRESS \
                        or (self.renderer.number_of_cycles == config.NUMBER_OF_CYCLES):
                    
                self.flags.run_flag = False
                break
            glfw_poll_events()

          
            self.scene.update(self.frameTime / 16.7, self.flags)
            self.renderer.render(self.scene, self.flags)
            self.screen_capture.capture_screen(self.flags, queue)

            # timing
            self.calculateFramerate()

        return self.quit(status,  run_simulation)

    
    def calculateFramerate(self):

        self.currentTime = glfw_get_time()
        delta = self.currentTime - self.lastTime
       
        if (delta >= 1):  # if more than a second has passed
            framerate = max(1, int(self.frame_counter / delta))
            #glfw_set_window_title(self.window, f"Running at {framerate} fps.")
            #glfw_set_window_title(self.window, f"Current frame {self.frame_index}")
            self.lastTime = self.currentTime
            self.frame_counter = -1
            self.frameTime = float(1000.0/max(1, framerate)) #seconds to ms
        self.frame_counter += 1
        self.frame_index += 1

    def reset_flags(self, ):
        pass
        #self.flags.period_flag = False
        #self.flags.cycle_flag = False
        
    def quit(self, status, run_simulation) -> int:
        run_simulation.stop()
        if not self.assets_deleted:
            status.setText("Quiting simulation...")
            self.renderer.quit(self.flags, run_simulation)
            self.scene.destroy()
            #deleting window destroys context, do it after 
            self.window.quit(self.flags)
            self.assets_deleted = True
        return 0




class GraphicsEngine:

    def __init__(self, scene: Scene, flags: config.Flags):

        #the model is really small, make it bigger [x,y,z]
        self.scale = [100, 100, 100] 
        self.original_scale = np.array(self.scale, dtype=np.float32)
        self.scale = self.original_scale.copy()
        self.number_of_cycles = 0
        #independent iterator from value in species
        self.idx_species  = 0
        self.do_mirror = 0
        #due to the float precision and "small" object we need to upscale model, textures, masks ...
        self.upscale = 1.0

        """
        Ještěrka obecná
        Ještěrka zední
        Ještěrka zelená
        Ještěrka živorodá
        Ještěrka travní
        """
        self.species_dictionary = {

            "Lacerta agilis female": 0,
            "Lacerta agilis male": 1,

            "Podarcis muralis female": 2,
            "Podarcis muralis male": 3,

            "Lacerta viridis female": 4,
            "Lacerta viridis male": 5,

            "Zootoca vivipara female": 6,
            "Zootoca vivipara male": 7,

            "Podarcis tauricus female": 8,
            "Podarcis tauricus male": 9
        }
        
 
        #self.create_fbo()
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glDepthFunc(GL_LESS)
        glCullFace(GL_BACK)
        glEnable(GL_BLEND)
        glBlendFuncSeparate(
            GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_ONE, GL_ONE)
        glBlendEquation(GL_FUNC_ADD)

        # initialise opengl
        glClearColor(0.1, 0.2, 0.2, 1) #some type of green color, with alpha channel == 1

        #create shaders, first one for lizard, second one for plane
        self.shader = self.createShader(
            "shaders/vertex.glsl", "shaders/fragment.glsl")
        glUseProgram(self.shader)
        self.shader_plane = self.createShader(
            "shaders/plane_vertex.glsl", "shaders/plane_fragment.glsl")
      

        #pick first lizard in list
        self.species = config.SPECIES_IN_ROTATION[0] #self.species_dictionary["Podarcis tauricus female"]
        # get skin paramas based on its species
        self.Skin_modifier = Skin_params(self.species)

        self.material = Material("lizard", "dds", self.Skin_modifier, flags)
        self.material_plane = Material(
            "plane", "dds", self.Skin_modifier, flags)
        self.material.use_masks(self.idx_species)


        #cube = Mesh("models/cube.obj")
        self.object_mesh = Mesh("models/plane.obj", flags, self.upscale)
        frame1 = Mesh("models/lizard_exhale.obj", flags, self.upscale)
        frame2 = Mesh("models/lizard_inhale.obj", flags,  self.upscale)


        # if config.BREATH_VOLUME < 1:
        #     frame2.limit_exhale(frame1.get_vertices(),config.BREATH_VOLUME)
            
        # shader, frame_time, frame_model_at_time, textures
        #self.object_mesh = Mesh("models/lizard_inhale.obj"
        '''
        the frames = [] here affect the speed of breathing
        '''
        self.animation_mesh = Animate_model(self.shader, 
                                            config.BREATH_HALF_PERIOD, config.NUMBER_OF_PERIODS,
                                              models=[frame1, frame2, frame1])
        for object in scene.objects:
            if isinstance(object,Breathing_lizard):
                object.set_animation_model(self.animation_mesh)

   
        self.to_shader_bend_params(frame1.y_coord_extremes)

        #TEXTURES
        self.texture_names = ['Material.base_map',
                              'Material.normalMap', 'Material.smoothnessMap']
        self.mask_names = ['Material.mask1',
                           'Material.mask2', 'Material.mask3']
        self.mask_color_names = ["Material.base_color",
                                 "Material.stripe_color", "Material.blob_color", "Material.dots_color"]
        
        self.to_shader_texture_names(self.shader, self.texture_names)
        self.to_shader_texture_names(self.shader_plane, self.texture_names[0:1]) #plane has only diffuse/albedo, for now
        self.to_shader_masks(self.shader)

        #PROJECTION
        # with near and far you can cut off the legs
        projection_transform = matrix44.create_perspective_projection(
            fovy=45, aspect=config.SCREEN_WIDTH/config.SCREEN_HEIGHT,
            near=self.upscale/2, far= self.upscale + 1000, dtype=np.float32
        )
        self.to_shader_light()
        self.to_shader_projection(projection_transform, scene)
    


    def to_shader_projection(self,projection_transform, scene: Scene):

        glUseProgram(self.shader)
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "projection"),
            1, GL_FALSE, projection_transform
        )

        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")

        glUniform3fv(glGetUniformLocation(self.shader, "cameraPosition"),
                     1, scene.direction)
        
        glUseProgram(self.shader_plane)

        glUniformMatrix4fv(glGetUniformLocation(self.shader_plane, "projection"),
                             1, GL_FALSE, projection_transform
                             )

        self.plane_modelMatrixLocation = glGetUniformLocation(self.shader_plane, "model")

        glUniform3fv(glGetUniformLocation(self.shader_plane, "cameraPosition"),
                     1, scene.direction)


    def to_shader_light(self):
        #LIGHTS
        self.lightLocation = {
            "direction": [
                glGetUniformLocation(self.shader, "Light.direction")
            ],
            "color": [
                glGetUniformLocation(self.shader, "Light.color")
            ],
            "strength": [
                glGetUniformLocation(self.shader, "Light.strength")
            ]
        }

        self.lightLocation_plane = {
            "direction": [
                glGetUniformLocation(self.shader_plane, "Light.direction")
            ],
            "color": [
                glGetUniformLocation(self.shader_plane, "Light.color")
            ],
            "strength": [
                glGetUniformLocation(self.shader_plane, "Light.strength")
            ]
        }
    
      

    def createShader(self, vertexFilepath, fragmentFilepath):

        with open(vertexFilepath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath, 'r') as f:
            fragment_src = f.readlines()

       
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))

        return shader


    def render(self, scene: Scene, flags: config.Flags):

        # refresh screen
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.shader)
 

        for i, light in enumerate(scene.lights):
            if flags.period_flag == True:
                light.strength = scene.orig_light_strenght + np.random.uniform(0,3)
                light.color = light.color_original + [np.random.randint(-5, 5) * 0.01, np.random.randint(-5, 5)* 0.01, np.random.randint(-2, 20)* 0.01]

            glUseProgram(self.shader_plane)
            glUniform3fv(
                self.lightLocation_plane["direction"][i], 1, light.direction)
            glUniform3fv(self.lightLocation_plane["color"][i], 1, light.color)
            glUniform1f(self.lightLocation_plane["strength"][i], np.float32(light.strength))

            glUniform3fv(glGetUniformLocation(self.shader_plane, "cameraPosition"),
                         1, scene.direction)    

            glUseProgram(self.shader)
            glUniform3fv(self.lightLocation["direction"][i], 1, light.direction)
            glUniform3fv(self.lightLocation["color"][i], 1, light.color)
            glUniform1f(self.lightLocation["strength"][i], np.float32(light.strength))

            glUniform3fv(glGetUniformLocation(self.shader, "cameraPosition"),
                            1, scene.direction)
            



        for object in scene.objects:

            if isinstance(object, Breathing_lizard):

                glBindVertexArray(self.animation_mesh.vao)
                flags.screen_cap_flag = 0
                #self.to_shader_period_flag()
                if (flags.period_flag == True) or (flags.lines_full_flag == True): #period as in inhale,exhale,inhale or exhale,inhale,exhale
                    self.to_shader_bend_params(object.model.base_models[0].y_coord_extremes)
                    self.to_shader_uv_shuffle()
                    self.to_shader_scale_shuffle(self.scale)
                    self.to_shader_position_shuffle(object.position)
                    flags.screen_cap_flag = 3
                    self.rotate_species(flags)
                    if self.number_of_cycles == config.NUMBER_OF_CYCLES: #simulator should be ending if this condition is met
                        flags.screen_cap_flag = 2
                        break
                    self.to_shader_masks(self.shader)
                    self.animation_mesh.update_breath_volume()
                    #self.animation_mesh.model_shuffle()
                    self.material.use_masks(self.idx_species)
                    #self.scale_shuffle(object, self.original_scale)
                    flags.period_flag = False

                if flags.cycle_flag == True: # cycle meaning we are back at the start of config.SPECIES_IN_ROTATION
                    flags.screen_cap_flag = 3
                    self.material.update_texture()
                    self.material.update_mask(flags, self.idx_species, self.species)
                    flags.cycle_flag = False

                if flags.first_frame_flag == True:
                    flags.first_frame_flag = False
                    flags.screen_cap_flag = 1

                if flags.last_frame_flag == True:
                    flags.last_frame_flag = False
                    flags.screen_cap_flag = 4
                
                object.draw(self.scale, flags)
                self.material.use_textures()
               
                model_transform = matrix44.create_identity(dtype=np.float32)

                #rotate 
                model_transform = matrix44.multiply( 
                    m1=model_transform,
                    m2=matrix44.create_from_eulers(
                        eulers=np.radians(object.eulers), dtype=np.float32
                    )
                )
                #scale
                model_transform = matrix44.multiply( 
                    m1=model_transform,
                    m2= matrix44.create_from_scale(self.scale)
                )

                #position
                model_transform =matrix44.multiply(
                    m1=model_transform,
                    m2= matrix44.create_from_translation(
                        vec=np.array(object.position), dtype=np.float32)
                )

                # that GL_FALSE tells the function NOT to transpose 
                # because it'll be passed corretly from pyrr
                # the first row is actually the first coll in shader

                glUniformMatrix4fv(self.modelMatrixLocation, 1,
                                   GL_FALSE, model_transform)

                glDrawArrays(GL_TRIANGLES, 0, object.model.vertex_count)

            if isinstance(object, Object):
                
                glUseProgram(self.shader_plane)
                self.material_plane.use_textures()
                glBindVertexArray(self.object_mesh.vao)
                model_transform = matrix44.create_identity(dtype=np.float32)

                model_transform = matrix44.multiply(
                    m1=model_transform,
                    m2=matrix44.create_from_eulers(
                        eulers=np.radians(object.eulers), dtype=np.float32
                    )
                )
                model_transform = matrix44.multiply(
                    m1=model_transform,
                    m2=matrix44.create_from_scale(self.scale)
                )
                model_transform = matrix44.multiply(
                    m1=model_transform,
                    m2=matrix44.create_from_translation(
                        vec=np.array(object.position), dtype=np.float32
                    )
                )

                glUniformMatrix4fv(self.plane_modelMatrixLocation, 1,
                                GL_FALSE, model_transform)
                glDrawArrays(GL_TRIANGLES, 0, self.object_mesh.vertex_count)

        #buffer to screen  
        glFlush()


    def to_shader_uv_shuffle(self):
        #add slight deformation to texture coords, values are independent from actual vertex position
        a = -0.0009
        b = 0.0009
        
        uv_idx = np.random.random_integers(0, 1) #random.randint(0, 1)
        uv_val =  randomf_range(a, b)#a + (b - a) * np.random.random_integers(0, 1) #random.randint(0,1)
        uv_val = np.float32(uv_val)
 
        glUniform1i(glGetUniformLocation(self.shader, "uv_idx"),
                   uv_idx)
        glUniform1f(glGetUniformLocation(self.shader, "uv_val"),
                    np.float32(uv_val))
        

    def to_shader_bend_params(self, extreme: list[float]):

        '''
        To answer why mulitply by 0.0001, there was a bug that required upscale to be 10000
        it is now gone so the to_shader shuffle parameters everywhere gotta go down
        '''
        F = randomf_range(0.0001,1.5)#np.random.random_sample(1, 2)  # random.randint(1,2)
        # / F  # random.randint(50, 500)
        A = np.random.random_integers(25 , 500) * 0.0001
        P = np.pi * randomf_range(-1,1)#np.random.random_integers(0,2)
        Off = randomf_range(0, 5) * 0.0001
        do_sin = 1 #np.random.random_integers(0,1) just do sinus
        do_cos = 0 #1 - do_sin

        glUniform1f(glGetUniformLocation(self.shader, "amplitude"),
                    np.float32(A))
        glUniform1f(glGetUniformLocation(self.shader, "frequency"),
                    np.float32(F))
        glUniform1f(glGetUniformLocation(self.shader, "offset"),
                    np.float32(Off))
        glUniform1f(glGetUniformLocation(self.shader, "phase"),
                    np.float32(P))
        glUniform1f(glGetUniformLocation(self.shader, "max_y"),
                     np.float32(extreme[0]))
        glUniform1f(glGetUniformLocation(self.shader, "min_y"),
                     np.float32(extreme[1]))
        glUniform1i(glGetUniformLocation(self.shader, "do_cos"),
                    do_cos)
        glUniform1i(glGetUniformLocation(self.shader, "do_sin"),
                    do_sin)


    def to_shader_scale_shuffle(self, scale: list[float]):
        scale_val = []
        do_mirror = np.random.random_integers(0,1)
        a = 0.1
        b = 0.5
        # we have culling enabled, if we mirror the object we would see the lizards belly
        if not do_mirror:
           glCullFace(GL_BACK)
        else:
            glCullFace(GL_FRONT)
            
        scale_val = np.array([randomf_range(a, b) for x in scale], dtype=np.float32)
        glUniform3fv(glGetUniformLocation(self.shader, "scale_val"),
                     1, scale_val)
        glUniform1i(glGetUniformLocation(self.shader, "do_mirror"),
                     do_mirror)
        glUseProgram(self.shader_plane)
        glUniform1i(glGetUniformLocation(self.shader_plane, "do_mirror"),
                     do_mirror)
        glUseProgram(self.shader)




    def to_shader_position_shuffle(self, position: list[float]):
        a = -250 * 0.0001
        b = 250 * 0.0001
        position_val = np.array([randomf_range(a, b) for x in position], dtype=np.float32)
        glUniform3fv(glGetUniformLocation(self.shader, "position_val"),
                     1, position_val)
        
    # def scale_shuffle(self, object, original_scale):
    #     a = -5
    #     b = 5
    #     object.position[0] = object.original_position[0]
    #     for i in range(len(original_scale)):
    #         self.scale[i] = original_scale[i] + a + (b-a)*random.random()

    #     # roll for mirror
    #     if random.randint(0,1):
    #         object.position[0] = -object.position[0]
    #         self.scale[0] = - self.scale[0]

            
    def to_shader_masks(self, shader):
        glUseProgram(shader)
        #load different mask based on current species
        #if isinstance(species_name, str):
            #self.species = self.species_dictionary[species_name]

        self.Skin_modifier = Skin_params(self.species)
        [self.color_shuffle(color) for color in self.Skin_modifier.species_color]

        start_index = len(self.texture_names)
        for idx, name in enumerate(self.mask_names):
            glUniform1i(glGetUniformLocation(self.shader, name), start_index + idx)

    
        for i, name in enumerate(self.mask_color_names):
            glUniform3fv(glGetUniformLocation(self.shader, name),
                        1, self.Skin_modifier.species_color[i])
        # glUniform3fv(glGetUniformLocation(self.shader, "stripe_color"),
        #              1, self.Skin_modifier.species_color[1])
        # glUniform3fv(glGetUniformLocation(self.shader, "blob_color"),
        #              1, self.Skin_modifier.species_color[2])
        # glUniform3fv(glGetUniformLocation(self.shader, "dots_color"),
        #              1, self.Skin_modifier.species_color[3])
        
    def to_shader_texture_names(self, shader, texture_names):
        glUseProgram(shader)
        for idx, name in enumerate(texture_names):
            glUniform1i(glGetUniformLocation(shader, name), idx)


        
    def color_shuffle(self, color:list[float]):
        a = -0.02; b = 0.02
        to_add = color
        to_add += a + (b-a) * np.random.rand(len(color))


    def rotate_species(self, flags: config.Flags):
        # rotate current species in config.SPECIES_IN_ROTATION
        # there are two independent iterators
        # idx_species is index in arrays, species is type of lizard
        if self.species == config.SPECIES_IN_ROTATION[-1]:
            self.species = config.SPECIES_IN_ROTATION[0]
            self.idx_species  = 0
            self.number_of_cycles += 1
            flags.cycle_flag = True
        else:
            self.idx_species += 1
            self.species = config.SPECIES_IN_ROTATION[self.idx_species]


    def quit(self, flags:config.Flags, run_simulation):
        
        try:
            self.object_mesh.destroy()
        except:
            print("No object mesh to destroy")
        try: 
            self.animation_mesh.destroy()
        except:
            print("No animation mesh")
        self.material.destroy()
        self.material_plane.destroy()
        glDeleteProgram(self.shader)
        glDeleteProgram(self.shader_plane)




class Screen_capture:
    def __init__(self) -> list[np.array]:
        self.total_frames = config.BREATH_HALF_PERIOD * config.NUMBER_OF_PERIODS
        self.reset_frame_idx()
        self.img = []
        self.scan_data = []
        self.full_img = [] #ScreenShotBuffer()
    
    def capture_screen(self, flags: config.Flags, queue: Buff_queue):

        flags.lines_full_flag = False
        if flags.screen_cap_flag == 1: # first frame capture
            self.__capture_matrix(queue)
            #flags.first_frame_flag = False
        elif flags.screen_cap_flag == 2: # last frame of simulation
            self.__capture_matrix_end(queue, flags)
        elif flags.screen_cap_flag == 3: # new species period
           self.__capture_matrix_period(queue, flags)
        elif flags.screen_cap_flag == 4: # last frame before period
           self.__capture_matrix_rest()
        else:
            self.__capture_line()

        if self.curr_frame < config.SCREEN_HEIGHT - 1:
            #scan the lines within screen height
            self.curr_frame += 1
        else:
            #we should move onto next lizard
            flags.lines_full_flag = True
            self.reset_frame_idx()
       

    def __capture_matrix(self, queue: Buff_queue):
        # this should work as area scan camera
        data = glReadPixels(
            0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, GL_RGBA, GL_UNSIGNED_BYTE)
        data = Image.frombytes(
            "RGBA", (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), data)
        data = data.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
        data = np.array(data)
        full = deepcopy(np.array(data))
        self.scan_data.append(data)
        #self.full_img.append(full)
        queue.put(full)


    def __capture_line(self):
        #this should work as line scan camera for screen in fbo
        data = glReadPixels(
            0, config.SCREEN_HEIGHT - self.curr_frame, config.SCREEN_WIDTH, 1, GL_RGBA, GL_UNSIGNED_BYTE)
        data = Image.frombytes(
            "RGBA", (config.SCREEN_WIDTH, 1), data)

        data = np.array(data)
        self.scan_data[0][self.curr_frame] = data[0]

    def __capture_matrix_rest(self):
        #capture the screen and slice only the remainder based on current frame
        data = glReadPixels(
            0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, GL_RGBA, GL_UNSIGNED_BYTE)
        data = Image.frombytes(
            "RGBA", (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), data)
        data = data.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
        data = np.array(data)
        self.scan_data[0][self.curr_frame:] = data[self.curr_frame:]


    def __capture_matrix_period(self, queue: Buff_queue, flags: Flags):
        data = glReadPixels(
            0, 0, config.SCREEN_WIDTH, config.SCREEN_HEIGHT, GL_RGBA, GL_UNSIGNED_BYTE)
        data = Image.frombytes(
            "RGBA", (config.SCREEN_WIDTH, config.SCREEN_HEIGHT), data)
        data = data.transpose(method=Image.Transpose.FLIP_TOP_BOTTOM)
        data = np.array(data)
        full = deepcopy(np.array(data))

        # cv.imshow("scan", self.scan_data[0])
        # k = cv.waitKey()
        #self.full_img.append(self.scan_data[0])
        if flags.use_postprocessing_flag:
            queue.put(self.postprocessing(self.scan_data[0]))
        else:
            queue.put(self.scan_data[0])
        self.scan_data = []
        self.scan_data.append(data)
        #self.full_img.append(full)
        queue.put(full)
        self.reset_frame_idx()


    def __capture_matrix_end(self, queue: Buff_queue, flags: Flags):
        if flags.use_postprocessing_flag:
            queue.put(self.postprocessing(self.scan_data[0]))
        else:
            queue.put(self.scan_data[0])
        #self.full_img.append(self.scan_data[0])
        

    def reset_frame_idx(self, value = config.SCREEN_HEIGHT):
        #here we can reset the curr frame to the start or to the edge of the neck. which one ?
        # OR  we can skip to random 
        self.curr_frame = value // 7
        #self.curr_frame = value//10


    def postprocessing(self, img: np.ndarray):
        """
        Aplly some filters to simulate image capture
        """
        mean = config.POSPROCESSING_MEAN
        stddev = config.POSPROCESSING_STD_DEVIATION
        noise = np.zeros(img.shape, np.uint8)
        B,G,R,_ = cv.split(noise)
        B = cv.randn(B, mean, stddev)
        G = cv.randn(G, mean, stddev)
        R = cv.randn(R, mean, stddev)
        # There is colored noise due from capture, you can replace this with for loop 
        noise[:,:, 0] = cv.add(B, noise[:,:, 0]) 
        noise[:,:, 1] = cv.add(G, noise[:,:, 1]) 
        noise[:, :, 2] = cv.add(R, noise[:,:, 2]) 
        noisy_img = cv.add(img, noise)
        k = config.POSPROCESSING_KERNEL_SIZE
        m = config.POSPROCESSING_CONTOUR_KERNEL_SIZE
        # The images are blurry 
        noisy_img = cv.GaussianBlur(noisy_img,(k, k),0)
        # the yellow tint comes from light color

        #attempt to blurr contour 
        blurred_img = cv.GaussianBlur(noisy_img, (m, m), 0)
        mask = np.zeros(noisy_img.shape, np.uint8)

        gray = cv.cvtColor(noisy_img, cv.COLOR_BGRA2GRAY)
        thresh = cv.threshold(gray, 50, 255, cv.THRESH_BINARY)[1]
        contours, hierarchy = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        cv.drawContours(mask, contours, -1, (255,255,255), 2*k)
        output = np.where(mask==np.array([255, 255, 255]), blurred_img, noisy_img)
        return output

        


class Mesh:
    def __init__(self, filename, flags: config.Flags, upscale = 1.0):

        # x, y, z, s, t, nx, ny, nz
        self.vertices_structure = ['x', 'y', 'z',
                                    's', 't',
                                    'nx', 'ny', 'nz',
                                    'tx', 'ty', 'tz'
                                    ]
        self.vertices_structure_count = [3, 2, 3, 3]
        self.original_vert = []
        # self.uv_index = 0
        # self.position_index = 0
        self.index = 0
     
        start = glfw_get_time()

        if flags.use_cython == True:
            self.original_vert = a_load_mesh.loadMesh(filename, upscale)
        else:
            self.original_vert = self.loadMesh(filename, upscale)


   
        self.original_vert = np.array(self.original_vert, dtype=np.float32)
        self.vertices = self.original_vert.copy()

        self.vertex_count = len(
                    self.original_vert)//len(self.vertices_structure)
        
        self.y_coord_extremes = []
        self.y_coord_extremes.append(np.max(self.vertices[1::len(self.vertices_structure)]))
        self.y_coord_extremes.append(np.min(self.vertices[1::len(self.vertices_structure)]))
        
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes,
                    self.vertices, GL_STATIC_DRAW)
        self.vertex_count = len(
            self.original_vert)//len(self.vertices_structure)
        
        n_bytes = 4
        byte_offset = 0
        total_bytes = int(len(self.vertices_structure) * n_bytes)
        for i, n_var in enumerate(self.vertices_structure_count):
            
            glEnableVertexAttribArray(i)
            glVertexAttribPointer(i, n_var, GL_FLOAT, GL_FALSE, total_bytes , ctypes.c_void_p(byte_offset))
            byte_offset += n_var * n_bytes

        end = glfw_get_time()
        print(f"Loaded .obj in {end - start} seconds")


    def loadMesh(self, filename, upscale):
        #reads .obj format

        # raw, unassembled data
        v = []
        vt = []
        vn = []
        
        # final, assembled and packed result
        vertices = []

        # open the obj file and read the data
        with open(filename, 'r') as f:
            line = f.readline()
            
            while line:
                words = line.split(" ")
                if words[0] == "v":
                    v.append([upscale *float(x) for x in words[1:]])
                elif words[0] == "vt":
                    texture_coord = [float(x) for x in words[1:]]
                    texture_coord[1] = -texture_coord[1] #negation because of OpenGL coordinates 
                    vt.append(texture_coord) 
                elif words[0] == "vn":
                    vn.append([float(x) for x in words[1:]])
                elif words[0] == "f":
                    vertices += self.get_triangle_data(words[1:], v, vt, vn)

                
                line = f.readline()
        return vertices 
    
    def get_triangle_data(self, words: list[str], v, vt, vn):
        # structure has changed now we have:
        # x, y, z, s, t, nx, ny, nz, tx,ty,tz, bx, by. bz
        vertices = []
        face_vertices = []
        face_texture = []
        face_normal =[]
        tangent = []
        bitangent = []

        words[-1] = words[-1].replace("\n", "")

        for vertex in words:
            data = [int(x) - 1 for x in vertex.split("/")]  # .obj has 1-based indexing, compensate
            index_position = data[0]
            index_texture = data[1]
            index_normal = data[2]
            face_vertices.append(v[index_position])
            face_texture.append(vt[index_texture])
            face_normal.append(vn[index_normal])

        triangles_in_face = len(words) - 2
        vertex_order = []
        """
            eg. 0,1,2,3 unpacks to vertices: [0,1,2,0,2,3]
        """
        
        for i in range(triangles_in_face):
            vertex_order.append(0)
            vertex_order.append(i+1)
            vertex_order.append(i+2)

        """"
        for TBN matrix we need the components of edge and 
        deltas of texture coordinates on tangent, bitangent
        this can probably be further simplified with matrices
        """
        points1 = face_vertices[vertex_order[0]]
        points2 = face_vertices[vertex_order[1]]
        points3 = face_vertices[vertex_order[2]]
        uv1 = face_texture[vertex_order[0]]
        uv2 = face_texture[vertex_order[1]]
        uv3 = face_texture[vertex_order[2]]
        edge1 = [points2[i] - points1[i] for i in range(3)]
        edge2 = [points3[i] - points1[i] for i in range(3)]
        deltaUV1 = [uv2[i] - uv1[i] for i in range(2)]
        deltaUV2 = [uv3[i] - uv1[i] for i in range(2)]
        # TB = inverse_deltauv_matrix * edge_matrix [0] = U, [1] = V in book reference
        determinant = (deltaUV1[0] * deltaUV2[1] - deltaUV1[1] * deltaUV2[0])
        if not determinant:
            determinant = 0.0001
        determinant = 1 / determinant
        adjung_matrix = np.array([[deltaUV2[1], -deltaUV2[0]], [-deltaUV1[1], deltaUV1[0]]])
        inverseUV = (determinant) * adjung_matrix
        edge_matrix = np.array([[edge1[0], edge1[1], edge1[2]], [
                            edge2[0], edge2[1], edge2[2]]])
        TB = inverseUV @ edge_matrix

        [tangent.append(val) for val in TB[0]]
        [bitangent.append(val) for val in TB[1]]

        for i in vertex_order:
            for x in face_vertices[i]:
                vertices.append(x)
            for x in face_texture[i]:
                vertices.append(x)
            for x in face_normal[i]:
                vertices.append(x)
            for x in tangent:
                vertices.append(x)
            for x in bitangent:
                vertices.append(x)


        return vertices

    # def get_vertices(self):
    #     return self.vertices

    # def get_uv_coordinates(self):
    #     #test = self.vertices[self.uv_indices]
    #     return self.vertices[self.uv_indices]

    #MOVED TO SHADER
    # def limit_exhale(self, min_vertices, amount):
    #     # only the x,y,z components in vertices
    #     delta = self.vertices - min_vertices
    #     self.original_vert = min_vertices + delta * amount
    #     self.vertices = self.original_vert.copy()

    #     # indices = []
    #     # indices.append([[xyz for xyz in vertex[0:2]] for vertex in self.vertices[0::len(self.vertices_structure)]])
    #     # delta = self.vertices[indices] - min_vertices[indices]
    #     # self.original_vert[indices] = min_vertices[indices] + delta * amount
    #     # self.vertices[indices] = self.original_vert[indices].copy()

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))


class Texture_file_names:
    def __init__(self, filename, filetype) -> None:
        self.type = filename
        if filename == 'lizard':

            self.albedo = f"textures/{filename}_4k.{filetype}"
            self.bump = f"textures/{filename}_bump.{filetype}"
            self.smoothness = f"textures/{filename}_smoothness.{filetype}"
            self.paths = [self.albedo, self.bump, self.smoothness]

        if filename == 'plane':
            self.albedo = f"textures/{filename}_texture.{filetype}"
            self.bump = f"textures/{filename}_bump.{filetype}"
            # self.smoothness = f"textures/{filename}_smoothness.png"
            self.paths = [self.albedo, self.bump]



class Material:

    def __init__(self, filename, filetype, Skin_modifier: Skin_params, flags: config.Flags):

        self.type = filename
        self.texture_names = Texture_file_names(filename, filetype)
        self.textures = []
        self.active_masks = []

        self.load_texture()
        glGenerateMipmap(GL_TEXTURE_2D)
        if self.type == 'lizard':
            
            #after each cycle we need to load new texture for the skin, scales. Try to fill a queue to speed this up
            self.alternate_skins = Buff_queue()
            self.load_alternate = Thread(target=get_new_skin, args=(self.alternate_skins, self.image, config.NUMBER_OF_CYCLES, flags))
        
            self.Skin_modifier = Skin_modifier # used for generating texture masks
            self.masks = []
            self.active_masks = []
            self.mask_type = ["dot", "blob"]  #checking for maks type, unfortunate way of checking file
            self.original_masks = []
            #load the textures

            self.load_masks(flags)

        

    def load_texture(self):

        def load_skin(path: str):
            with WandImage(filename=filepath) as image:
                image.compression = "no"
                image = cv.cvtColor(np.asarray(image), cv.COLOR_RGB2BGR)
                image = Image.fromarray(np.asarray(image))
            #image = Image.open(os.path.join(os.getcwd(), filenames[choice]), 'r')
            
            return image

        for idx, filepath in enumerate(self.texture_names.paths):
            #send texture to GL
            self.textures.append(glGenTextures(1))
            glBindTexture(GL_TEXTURE_2D, self.textures[idx])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                            GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

            #with Image.open(filepath, mode="r") as image:
            with WandImage(filename=filepath) as image:
                image.compression = "no"
                # image2 = np.array(image)
                # show_image(image2)
                image = Image.fromarray(np.asarray(image))
                self.image = image
                image_width, image_height = image.size
                #image = image.convert("RGBA")
                img_data = bytes(image.tobytes())
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width,
                            image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            glGenerateMipmap(GL_TEXTURE_2D)


    def get_modifiers(self, word, shuffle_params):

        if word == self.mask_type[0]: #dots
            brush_size = shuffle_params[1]
            do_period = shuffle_params[3]
        elif word == self.mask_type[1]: #blobs
            brush_size = shuffle_params[0]
            do_period = shuffle_params[2]
        return [brush_size, do_period, shuffle_params[4], shuffle_params[5]]
    
    def load_masks(self, flags: config.Flags):
        #without threads this takes 30 seconds, the gain is probably in multiple cython threads
        start = glfw_get_time()
        mask_queue = Buff_queue()
        # we shouldn't read from the same file... right ?
        # instead of passing species pass values that species is used for 

        if (len(config.SPECIES_IN_ROTATION) == 1) or (flags.use_threads_flag == False):
            for idx, species in enumerate(config.SPECIES_IN_ROTATION):
                self.read_mask(
                    idx, species, flags, mask_queue)
        else:
            threads = []
            for idx, species in enumerate(config.SPECIES_IN_ROTATION):
                # load each mask for each species
                #self.Skin_modifier = Skin_params(species)
                #path = f"masks/{species}"
                t = Thread(target=self.read_mask, args=(idx, species, flags, mask_queue))
                threads.append(t)
                t.start()

            for thread in threads:
                thread.join()

        species_masks = list(range(mask_queue.qsize()))
        original_masks = list(range(mask_queue.qsize()))
        while not mask_queue.empty():
            # sort it and append to object list
            mask = mask_queue.get()
            idx = mask[0]
            s_mask = mask[1]
            o_mask = mask[2]
            species_masks[idx] = s_mask
            original_masks[idx] = o_mask
            # load texture masks for colored spots
        # self.masks.append(species_masks)
        # self.original_masks.append(original_masks)
        self.masks = species_masks
        self.original_masks = original_masks
            
        end = glfw_get_time()
        print(f"Generated masks in {end - start} seconds")

    def read_mask(self,idx:int ,species: int, flags: config.Flags, queue: Buff_queue):
        
        np.random.default_rng(seed=None)
        species_masks = []
        original_masks = []
        # if species not in config.SPECIES_IN_ROTATION:
        #     pass
        #     #species_masks.append(None)
        #     #original_masks.append(None)
        #     #queue.put([species, None, None])
        # else:
        print(f"Loaded mask: {species}")
        Skin_modifier = Skin_params(species)
        type = None
        path = f"masks/{species}"
        for filename in sorted(glob(os.path.join(path, '*.png'))):
            with Image.open(os.path.join(os.getcwd(), filename), 'r') as image:
                image = image.convert("RGBA")
                original_img = image
                image_width, image_height = image.size
                for word in self.mask_type:
                    if word in filename:
                        type = word
                        red, green, blue, alpha = Image.Image.split(
                            image)
                        shuffle_params = self.get_modifiers(
                            word, Skin_modifier.shuffle_params)
                        new_alpha = self.texture_shuffle(
                            alpha, shuffle_params, flags)
                        image = Image.merge(
                            'RGBA', (red, green, blue, new_alpha))
                img_data = [bytes(image.tobytes()),
                            image_width, image_height, type]
                original_img_data = [original_img,
                                        image_width, image_height, type]
                species_masks.append(img_data)
                original_masks.append(original_img_data)
        queue.put([idx, species_masks, original_masks])
    

    def update_mask(self, flags:config.Flags, idx_species: int ,species: int):
        '''
        Without threads it takes 22 seconds, since its all python commands the impovement is negligible 
        or it's even worse than single thread
        texture shuffle can't iterate it's function over the same mask several times ,
        therefore the need for the original masks which get deformed differently every time
        '''
        start = glfw_get_time()
        mask_queue = Buff_queue()
        # we shouldnt read from the same file... right ?
        
       

        if (len(config.SPECIES_IN_ROTATION) == 1) or (flags.use_threads_flag == False):
            for species_masks, species in zip(self.masks, config.SPECIES_IN_ROTATION):
                self.shuffle_mask_main(
                    species_masks, idx_species, species, flags)
        else:
            threads = []
            for species_masks, species in zip(self.masks, config.SPECIES_IN_ROTATION):
                # load each mask for each species
                t = Thread(target=self.shuffle_mask, args=(
                    species_masks, idx_species, species, flags, mask_queue))
                threads.append(t)
                t.start()

            for thread in threads:
                thread.join()

            while not mask_queue.empty():
                i, j, img_data = mask_queue.get()
                self.masks[i][j][0] = img_data 


        end = glfw_get_time()
        print(f"Updated masks in {end - start} seconds")

    def shuffle_mask_main(self, species_masks , idx_species: int, species: int, flags: config.Flags):
        
        Skin_modifier = Skin_params(species)
        for i, image_data in enumerate(self.original_masks[idx_species]):
            for word in self.mask_type:
                if word == image_data[3]:
                    red, green, blue, alpha = Image.Image.split(
                        image_data[0])
                    shuffle_params = self.get_modifiers(
                        word, Skin_modifier.shuffle_params)
                    new_alpha = self.texture_shuffle(
                        alpha, shuffle_params, flags)
                    image = Image.merge(
                        'RGBA', (red, green, blue, new_alpha))
                    img_data = bytes(image.tobytes())
                    species_masks[i][0] = img_data

    def shuffle_mask(self, species_masks,  idx_species: int, species: int, flags: config.Flags, queue: Buff_queue):
        
        def update(mask, word, idx):
            red, green, blue, alpha = Image.Image.split(
                        mask)
            shuffle_params = self.get_modifiers(
                word, Skin_modifier.shuffle_params)
            new_alpha = self.texture_shuffle(
                alpha, shuffle_params, flags)
            image = Image.merge(
                'RGBA', (red, green, blue, new_alpha))
            img_data = bytes(image.tobytes())
            queue.put([idx_species, idx, img_data])
            
        Skin_modifier = Skin_params(species)
        [update(image_data[0], image_data[3], idx)
          for idx, image_data in enumerate(self.original_masks[idx_species])
          if image_data[3] is not None]
            #[update(image_data[3]) if image_data[3] is not None else '' for word in self.mask_type]
            # for word in self.mask_type:
            #     if word == image_data[3]:
                    
            #         #species_masks[i][0] = img_data


    def use_masks(self, idx_species: int):
        #reset
        glDeleteTextures(len(self.active_masks), self.active_masks)
        self.active_masks = []
        for i, image_data in enumerate(self.masks[idx_species]):
            if image_data == None:
                pass
            else:
                image = image_data[0]
                image_width = image_data[1]
                image_height = image_data[2]
                
                self.active_masks.append(glGenTextures(1))
                glBindTexture(GL_TEXTURE_2D, self.active_masks[i])
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width,
                            image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        
        
    def use_textures(self):
        loaded_textures = self.textures + self.active_masks
        for i in range(len(loaded_textures)):
            glActiveTexture(GL_TEXTURE0 + i)
            glBindTexture(GL_TEXTURE_2D, loaded_textures[i])
        
    def update_texture(self):
        '''
        this function simply changes to  different skin, greyscale for lizard from 
        folder.
        These new skins are generated separately
        '''

        #new texture image
    
        while self.alternate_skins.empty():
            # wait for load_alternate to finish
            time_sleep(1)   
        # 4k, bump, smoothnesss
        # these are mapped to the first three textures
        texture_maps = self.alternate_skins.get()

        for i, image in enumerate(texture_maps):

            glBindTexture(GL_TEXTURE_2D, self.textures[i])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                            GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            image_width, image_height = image.size
            image = image.convert("RGBA")
            img_data = bytes(image.tobytes())
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width,
                        image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            glGenerateMipmap(GL_TEXTURE_2D)

    def texture_shuffle(self, image, shuffle_params, flags: config.Flags):

    
        arr_size = image.size
        # pick random points
        candidates = np.argwhere(np.asanyarray(image) > 0.1) #0.1 alpha value
        crop = len(candidates) * randomf_range(0.005, 0.01)#random.uniform(0.001, 0.01)
        N = np.random.randint(crop)
       
        candidates = choices(candidates, k = int(N))
        #candidates = np.array([x for x in candidates[choose_random]])
        candidates = np.array(sorted(candidates, key=itemgetter(1)))
 
  
        # create new alpha channel for "Random" skin coloring
        alpha = np.zeros(arr_size, dtype=np.uint8)
        # cython is slightly faster, but is still terrible
        if flags.use_cython == True:
            self.ival = 0
            for x in candidates:
                self.ival = draw_alpha.draw_point(alpha, x, shuffle_params, N, self.ival)
            self.ival = 0
        else:
            [self.draw_points(alpha, x, shuffle_params, N) for x in candidates]

        alpha = cv.flip(cv.rotate(cv.cvtColor(alpha, cv.COLOR_BGR2RGBA), cv.ROTATE_90_COUNTERCLOCKWISE), 0)
        alpha = (alpha-np.min(alpha)) / \
            (np.max(alpha)-np.min(alpha))
        alpha = Image.fromarray(np.uint8(alpha)*255).convert('L')

        return alpha

    def draw_points(self, alpha, x, shuffle_params, N):

    
        i_val = 0
        n_erode = 0; n_dilate = 0
        brush_size = shuffle_params[0]
        do_period = shuffle_params[1]
        do_dilate = shuffle_params[2]
        do_erode = shuffle_params[3]


        radius = np.random.randint(
            1, int(brush_size)) if brush_size > 1 else 0
        i = np.random.randint(1, 50)
        j = np.random.randint(1, 20)
        weight = np.cos(i_val*np.pi)
        if weight > 0:
            alpha = cv.circle(alpha, x, radius, color=(
                255, 255, 255, 255), thickness=-1)

            if do_dilate == 1:

                alpha[x[0]-i:x[0]+i, x[1]-j:x[1]+j] = cv.dilate(
                    alpha[x[0]-i:x[0]+i, x[1]-j:x[1]+j], np.ones((7, 7), np.uint8))
                n_dilate += 1

            i_val += brush_size * 1/N * do_period
        elif weight < 0:
            if do_erode == 1:
                alpha[x[0]-i:x[0]+i, x[1]-j:x[1]+j] = cv.erode(
                    alpha[x[0]-i:x[0]+i, x[1]-j:x[1]+j], np.ones((21, 21), np.uint8))
                n_erode += 1

            i_val += brush_size * 1/N * do_period


    def destroy(self):

        glDeleteTextures(len(self.textures), self.textures)
        glDeleteTextures(len(self.active_masks), self.active_masks)
        # for x in self.masks:
        #     if x == None:
        #         continue
        #     else:
        #         glDeleteTextures(len(self.masks), self.masks)





class Animate_model:

    def __init__(self, shader, frame_half_period, frame_number, models):

        self.base_models = models
        self.original_frames, self.models = self.get_frame_array(
            frame_half_period, frame_number, models)
        self.frames = [x for x in self.original_frames]
        #this should be shader for lizard object
        self.shader = shader
        glUseProgram(shader)
        
        self.frame = 0
        self.frame_idx = 0

        #volume adjustment parameters
        self.switched_models = 0
        self.breath_volume_max = config.BREATH_VOLUME_MAX
        self.original_breath_volume_min = config.ORIGINAL_BREATH_VOLUME_MIN
        self.breath_volume_min = config.BREATH_VOLUME_MIN
        self.exhale_increment = config.EXHALE_INCREMENT #* 1.75
        self.inhale_increment = config.INHALE_INCREMENT #* 0.75
        self.hold_breath = 1
        self.periods_till_exhale = config.NUMBER_OF_PERIODS//2
        self.period  = 0
        self.smooth_transition = False
        self.smooth_counter = 0


        #interpolation variables for animation, cubic bezier has 2 inbetween points, 
        # but we calculate third as the "middle " between the two
        self.middle_point_change =  config.MIDDLE_POINT_CHANGE
        self.first_point_change = config.FIRST_POINT_CHANGE
        self.second_point_change = config.SECOND_POINT_CHANGE

        self.previousModel = self.models[0]
        self.nextModel = self.models[1]

        self.vertices = self.models[0].vertices
        self.vertices_structure = self.models[0].vertices_structure
        self.vertices_structure_count = self.models[0].vertices_structure_count
        self.maxFrame = self.frames[-1]
        self.vertex_count = len(
             self.vertices)//len(self.vertices_structure)


        # glsl parameters
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.previousModel.vertices.nbytes,
                     self.previousModel.vertices, GL_STATIC_DRAW)

        n_bytes = 4
        byte_offset = 0
        total_bytes = int(len(self.vertices_structure) * n_bytes)
        attribute = 0
        for i, n_var in enumerate(self.vertices_structure_count):
            attribute = i
            glEnableVertexAttribArray(attribute)
            glVertexAttribPointer(
                attribute, n_var, GL_FLOAT, GL_FALSE, total_bytes, ctypes.c_void_p(byte_offset))
            byte_offset += n_var * n_bytes
            
        n_bytes = 4
        byte_offset = 0
        self.vbo_next = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_next)
        glBufferData(GL_ARRAY_BUFFER, self.nextModel.vertices.nbytes,
                     self.nextModel.vertices, GL_STATIC_DRAW)
        attribute += 1
        attribute2 = attribute
        for i, n_var in enumerate(self.vertices_structure_count):
            attribute2 = attribute + i
            glEnableVertexAttribArray(attribute2)
            glVertexAttribPointer(
                attribute2, n_var, GL_FLOAT, GL_FALSE, total_bytes, ctypes.c_void_p(byte_offset))
            byte_offset += n_var * n_bytes
        

        
        # self.vao = glGenVertexArrays(1)
        # glBindVertexArray(self.vao)
        # self.vbo = glGenBuffers(1)
        # glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        # glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes,
        #                 self.vertices, GL_STATIC_DRAW)
        # self.vertexCount = int(len(self.vertices)/8)
       
        # # position attribute
        # glEnableVertexAttribArray(0)
        # glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE,
        #                         self.vertices.itemsize*8, ctypes.c_void_p(0))
        # #texture attribute
        # glEnableVertexAttribArray(1)
        # glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE,
        #                         self.vertices.itemsize*8, ctypes.c_void_p(12))
        # # normal attribute
        # glEnableVertexAttribArray(2)
        # glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE,
        #                         self.vertices.itemsize*8, ctypes.c_void_p(20))
        

    def update(self, frametime, flags: config.Flags):
        #animation speed  rate
        inc = self.inhale_increment if self.switched_models else self.exhale_increment
        self.frame += inc
        if (self.frame == (self.maxFrame - config.PER_FRAME_INCREMENT)):
            flags.last_frame_flag = True

        if (self.frame >= self.maxFrame) or (flags.lines_full_flag == True):
            flags.period_flag = True
            #self.frame -= (self.maxFrame - 1)
            self.frame = 1 
            self.switched_models = 0
            self.frame_idx = 0
            #self.breath_volume_min = self.original_breath_volume_min

            

    def get_frame_array(self, frame_half_period, frame_number, model):
        frames = []
        models = []
        if frame_half_period < 1:
            frame_half_period = 1
        if frame_number < 1:
            frame_number = 1
        # times 2 because [inhale exhale inhale] the exhale and inhale are the 2 
        # even frame_number gives even breath ending, odd ends on exhale and is normal period
        #frame_range =  frame_number*3 if int(frame_number)%2 else  frame_number*3 -1 

        percent = randomf_range(0, 0.45)

        for i in range(0,int(frame_number + 1)):

            self.exhale_frame_extension = config.BREATH_HALF_PERIOD#*0.5 - config.BREATH_HALF_PERIOD*percent
            self.inhale_frame_extension = config.BREATH_HALF_PERIOD#*0.5 + config.BREATH_HALF_PERIOD*percent

            if i%2 == 0:
                frames.append(int(self.exhale_frame_extension * i))
                #exhale
                models.append(self.base_models[0])
            else:

                frames.append(int(self.inhale_frame_extension * i))
                #inhale
                models.append(self.base_models[1])
        return frames, models

    ##PREVIOUS VERSIONS NOW REALIZED IN SHADER
    # def model_shuffle(self):
    #     rand_T = random.randint(1, 3)
    #     rand_A = random.randint(10,15)
    #     rand_uv = np.random.random()
    #     uv_start = random.randint(3, 4)
    #     nth = 1
    #     bend_x = self.get_bend_param(
    #          self.base_models[0].vertices, self.base_models[0].vertices, rand_T, rand_A, nth)

       
    #     for model in self.base_models[0:2]:
    #         self.uv_shuffle(model.vertices, model.original_vert, rand_uv, uv_start)
    #         # bend_x = self.get_bend_param(
    #         #     model.vertices, model.vertices, rand_T, rand_A)
    #         model.vertices[2::8*nth] = model.original_vert[2::8*nth] + bend_x
           
    ##THIS SECTION HAS BEEN MOVED TO SHADER
    # def uv_shuffle(self, vertices, original_uv, rand_uv, uv_start):
    #     # slightly shuffle the uv vertices, more variety kinda...
    #     # this is wrong, we do this for every model randomly, move the random into model_shuffle
    #     a = -0.0009
    #     b = 0.0009
    #     rnd = a + (b - a) * rand_uv
    #     vertices[uv_start::8] =  original_uv[uv_start::8] + np.float32(a + (b - a) * np.full((vertices[uv_start::8].size), rnd))

    ##THIS SECTION HAS BEEN MOVED TO SHADER
    # def get_bend_param(self, vertices, original_shape: np.array, rand_T, rand_A, nth):
    #     #bending is on of the more compicated things, leave it to blender...
    #     rand_T = 1
    #     # format of vertices
    #     # x, y, z, s ,t, nx, ny, nz
    #     # we want to apply slight curve to the model by changing its x coordinate
    #     # this is achievied by using sin or cos wiht all x coordinates
    #     x_coord = original_shape[1::8*nth]
    #     #y_coord = original_shape[0::8]
    #     #x_coord = np.unique(x_coord)
    #     #max_y = x_coord.max()
    #     #min_y = x_coord.min()
    #     x_norm = 2 * (x_coord - np.min(x_coord))/np.ptp(x_coord) - 1
    #     #x_norm = np.sort(x_norm)
    #     x_trans = 1 * np.cos(x_norm * np.pi * 2)
    #     return x_trans
      
    def to_shader_animation_params(self):

        #pass animation parameters to shader for calculation
        glUseProgram(self.shader)

        #used as a bool indicating switc between models
        glUniform1i(glGetUniformLocation(self.shader, "AnimParams.switched"),
                    self.switched_models)
        
        glUniform1f(glGetUniformLocation(self.shader, "AnimParams.breath_volume_max"),
                    np.float32(self.breath_volume_max))
        
        glUniform1f(glGetUniformLocation(self.shader, "AnimParams.breath_volume_min"),
                    np.float32(self.breath_volume_min))
        
        #bezier interpolation values
        glUniform1f(glGetUniformLocation(self.shader, "AnimParams.mid_point_change"),
                    np.float32(self.middle_point_change))
        glUniform1f(glGetUniformLocation(self.shader, "AnimParams.first_point_change"),
                    np.float32(self.first_point_change))
        glUniform1f(glGetUniformLocation(self.shader, "AnimParams.second_point_change"),
                    np.float32(self.second_point_change))

        glUniform1f(glGetUniformLocation(self.shader, "t"),
                    np.float32(self.t))
        #load new vertices data to shader
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        memoryHandle = glMapBuffer(GL_ARRAY_BUFFER, GL_WRITE_ONLY)
        ctypes.memmove(ctypes.c_void_p(memoryHandle), ctypes.c_void_p(self.previousModel.vertices.ctypes.data),  self.previousModel.vertices.nbytes)
        glUnmapBuffer(GL_ARRAY_BUFFER)
                
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo_next)
        memoryHandle = glMapBuffer(GL_ARRAY_BUFFER, GL_WRITE_ONLY)
        ctypes.memmove(ctypes.c_void_p(memoryHandle), ctypes.c_void_p(self.nextModel.vertices.ctypes.data),  self.nextModel.vertices.nbytes)
        glUnmapBuffer(GL_ARRAY_BUFFER)


    def update_breath_volume(self):
        self.period = 0
        self.hold_breath = 0
        #should be called from render when period flag is true
        #if flags.period_flag:
        # usually lizards hold their breath then suddenly exhale, while their chest slighly quivers
        # you can simulate this with small breath period while having this "hard" exhale separate 
        # self.nervous = np.random.randint(0,2)
        # if self.nervous:
        #     self.periods_till_exhale = np.random.randint(config.NUMBER_OF_PERIODS//4, config.NUMBER_OF_PERIODS//2)
        # else:
        #     self.periods_till_exhale = np.random.randint(config.NUMBER_OF_PERIODS//2, config.NUMBER_OF_PERIODS)


    def update_animation_params(self, flags: Flags):
        # when exhale or inhale finishes we can change the opposite parameters
        #self.frames = self.original_frames

        if (config.BREATH_VOLUME_RANDOMIZE) and (self.switched_models):
            #we just finished exhaling, make changes for next exhale
           
            if (not self.hold_breath) :
                self.breath_volume_min = randomf_range(-0.45, 1)
            elif (self.hold_breath):
                self.breath_volume_min = randomf_range(config.BREATH_VOLUME * 0.9, config.BREATH_VOLUME * 0.92)

            if (config.BREATH_HALF_PERIOD_RANDOMIZE):
                #self.frames[self.frame_idx + 1:] = [x + np.random.randint(0,config.BREATH_HALF_PERIOD - 1) for x in self.original_frames[self.frame_idx + 1:]]
                self.middle_point_change = randomf_range(0.25, 0.45)
                self.first_point_change = randomf_range(0.25, 0.45)

        elif (config.BREATH_VOLUME_RANDOMIZE) and (not self.switched_models):
            #we just finished inhaling, make changes for next inhale
            
            if (not self.hold_breath):
                self.breath_volume_max = randomf_range(config.BREATH_VOLUME * 0.85, config.BREATH_VOLUME* 1.25)
            elif (self.hold_breath):
                self.breath_volume_max = randomf_range(
                      config.BREATH_VOLUME * 0.94, config.BREATH_VOLUME * 0.95)
                
            if (config.BREATH_HALF_PERIOD_RANDOMIZE):
                #self.frames[self.frame_idx + 1:] = [x - np.random.randint(0,config.BREATH_HALF_PERIOD - 1) for x in self.frames[self.frame_idx + 1:]]
                self.middle_point_change = randomf_range(0.85, 0.95)
                self.second_point_change = randomf_range(0.95, 1)
        else:
            print(f"Update_animation_params: state {self.switched_models} isn't an option" )

        self.period = (self.period + 1) if (self.period <=
                                            (config.NUMBER_OF_PERIODS//2)) else config.NUMBER_OF_PERIODS//2
        #self.hold_breath = np.random.randint(0,config.NUMBER_OF_PERIODS//2)
        self.hold_breath = np.random.randint(0, self.period)
        # self.hold_breath_previous = self.hold_breath
       
        # if (not self.smooth_transition):
           
        #     #self.hold_breath = np.random.randint(0,config.NUMBER_OF_PERIODS//2)
        #     self.smooth_transition = False if self.throw else True
        # else:
        #     self.hold_breath = 1
            
          

        # if not (self.hold_breath and self.hold_breath_previous):
        #     self.smooth_inhale = True
        #if (not self.switched_models):
            # if self.period == self.periods_till_exhale:
            #     self.hold_breath = 0
            #     self.period = 0
            # else:
            #     self.hold_breath = 1
            # self.period += 1
            


    def draw(self, scale, flags):
        
   
        #find next and previous frames
        previousFrame = self.frames[len(self.frames) - 1]
        self.previousModel = self.models[len(self.frames) - 1]
        nextFrame = self.frames[0]
        self.nextModel = self.models[0]
        for i in range(len(self.frames)):
            if self.frames[i] > self.frame:
                 
                previousFrame = self.frames[i - 1]
                self.previousModel = self.models[i - 1]
                nextFrame = self.frames[i]
                self.nextModel = self.models[i]
                break
            elif self.frames[i] == self.frame:
                
                #indicate that models have been switched
                self.switched_models = 1 if (self.switched_models == 0) else 0
                #with ongoing breaths the min should stabilize
                check1 = (self.breath_volume_min + abs(self.original_breath_volume_min) * 0.5) < 1
                self.frame_idx += 1
                self.update_animation_params(flags)
            
        # if (self.smooth_transition) and (not self.switched_models):
        #     #exhale
        #     if self.breath_volume_min >= (config.BREATH_VOLUME/2):
        #         self.breath_volume_min -= 0.01 
        #         self.breath_volume_max = self.breath_volume_min
        #     else:
        #         self.smooth_counter += 1
        # if (self.smooth_transition) and (self.switched_models):
        #     #inhale
        #     if (self.breath_volume_max >= (config.BREATH_VOLUME/2)) and (self.breath_volume_max <= (config.BREATH_VOLUME)):
        #         self.breath_volume_max += 0.01 
        #         self.breath_volume_min = self.breath_volume_max
        #     else:
        #         self.smooth_counter += 1
        # if self.smooth_counter >= 2:
        #     self.smooth_counter = 0
        #     self.smooth_transition = False
        #     self.hold_breath = 0 
            
                

                
        
        ##THIS SECTION HAS BEEN MOVED TO SHADER
        #attempt at bezier interpolation
        self.t = (self.frame - previousFrame) / (nextFrame - previousFrame)
        # p_middle = previousModel.vertices + (nextModel.vertices - previousModel.vertices) * 0.5
        # p_middle_1 = previousModel.vertices + (p_middle - previousModel.vertices) * 0.25
        # p_middle_2 = p_middle + (nextModel.vertices - p_middle) * 0.75

        # T = np.array([1, t, t**2, t**3], dtype=np.float32)

        # M = np.array([[1, 0, 0, 0],
        #      [-3, 3, 0, 0],
        #      [3, -6, 3, 0],
        #     [-1, 3, -3, 1]], dtype=np.float32)
        
        # P = np.array([previousModel.vertices,
        #              p_middle_1,
        #              p_middle_2,
        #              nextModel.vertices], dtype=np.float32)
        # self.vertices = T @ M @ P
        # TM = np.dot(T,M)
        # self.vertices = np.dot(TM,P)

        #linear interpolation between frames, getting pizza like distortion on image
        # interpolationAmount = (self.frame - previousFrame) / (nextFrame - previousFrame)
        # self.vertices = (1 - interpolationAmount) * previousModel.vertices + interpolationAmount * nextModel.vertices
      
        self.to_shader_animation_params()
    
    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,self.vbo_next))
        for model in self.base_models:
            model.destroy()


