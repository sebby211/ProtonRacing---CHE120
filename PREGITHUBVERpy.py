
import pygame #AS: Imports all of the available pygame modules into the program
import sys #AS: Imports the sys module
import time #AS: Imports the time module
import math #AS: Imports math module
 
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
    count_down_messages = ["3", "2", "1", "Go!"] #AS: A homogenous string list is defined as to a variable name (this list includes the text that will show on the screen during the countdown)
    for number in count_down_messages: #AS: Consists of a for loop that goes through each item within the list
        screen.blit(track_image, (0, 0)) #AS: This will display the track image through each iteration 
        text = font.render(number, True, WHITE) #AS: Here a variable is set to a specific font (font was established earlier in the program), and the established tuple, WHITE. The eterated values are to be set as arguments within the render function as well.  
        screen.blit(text, (600,325)) #AS: This allows the text variable above to be postioned and surfaced onto the screen, using a specific position tuple as an argment.
        pygame.display.update() #AS: Updates the display every iteration. 
        time.sleep(1) #AS: Pauses the loop for a second between each iteration, allowing the coundown to flow smoothly. 
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
        
pause_menu_option_y_positions = [360, 420] # SC: Provided a list with two different y positions for the pause menu options, and will be accessed throughout the pause menu function. 

def pause_menu():
    selected_option = 0  # SC: Initalizes the selected option on 0 (in this case it would be Resume)
    paused = True # SC: If true, runs the while loop below
    while paused:
        for event in pygame.event.get(): # SC: Acts as a for loop within the while paused loop, in short --> checks for inputs from the player
            if event.type == pygame.KEYDOWN: # SC: Only computes for keyboard inputs
                if event.key == pygame.K_w: # SC: If the player presses the 'w' key...
                    selected_option = selected_option - 1 # SC: If the w key is pressed, the selected option will move up 
                elif event.key == pygame.K_s:  # SC: If the player presses on the 's' key...
                    selected_option = selected_option + 1 # SC: If the s key is pressed, the selected option will move down. 
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
            
            i += 1  # SC: Iterates current value of i.
            

        pygame.display.update() 
         
def gameover_menu(): #N.L - A function that draws and codes functionality of the gameover screen, and has no arguments since it just needs to be called to show up 
    while True: #N.L - A while loop to make these things occur over and over again while the condition is True 
        for event in pygame.event.get(): #N.L - Pygame function that essentially checks all events that have occured, saying that for each "action" or event that happens, do...
            if event.type == pygame.QUIT: #N.L - If the user hits the "X" aka the close button on the window, it detects this and then...
                pygame.quit() #N.L - It will close PyGame, since we iniitalized it in the beginning it needs to be quit
                sys.exit() #N.L - It will close the program and closes everything properly 
            if event.type == pygame.KEYDOWN: #N.L - If a key on the keyboard is pressed (regardless of what it is), then...
                    if event.key == pygame.K_RETURN: #N.L - If the key pressed was "Enter" or "Return", then it will...
                        pygame.quit() #N.L - It will close PyGame, since we iniitalized it in the beginning it needs to be quit
                        sys.exit() #N.L - It will close the program and closes everything properly so when the user hits enter on the "Quit" button (defined below), it will close

        
        background_image = pygame.image.load('demo_car.png') #N.L - Load the image, which in this case is the gameover "car crash" picture using PyGame's image load function
        background_image = pygame.transform.scale(background_image, (1280, 720)) #N.L - Uses PyGame's scaling functionality to make the image fit the screen properly 
        screen.blit(background_image, (0, 0)) #N.L - Make the image appear on the screen at (0,0), which just makes the image that is 1280 x 720 fit it properly

        title = font.render("Game Over", True, RED) #N.L - Makes the title text using PyGame's render function, which just makes "Game Over" appear in red 
        screen.blit(title, (330, 50)) #N.L - Makes the text appear on screen using PyGame's blit function, which its respective positioning coordinates
                     
        text = small_font.render("Quit", True, GREEN) #N.L - Makes the quit button appear in green using PyGame's render function with the previously defined small_font
        screen.blit(text, (550, 200)) #N.L - Makes the text appear on screen using PyGame's blit function, which its respective positioning coordinates
            
        pygame.display.update() #N.L - Call this function to ensure that when this appears, make the display of the game update such as blits (ensures everything is up-to-date in a sense)
        

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
             
        text = small_font.render(option, True, colour) 
        screen.blit(text, (460, menu_option_y_positions[i]))  # SC: Make the text appear on screen by blitting, and the i iteration makes each option i (Play, Audio, Quit) appear on screen with a given position (defined the list above)
        
        i += 1 # SC: Mentioned above

    if music_playing: # SC: Set as a boolean, (aka if True)
        screen.blit(speaker_on_image, (speaker_icon_x, speaker_icon_y)) # SC: Blit image on screen, make a speaker_on png to appear with a respective position
    else: # SC: aka if False
        screen.blit(speaker_off_image, (speaker_icon_x, speaker_icon_y)) # SC: Blit image on screen, make a speaker_off png to appear with a respective position
    pygame.display.update() # SC: Update the screen with the draw_menu variables and text, etc. 


