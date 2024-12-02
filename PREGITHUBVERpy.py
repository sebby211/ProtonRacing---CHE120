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

class Car: #JV: Initializes a car class which can be used to create car objects 
    def __init__(self, pygame): #JV: Initialization of the parts of the class
        self.sizey = 20 #JV: A size in the vertical direction
        self.sizex = 50 #JV: A size in the horizontal direction
        self.position = pygame.Vector2(1075, 350) #JV: Establish a vector position
        self.shape = pygame.image.load('carnew.png') #JV: Loads the attached image from the zip file
        self.image = self.shape #JV: Creates a image that can be transformed without changing the original image
        self.velocity = 0 #JV: Velocity of car at different times, starts at 0 because car doesn't move
        self.acceleration = 0.006 #JV: The rate that the velocity goes up per tick of the code, many ticks per second so value is very small
        self.rotation = 0 #JV: Current angle relative to horizontal of the car
        self.cornering = 0.4 #JV: Amount the cars rotation can change per tick, in degrees.
        self.topspeed = 2 #JV: Maximum speed the car can hit

    #JV: Note: Code did not behave as expected initially because when I wrote it in my environment, point (0,0) was bottom left
    #JV: Cont: For the code written by other members it was the top left
    #JV: Cont: This resulted in weird results where in order to increase velocity we need to actually decrease it etc.
    #JV: Cont: Basically, I just inverted all of the statements until it worked
    def update_position(self, math): #JV: Function for updating position of the car based on the velocity and rotation. Uses trig. to determine cars position
        self.position = pygame.Vector2(self.position.x + (math.sin(math.radians(self.rotation)))*self.velocity, self.position.y + (math.cos(math.radians(self.rotation))*self.velocity))
    def update_rotation_left(self): #JV: Player choose to go left, so angle responds accordingly
        self.rotation += self.cornering
    def update_rotation_right(self): #JV: Player choose to go right, so angle responds accordingly
        self.rotation -= self.cornering
    def goforwardvelocity(self): #JV: Player goes forward which changes the velocity as long as its less than the top speed
        if self.velocity >= self.topspeed*(-1):
            self.velocity -= self.acceleration
    def gobackwardvelocity(self): #JV: Player goes backward, velocity is changed as long as not going backward faster than top speed
        if self.velocity <= self.topspeed:
            self.velocity += self.acceleration
    def update_image(self, math, pygame): #JV: Blits to the screen a copy of the the current positon (image) of the car.
        self.update_position(math)
        image = pygame.transform.rotate(self.image, self.rotation)
        screen.blit(image, self.position)
                    
n = Car(pygame) #JV: Initializes a car object for the player

def start_count_down():
    count_down_messages = ["3", "2", "1", "Go!"]
    for number in count_down_messages:
        screen.blit(track_image, (0, 0))  
        text = font.render(number, True, WHITE)  
        screen.blit(text, (600,325)) 
        pygame.display.update()  
        time.sleep(1)  
global times_list
times_list = [0]  #JV: Initially there are no times, but needs some text to print or there will be an error, hence: 0

def display_timer(carobject, lap, moved, start_time): #JV: Defines a function with required parameters
    if start_time is not None: #JV: Insuring the game has started
        elapsed_time = time.time() - start_time #JV: Time of start minus the current time represents the elapsed time
        minutes = int(elapsed_time) // 60 #JV: If time is > 60, will need to be split into minutes and seconds
        seconds = int(elapsed_time) % 60
        timer_text = f"{minutes:02}:{seconds:02}" 
        text = small_font.render(timer_text, True, WHITE) #JV: Renders the text with font on the screen for the timer
        screen.blit(text, (20, 20)) #JV: Blits it to the screen
        x,y = carobject.position #JV: Takes the x,y position of the car currently 
        if int(x) > 1000 and int(x) < 1150 and int(y) == 350 and moved: #JV: If car is currently at the start line and has moved since the last it was there
            if times_list[0] == 0: #JV: Times list was initialized with a 0, if it still contains it, remove it and put the new time at its index
                times_list[0] = elapsed_time #JV: If 0 stays, it will always be the quickest lap, must be removed
            times_list.append(elapsed_time) #JV: if not 0, just append it to the list
            start_time = time.time() #JV: Redefine start time as now for future laps
            lap += 1 #JV: Increment laps
            moved = False #JV: The car has not moved since the last time it was at the start, so False. When it moves again it will be set to true
        lap_text = small_font.render('LAP: ' + str(lap), True, WHITE) #JV: Display the text of the current lap
        screen.blit(lap_text, (1050, 10)) #JV: Blits it to the screen
        w = min(times_list) #JV: Finds the minimum/best lap time
        w = ("%.2f" % w) #JV: Formats it to 2 decimal places
        w = str(w) #JV: Turns into a str so it can be printed
        w = w.split('.') #JV: Remove the period and split it into a list
        if w[0] == 0: #JV: Only pertinent for 1st lap, just reformates the 0 for the first lap
            w = ['0','00']
        output = 'Best LAP: ' + str(w[0])+':'+ str(w[1]) #JV: Creates a str for output, format is "seconds" + ":" + "milliseconds".
        best_text = small_font.render(output, True, WHITE) #JV: Renders the text 
        screen.blit(best_text, (790, 50)) #JV: Blits it to the screen
        return lap, moved, start_time #JV: Returns information needed for future loops of this function, will be repassed through every time. 
        
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

    if music_playing: 
        screen.blit(speaker_on_image, (speaker_icon_x, speaker_icon_y)) 
    else:
        screen.blit(speaker_off_image, (speaker_icon_x, speaker_icon_y)) 
    pygame.display.update() 

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
                            a = display_timer(n, lap, moved, start_time) #JV: n is the car object, lap is the current lap, moved is whether the car has moved
                            lap = a #JV: Sets lap to return of display_timer to see if lap has changed
                            pygame.display.update() #JV: Prints to screen all rendered/blitted stuff throughout the code
                            return lap #Returns lap for running throughout the loop
                            

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
                                 
                                x, y = carobject.position #JV: Takes the cars position
                                if int(x) < 1000 or int(x) > 1150 and int(y) != 350: #JV: Sees if the car has moved
                                    moved = True #JV: Car has moved, so set moved = True
                                
                                if not is_on_track(n):
                                    crash_sound.play()
                                    pygame.mixer.music.stop() 
                                    game_running = False 
                                    gameover_menu()
                                
                                lap, moved, start_time = render_objects(lap, moved, start_time) #JV: Passes in lap, moved, and start_time, and will return them if they have changed
                                
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
