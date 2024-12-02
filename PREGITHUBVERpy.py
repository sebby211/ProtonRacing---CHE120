import pygame 
import sys 
import time 
import math 
#hi 
pygame.init()  

screen = pygame.display.set_mode((1280, 720))

BLACK = (0, 0, 0) 
WHITE = (255, 255, 255)  
GREEN = (0, 255, 0)
RED = (255, 0, 0)

font = pygame.font.Font('supfont.ttf', 90)  
small_font = pygame.font.Font('supfont.ttf', 50) 

menu_options = ["Start Game", "Audio", "Quit"] 
pause_screen_options = ["Resume", "Quit"] 
music_playing = True  

speaker_on_image = pygame.image.load('speaker_on.png') 
speaker_off_image = pygame.image.load('speaker_off.png') 
speaker_on_image = pygame.transform.scale(speaker_on_image, (50,50)) 
speaker_off_image = pygame.transform.scale(speaker_off_image, (50,50))
speaker_icon_x = 800  
speaker_icon_y = 205  

track_image = pygame.image.load('tracknew.png') 
car_image = pygame.image.load('carnew.png') 
track_image = pygame.transform.scale(track_image, (1280, 720)) 
track_pixels = pygame.surfarray.array3d(track_image) 
track_colour = (84, 84, 84) 
screen = pygame.display.set_mode((track_image.get_width(), track_image.get_height())) 
car_x, car_y = 968, 225  

crash_sound = pygame.mixer.Sound('gameoversoundeffect.mp3') 
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
    count_down_messages = ["3", "2", "1", "Go!"]
    for number in count_down_messages:
        screen.blit(track_image, (0, 0))  
        text = font.render(number, True, WHITE)  
        screen.blit(text, (600,325)) 
        pygame.display.update()  
        time.sleep(1)  
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
        
pause_menu_option_y_positions = [360, 420] # SC: Provided a list with two different y positions for the pause menu options, and will be accessed throughout the pause menu function. 

def pause_menu():
    selected_option = 0  # SC: Initalizes the selected option on 0 (in this case it would be Resume)
    paused = True # SC: If true, runs the while loop below
    while paused:
        for event in pygame.event.get(): # SC: Acts as a for loop within the while paused loop, in short --> checks for inputs from the player
            if event.type == pygame.KEYDOWN: # SC: Only computes for keyboard inputs
                if event.key == pygame.K_w: # SC: If the player presses the 'w' key...
                    selected_option = (selected_option - 1) % 3 # SC: If the w key is pressed, the selected option will move up (purpose of outputing the remainder value between 3 (the len of options) allows players to go from the top selection to the bottom using 'w' for example).
                elif event.key == pygame.K_s:  # SC: If the player presses on the 's' key...
                    selected_option = (selected_option + 1) % 3 # SC: If the s key is pressed, the selected option will move down. 
                elif event.key == pygame.K_RETURN: # SC: If the player presses on the 'return' or 'enter' key...
                    if selected_option == 0:  # SC: If the player hits the "Resume" value, paused value is set to False, removing the surfaced pause menu screen and returning back to the game.
                        paused = False
                    elif selected_option == 1: # SC: If the player hits the "Quit" value, the program shuts down, exiting out of the game. 
                        pygame.quit()
                        sys.exit()

        pause_menu_image = pygame.image.load('pausemenuimage.png') # SC: This loads the pause menu background image, initially provided as a png file. 
        pause_menu_image = pygame.transform.scale(pause_menu_image, (1280, 720)) # SC: This transforms the loaded surface object (the background image) and transforms it into specified dimensions. 
        screen.blit(pause_menu_image, (0,0))  # SC: Displays the background image into the screen
        title = font.render("Paused", True, WHITE) # SC: Defines a variable to the string value and makes it white.
        screen.blit(title, (455, 240))  # SC: Positions and displays the title onto the paused screen. 
        
        i = 0 # SC: Initalizes the variable i as 0 outside of the loop below.
        for option in pause_screen_options: # SC: A for loop that goes through the pause_screen_options list
            if i == selected_option: # SC: If the player is on a selected option, the option will be displayed as a defined colour. 
                if i == 0: # SC: If the player is on "Resume" the text will appear green.
                    colour = GREEN
                elif i == 1: # SC: If the player is on "Quit" the text will appear red. 
                    colour = RED
            else: # SC: Every other option that is not being selected at that point in time will be displayed as white. 
                colour = WHITE 
            text = small_font.render(option, True, colour) # SC: Defines the text to be a specific font and colour.
            screen.blit(text, (540, pause_menu_option_y_positions[i])) # SC: Displays the changes to the text using specified positions.
            
            i += 1  # SC: Iterioate current value of iterates.
            
        pygame.display.update() # SC: Updates the display every iteration.
        
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
    background_image = pygame.image.load('test10car.png') # SC: Sets the background image of the main menu through the loading of a png file (by creating the png into a usable surface object).
    background_image = pygame.transform.scale(background_image, (1280,720)) #SC: Tranforms the background image to specified dimensions.
    screen.blit(background_image, (0, 0))  #SC: Displays the background image.
    title = font.render("Proton Racing", True, WHITE) # SC: Renders the title of the game in a white colour and specific font (*not mentioned in other render functions --> True boolian argument allows for antialias; smoothes the edges of images and reduces distortion).
    screen.blit(title, (250, 50)) #SC: Displays the title at specified positioning.
    i = 0 # SC: Initalizes the variable i as 0 outside of the loop below.
    for option in menu_options: # SC: A for loop that goes through the menu_options list.
        if i == selected_option: # SC: If the player is on a selected option, the option will be displayed as a defined colour. 
            if i == 2: # SC: If the player is on the option "Quit" then the text will turn red.
                colour = RED
            else: # SC: If the player is on any other option the text will turn green.
                colour = GREEN 
        else: # SC: Any other options (that the player is not on), will appear white. 
            colour = WHITE
        if option == "Audio": # SC: In the for loop, if the user selects "Audio" in the list of menu options, then ...
            if music_playing: # SC: Check if music_playing boolean is true (aka if True)
                option = "Audio: On"  # SC: If option in the for loop is 1, for example, it will make it equal to "Audio: On" 
            else:
                option = "Audio: Off"   # SC: If option in the for loop is 2, for example, it will make it equal to "Audio: Off"  
                
        text = small_font.render(option, True, colour) # SC: Set a variable text by using PyGame render function (previously talked about)
        screen.blit(text, (460, menu_option_y_positions[i]))  # SC: Make the text appear on screen by blitting, and the i iteration makes each option i (Play, Audio, Quit) appear on screen with a given position (defined the list above)
        
        i += 1 # SC: Mentioned above

    if music_playing: # SC: Set as a boolean, (aka if True)
        screen.blit(speaker_on_image, (speaker_icon_x, speaker_icon_y)) # SC: Blit image on screen, make a speaker_on png to appear with a respective position
    else: # SC: aka if False
        screen.blit(speaker_off_image, (speaker_icon_x, speaker_icon_y)) # SC: Blit image on screen, make a speaker_off png to appear with a respective position
    pygame.display.update() # SC: Update the screen with the draw_menu variables and text, etc. 

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
