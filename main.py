import sfml
import constants

class Main:
    def __init__(self):
        self.window = sfml.RenderWindow(sfml.VideoMode(800, 600), title = "Parallax Test")
        self.window.framerate_limit = 30 #prevent 100% cpu usage
        self.bgs = [sfml.Sprite(sfml.Texture.load_from_file("sprites/montane/montane%i.png" % i)) for i in range(8)]
        for background in self.bgs:
            background.scale = (6,6)
            
        self.window_focused = True
        
        self.view_height = constants.VIEW_HEIGHT
        self.view_width = constants.VIEW_WIDTH
        
        
        #direct middle of map
        map_width_middle = self.bgs[0].global_bounds.width/2
        map_height_middle = self.bgs[0].global_bounds.height/2
        
        self.camera_x = map_width_middle
        self.camera_y = map_height_middle
        
        self.foreground = self.bgs[0]
        self.background = self.bgs[7]
        
        #list to be rendered in order by the renderer
        self.backgrounds = []
        
    def step(self):
        
        while (True):
            if self.handle_input() == False:
                return(False)
            self.render()
            
    def render(self):
        self.xview = int(int(self.camera_x) - self.view_width / 2)
        self.yview = int(int(self.camera_y) - self.view_height / 2)
        
        self.clean_rendering_lists()
        
        
        #Background (Sky)
        self.position_map(self.bgs[7])
        self.window.draw(self.bgs[7])
        
        #Backgrounds in between
        parallaxed_maps = [self.bgs[i] for i in range(1, 7)]
        parallaxed_maps.reverse()
        self.parallax_map (parallaxed_maps)
        
        #Foreground
        self.position_map(self.bgs[0])
        self.window.draw(self.bgs[0])
        
        #Render everything
        self.window.display()
        
    def get_screen_coords(self, x, y):
        # calculate drawing position
        draw_x = int(x - self.xview)
        draw_y = int(y - self.yview)

        return draw_x, draw_y
    def position_map (self, map_sprite):
        map_sprite.position = (-self.xview, -self.yview)
        
    def parallax_map (self, map_sprites):
        #the list passed to this function are the sprites between the foreground and background
        speed_increment = 1.0/len(map_sprites)
        for iteration, background in enumerate(map_sprites):
            multiplier = speed_increment * iteration
            background.position = (-self.xview* multiplier, -self.yview * ((multiplier+1.0)/2))
            self.window.draw(background)
    
    def handle_input(self):
        for event in self.window.iter_events():
            if event.type == sfml.Event.CLOSED: #Press the 'x' button
                return False
            if event.type == sfml.Event.LOST_FOCUS:
                self.window_focused = False
            if event.type == sfml.Event.GAINED_FOCUS:
                self.window_focused = True
            if event.type == sfml.Event.KEY_PRESSED: #Key handler
                if self.window_focused:
                    if event.code == sfml.Keyboard.ESCAPE:
                        return False
                    if event.code == sfml.Keyboard.W:
                        self.camera_y -= 10
                    if event.code == sfml.Keyboard.S:
                        self.camera_y += 10
                    if event.code == sfml.Keyboard.A:
                        self.camera_x -= 10
                    if event.code == sfml.Keyboard.D:
                        self.camera_x += 10
    def clean_rendering_lists(self):
        self.backgrounds = []
#create the object and run the step
runner = Main()
runner.step()