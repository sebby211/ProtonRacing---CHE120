import pygame #AS: Imports all of the available pygame modules into the program
import sys #AS: Imports the sys module
import time #AS: Imports the time module
import math #AS: Imports math module
#hi 
pygame.init() #AS: Used to avoid any issues related to uninitalized modules by ensuring pygame modules function correctly within the program 

screen = pygame.display.set_mode((1280, 720)) #AS: Sets up the main window using the parameters of the given width and height tuple

BLACK = (0, 0, 0) #AS: All of these set variables(colours) are set to defined RGB models as tuple values 
WHITE = (255, 255, 255)  
GREEN = (0, 255, 0)
RED = (255, 0, 0)

font = pygame.font.Font('supfont.ttf', 90) #AS: The variable is set to a function with the parameters of a given TrueType file and size (this will be the larger sized font)
 
small_font = pygame.font.Font('supfont.ttf', 50) #AS: The variable is set to a function with the parameters of a given TrueType file and size (this will be the smaller sized font)

menu_options = ["Start Game", "Audio", "Quit"] #AS: Establishes a variable name with a list of string values to be used in the main menu screen
pause_screen_options = ["Resume", "Quit"] #AS: Establishes a variable name with a list of string values to be used in the pause menu screen
music_playing = True  #AS: Sets this to be true when game opens (basically, it allows this to start off true, and then set to false later)

speaker_on_image = pygame.image.load('speaker_on.png') #AS: Sets the variable to load an image file by creating a surface object from the given png file (used as the audio on the speaker)
speaker_off_image = pygame.image.load('speaker_off.png') #AS: Also sets the variable to load an image file by creating a surface object from the given png file (used as the audio mute speaker)
speaker_on_image = pygame.transform.scale(speaker_on_image, (50,50)) #AS: These two functions rescale the previously loaded images by calling the surface objects and the desired tuple size as arguments
speaker_off_image = pygame.transform.scale(speaker_off_image, (50,50)) 
speaker_icon_x = 800  #AS: Establishes the x-coordinate for placing the speaker icon
speaker_icon_y = 205  #AS: Establishes the y-coordinate for placing the speaker icon

track_image = pygame.image.load('tracknew.png') #AS: Loads the given png file into the program by creating a surface object
car_image = pygame.image.load('carnew.png') #AS: Also loads the given png file into the program by creating a surface object
track_image = pygame.transform.scale(track_image, (1280, 720)) #AS: Rescales the surface object 'track_image' using the given tuple size 
track_pixels = pygame.surfarray.array3d(track_image) #AS: Creates an array of pixels that defines the pixels that make-up the track
track_colour = (84, 84, 84) #AS: Defines the track colour using RGB|values, in this case it is a shade of grey, and is important for track definition
screen = pygame.display.set_mode((track_image.get_width(), track_image.get_height())) #AS: Defines the boundaries of the screen with the image of the track screen (ensures no black space)
car_x, car_y = 968, 225  #AS: Establishes the car's initial starting position when the game is run as a tuple 

crash_sound = pygame.mixer.Sound('gameoversoundeffect.mp3') #AS: Defines the crash sound using pygame's mixer.Sound class and an imported mp3 file
start_time = None

class Car:
    def __init__(self, pygame):
        self.sizey = 20
        self.sizex = 50
        self.position = pygame.Vector2(1075, 350)
        self.shape = pygame.image.load('carnew.png')
        self.image = self.shape
        self.velocity = 0
        self.acceleration = 0.006
        self.rotation = 0
        self.cornering = 0.4
        self.topspeed = 2
        
    def update_position(self, math):
        self.position = pygame.Vector2(self.position.x + (math.sin(math.radians(self.rotation)))*self.velocity, self.position.y + (math.cos(math.radians(self.rotation))*self.velocity))
    def update_rotation_left(self):
        self.rotation += self.cornering
    def update_rotation_right(self):
        self.rotation -= self.cornering
    def goforwardvelocity(self):
        if self.velocity >= self.topspeed*(-1):
            self.velocity -= self.acceleration
    def gobackwardvelocity(self):
        if self.velocity <= self.topspeed:
            self.velocity += self.acceleration
    def update_image(self, math, pygame):
        self.update_position(math)
        image = pygame.transform.rotate(self.image, self.rotation)
        screen.blit(image, self.position)
                    