def main(): #
    global music_playing  

    selected_option = 0 
    clock = pygame.time.Clock()
    
    pygame.mixer.init() #N.L - Opens/initializes PyGame's mixer, which is responsible for the music playing and sound effects
    pygame.mixer.music.load('backgroundmusictest.mp3') #N.L - Uses the music.load function in PyGame to load the mp3 file which contains the background music
    pygame.mixer.music.play(-1, 0.0) #N.L - Plays the mp3 file background music, the -1 allows an infinite looping of the file, and makes sure it starts at 0.0 seconds
    lap = 0
    while True: 
        for event in pygame.event.get(): #N.L - Checks for each action/event that occurs using PyGame's event.get function 
    
            if event.type == pygame.QUIT: #N.L - If the event/action that occurs is the "X" at the corner of the window, then...
                pygame.quit() #N.L - Close PyGame
                sys.exit() #N.L - It will close the program and closes everything properly 

            if event.type == pygame.KEYDOWN: #N.L - If the user hits a key on the keyboard, then...
                if event.key == pygame.K_w: #N.L - If the user hits the "w" key, then...
                    selected_option = selected_option - 1 #N.L - Make the selected_option index go down one value, since you are then going up in the positions (aka moving up the menu options)

                if event.key == pygame.K_s: #N.L - If the user hits the "s" key, then...
                    selected_option = selected_option + 1 #N.L - Make the selected_option index go up one value, since you are then going down in the positions (aka moving down the menu options)

                if event.key == pygame.K_RETURN: #N.L - If the user hits "Enter" on the keyboard then...
                    if selected_option == 0: #N.L - If the user hits this while on the Play button (selected_option = 0), then...
                        start_count_down() #N.L - Call the start_count_down function, which has already been defined above 

                     
                        def is_on_track(n): #N.L - Function definition, defines what the track is based on pixel colour
                            x, y = n.position #JV: the position of the car is the x,y tuple 
                            x = int(x) #JV: pygame requires a vector position, but needs to be used as a position, to determine on track, so convert to an integer
                            y = int(y) #JV: same reason as above 
                        
                            width = track_pixels.shape[0] #N.L - As defined in the beginning of the code, track_pixels was defined as an arary, hence by using shape[0], its accessing the columns of the arary (which is the width)
                            height = track_pixels.shape[1] #N.L - As defined in the beginning of the code, track_pixels was defined as an arary, hence by using shape[1], its accessing the rows of the arary (which is the height)
                            pixel_colour = track_pixels[x, y]  #N.L - Establish a pixel_colour variable as a tuple of x,y positions (which is why x and y needed to be coverted to int
                            if 0 <= x < width and 0 <= y < height and tuple(pixel_colour) == track_colour: #N.L - Checks if on track by making sure the car's x and y positions are in the array of pixels and that they match the colour of the track  
                                return True #N.L - If it does satisfy these conditions, then return True obviously
                            else:
                                return False #N.L - Otherwise, return False if the conditions are not met 
                      
                        def render_objects(lap, moved, start_time): #JV: Function which renders all objects that are displayed on the screen
                            screen.blit(track_image, (0, 0)) #JV: Blits the image of the track to the screen
                            Car.update_image(n, math, pygame) #JV: Uses a car method to update the current image of the car on the screen
                            a = display_timer(n, lap, moved, start_time) #JV: n is the car object, lap is the current lap, moved is whether the car has moved
                            lap = a #JV: Sets lap to return of display_timer to see if lap has changed
                            pygame.display.update() #JV: Prints to screen all rendered/blitted stuff throughout the code
                            return lap #JV: Returns lap for running throughout the loop
                            

                        def run_game(lap, carobject): 
                            global car_x, car_y  
                            game_running = True 
                            moved = False
                            global start_time
                            start_time = time.time()

                            while game_running: #JV: Continuously loops through the game loop while the game is running
                                for event in pygame.event.get(): #JV: Loops through all the events that occured
                                    if event.type == pygame.QUIT: #JV: If the tab is closed, stop the code from running, otherwise will run forever
                                        game_running = False
                                    if event.type == pygame.KEYDOWN: 
                                        if event.key == pygame.K_ESCAPE: #JV: If key pressed is escape run the pause_menu() function
                                            pause_menu() 
                                            
                                keys = pygame.key.get_pressed() #JV: Takes in input from pygame as to what keys the user pressed
                                if keys[pygame.K_w]: #JV: Checks if they pressed w for go forward
                                    Car.goforwardvelocity(n) #JV: Runs the corresponding velocity function
                                  
                                if keys[pygame.K_s]: #JV: Checks if they pressed s for go backward
                                    Car.gobackwardvelocity(n)  #JV: Runs the corresponding velocity function
                                    
                                if keys[pygame.K_a]: #JV: Checks if they pressed a for go left
                                    Car.update_rotation_left(n) #JV: Runs the corresponding rotation function
                                   
                                if keys[pygame.K_d]: #JV: Checks if they pressed d for go right
                                    Car.update_rotation_right(n) #JV: Runs the corresponding rotation function
                                 
                                x, y = carobject.position #JV: Takes the cars position
                  
                                if int(x) < 1000 or int(x) > 1150 and int(y) != 350: #JV: Sees if the car has moved
                                    moved = True #JV: Car has moved, so set moved = True
                                
                                if is_on_track(n) == False #N.L - Checks if the conditions for the is_on_track function are satisfied, if they are not (aka off the tracK), then...
                                    crash_sound.play() #N.L - Play the crash sound, which has been loaded previously 
                                    pygame.mixer.music.stop() #N.L - Stop the background music 
                                    game_running = False #N.L - Set the game_running variable to False, which is a way of indirectly breaking the game loop 
                                    gameover_menu() #N.L - Calls the game over menu, which contains the functionality and the menu screen drawing 
                                
                                lap, moved, start_time = render_objects(lap, moved, start_time) #JV: Passes in lap, moved, and start_time, and will return them if they have changed
                                
                                pygame.display.update() #N.L - Updates the current display when the run_game function is called 
                                
                           
                            return lap
                        
                        run_game(lap, n)

                    elif selected_option == 1: #N.L - If the user is hits the second button (Audio button), then...
                        if music_playing: #N.L - Previously, the music_playing variable was iniitalized as True, so if the music is already playing then...
                            pygame.mixer.music.stop() #N.L - Stop the music 
                            music_playing = False #N.L - Since the music isn't playing anymore, set the variable to False
                        else: 
                            pygame.mixer.music.play(-1, 0.0)  #N.L - If it is not playing already, then start the music by infinitely looping it and starting at 0.0 seconds
                            music_playing = True #N.L - Set the music playing variable to be True since music is now playing

                    elif selected_option == 2:  #N.L - If the user selects the third button on the menu screen (Quit), then...
                        pygame.quit() #N.L - Quit Pygame
                        sys.exit() #N.L - Properly close the execution of the code 

        draw_menu(selected_option) #N.L - Calls the draw_menu function with the argument of the respective selected_option, which draws and applies the functionality of the menu screen
        clock.tick(60) #N.L - Sets the frame rate to be 60 frames per second (60 fps), using PyGame's clock.tick function 

if __name__ == "__main__":
    main()