n = Car(pygame)

def start_count_down():
    count_down_messages = ["3", "2", "1", "Go!"] #AS: A homogenous string list is defined as to a variable name (this list includes the text that will show on the screen during the countdown)
    for number in count_down_messages: #AS: Consists of a for loop that goes through each item within the list
        screen.blit(track_image, (0, 0)) #AS: This will display the track image through each iteration 
        text = font.render(number, True, WHITE) #AS: Here a variable is set to a specific font (font was established earlier in the program), and the established tuple, WHITE. The eterated values are to be set as arguments within the render function as well.  
        screen.blit(text, (600,325)) #AS: This allows the text variable above to be postioned and surfaced onto the screen, using a specific position tuple as an argment.
        pygame.display.update() #AS: Updates the display every iteration. 
        time.sleep(1) #AS: Pauses the loop for a second between each iteration, allowing the coundown to flow smoothly. 
global times_list
times_list = [0]   

def display_timer(carobject, lap, moved, start_time):
    if start_time is not None:
        elapsed_time = time.time() - start_time
        minutes = int(elapsed_time) // 60
        seconds = int(elapsed_time) % 60
        timer_text = f"{minutes:02}:{seconds:02}"
        text = small_font.render(timer_text, True, WHITE)
        screen.blit(text, (20, 20))
        x,y = carobject.position
        if int(x) > 1000 and int(x) < 1150 and int(y) == 350 and moved:
            if times_list[0] == 0:
                times_list[0] = elapsed_time
            times_list.append(elapsed_time)
            start_time = time.time()
            lap += 1
            moved = False
        lap_text = small_font.render('LAP: ' + str(lap), True, WHITE)
        screen.blit(lap_text, (1050, 10))
        w = min(times_list)
        w = ("%.2f" % w)
        w = str(w)
        w = w.split('.')
        if w[0] == 0:
            w = ['0','00']
        output = 'Best LAP: ' + str(w[0])+':'+ str(w[1])
        best_text = small_font.render(output, True, WHITE)
        screen.blit(best_text, (790, 50))
        return lap, moved, start_time
        
pause_menu_option_y_positions = [360, 420]

def pause_menu():
    selected_option = 0 
    paused = True 
    while paused:
        for event in pygame.event.get(): 
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_w: 
                    selected_option = (selected_option - 1) % 3 
                elif event.key == pygame.K_s: 
                    selected_option = (selected_option + 1) % 3 
                elif event.key == pygame.K_RETURN: 
                    if selected_option == 0: 
                        paused = False
                    elif selected_option == 1: 
                        pygame.quit()
                        sys.exit()

        pause_menu_image = pygame.image.load('pausemenuimage.png') 
        pause_menu_image = pygame.transform.scale(pause_menu_image, (1280, 720)) 
        screen.blit(pause_menu_image, (0,0)) 
        title = font.render("Paused", True, WHITE) 
        screen.blit(title, (455, 240)) 
        
        i = 0 
        for option in pause_screen_options: 
            if i == selected_option: 
                if i == 0: 
                    colour = GREEN
                elif i == 1: 
                    colour = RED
            else: 
                colour = WHITE 
            text = small_font.render(option, True, colour) 
            screen.blit(text, (540, pause_menu_option_y_positions[i])) 
            
            i += 1 
            
        pygame.display.update() 
        
gameover_menu_option_y_positions = [150, 210, 270]
        
def gameover_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.quit()
                        sys.exit()
        
        background_image = pygame.image.load('demo_car.png')
        background_image = pygame.transform.scale(background_image, (1280, 720))
        screen.blit(background_image, (0, 0))

        title = font.render("Game Over", True, RED)
        screen.blit(title, (330, 50)) 
                     
        text = small_font.render("Quit", True, GREEN) 
        screen.blit(text, (550, 200))
            
        pygame.display.update()
        

menu_option_y_positions = [150, 210, 270] 
def draw_menu(selected_option):
    background_image = pygame.image.load('test10car.png') 
    background_image = pygame.transform.scale(background_image, (1280,720)) 
    screen.blit(background_image, (0, 0))  
    title = font.render("Proton Racing", True, WHITE) 
    screen.blit(title, (250, 50))   

    i = 0 
    for option in menu_options:
        if i == selected_option:   
            if i == 2: 
                colour = RED
            else: 
                colour = GREEN 
        else: 
            colour = WHITE
        if option == "Audio": 
            if music_playing: 
                option = "Audio: On" 
            else:
                option = "Audio: Off"   
                
        text = small_font.render(option, True, colour) 
        screen.blit(text, (460, menu_option_y_positions[i])) 
        
        i += 1 

    if music_playing: #AS: Set as a boolean, (aka if True)
        screen.blit(speaker_on_image, (speaker_icon_x, speaker_icon_y)) #AS: Blit image on screen, make a speaker_on png to appear with a respective position
    else: #AS: aka False
        screen.blit(speaker_off_image, (speaker_icon_x, speaker_icon_y)) #AS: Blit image on screen, make a speaker_off png to appear with a respective position 
    pygame.display.update() #AS: Update the screen with the draw_menu variables and text, etc. 

def main():
    global music_playing  

    selected_option = 0
    clock = pygame.time.Clock()
    
    pygame.mixer.init()
    
    pygame.mixer.music.load('backgroundmusictest.mp3')  
    pygame.mixer.music.play(-1, 0.0)  
    lap = 0
    while True: 
        for event in pygame.event.get(): 
    
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_w: 
                    selected_option = (selected_option - 1) % len(menu_options) 

                if event.key == pygame.K_s: 
                    selected_option = (selected_option + 1) % len(menu_options)

                if event.key == pygame.K_RETURN: 
                    if selected_option == 0: 
                        start_count_down() 

                     
                        def is_on_track(n): 
                            x, y = n.position
                            x = int(x)
                            y = int(y)
                        
                            width = track_pixels.shape[0] 
                            height = track_pixels.shape[1]
                            pixel_colour = track_pixels[x, y]
                            if 0 <= x < width and 0 <= y < height and tuple(pixel_colour) == track_colour:
                            
                                return True 
                            else:
                                return False 
                      
                        def render_objects(lap, moved, start_time): 
                            screen.blit(track_image, (0, 0)) 
                           
                            Car.update_image(n, math, pygame)
                            a = display_timer(n, lap, moved, start_time)
                            lap = a
                            pygame.display.update() 
                            return lap
                            

                        def run_game(lap, carobject): 
                            global car_x, car_y  
                            game_running = True 
                            moved = False
                            global start_time
                            start_time = time.time()

                            while game_running: 
                                for event in pygame.event.get(): 
                                    if event.type == pygame.QUIT: 
                                        game_running = False
                                    if event.type == pygame.KEYDOWN:
                                        if event.key == pygame.K_ESCAPE: 
                                            pause_menu() 
                                            
                                keys = pygame.key.get_pressed()
                                if keys[pygame.K_w]:
                                    Car.goforwardvelocity(n)
                                  
                                if keys[pygame.K_s]:
                                    Car.gobackwardvelocity(n)
                                    
                                if keys[pygame.K_a]:
                                    Car.update_rotation_left(n)
                                   
                                if keys[pygame.K_d]:
                                    Car.update_rotation_right(n)
                                 
                                x, y = carobject.position
                                if int(x) < 1000 or int(x) > 1150 and int(y) != 350:
                                    moved = True
                                
                                if not is_on_track(n):
                                    crash_sound.play()
                                    pygame.mixer.music.stop() 
                                    game_running = False 
                                    gameover_menu()
                                
                                lap, moved, start_time = render_objects(lap, moved, start_time) 
                                
                                pygame.display.flip() 
                                
                            pygame.quit() 
                            sys.exit() 
                            return lap
                        
                        run_game(lap, n)

                    elif selected_option == 1: 
                        if music_playing: 
                            pygame.mixer.music.stop() 
                            music_playing = False 
                        else: 
                            pygame.mixer.music.play(-1, 0.0)  
                            music_playing = True 

                    elif selected_option == 2:  
                        pygame.quit() 
                        sys.exit() 

        draw_menu(selected_option) 
        clock.tick(60)

if __name__ == "__main__":
    main()
