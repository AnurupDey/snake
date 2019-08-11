# SNAKE GAME 

# Use ARROW KEYS to play, SPACE BAR for pausing/resuming and Esc Key for exiting

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

curses.initscr()
win = curses.newwin(20, 60, 0, 0)
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

key = KEY_RIGHT                                                    # Initializing values
score = 0

snake = [[4,10], [4,9], [4,8]]                                     # Initial snake co-ordinates
food = [10,20]                                                     # First food co-ordinates

win.addch(food[0], food[1], '*')                                   # Prints the food

while key != 27:                                                   # While Esc key is not pressed
    win.border(0)
    win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # Printing 'Score' and
    win.addstr(0, 27, ' SNAKE ')                                   # 'SNAKE' strings
    win.timeout(150 - (len(snake)//5 + len(snake)//10)%120)          # Increases the speed of Snake as its length increases
    
    prevKey = key                                                  # Previous key pressed
    event = win.getch()
    key = key if event == -1 else event 


    if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
        key = -1                                                   # one (Pause/Resume)
        while key != ord(' '):
            key = win.getch()
        key = prevKey
        continue

    if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If an invalid key is pressed
        key = prevKey

    # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
    # This is taken care of later at [1].
    snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

    # If snake crosses the boundaries, make it enter from the other side
    if snake[0][0] == 0: snake[0][0] = 18
    if snake[0][1] == 0: snake[0][1] = 58
    if snake[0][0] == 19: snake[0][0] = 1
    if snake[0][1] == 59: snake[0][1] = 1

    # Exit if snake crosses the boundaries (Uncomment to enable)
    #if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: break

    # If snake runs over itself
    if snake[0] in snake[1:]: break

    
    if snake[0] == food:                                            # When snake eats the food
        food = []
        score += 1
        while food == []:
            food = [randint(1, 18), randint(1, 58)]                 # Calculating next food's coordinates
            if food in snake: food = []
        win.addch(food[0], food[1], '*')
    else:    
        last = snake.pop()                                          # [1] If it does not eat the food, length decreases
        win.addch(last[0], last[1], ' ')
    win.addch(snake[0][0], snake[0][1], '#')
    
curses.endwin()
print("\nScore - " + str(score))

########################################################################################################################
#               ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ OLD CODE ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ 
########################################################################################################################

class Snake:
    
    def __init__ (self, initial_coords):
        self.path = initial_coords 
    
    def current_coordinate (self):
        return self.path[0]

    def length ():
        return len (self.path)

    def follow_path (self):
        self.path.insert (0, current_coordinate())

    def move_left (self):
        new_coord = self.current_coordinate()
        new_coord[0] -= 1
        self.path.insert (0, new_coord)

    def move_right (self):
        new_coord = self.current_coordinate()
        new_coord[0] += 1
        self.path.insert (0, new_coord)

    def move_down (self):
        new_coord = self.current_coordinate()
        new_coord[1] += 1
        self.path.insert (0, new_coord)

    def move_up (self):
        new_coord = self.current_coordinate()
        new_coord[1] -= 1
        self.path.insert (0, new_coord)
    
    def adjust_to_boundary (self, height, width, margin):
        coord = self.current_coordinate ()
        coord[0] = width  - margin if coord[0] == 0 else margin
        coord[1] = height - margin if coord[1] == 0 else margin                                                                           
    
class SnakeGame:

    KEY_ESCAPE = 27
    KEY_SPACE  = ' ' 

    def __init__ (self, height, width, margin):
        # handle to snake
        self.snake = Snake ([[4,10], [4,9], [4,8]])
        
        # curses initialization 
        self.init_curses ()

        self.height, self.width = height, width 
        self.margin = margin 

        self.score = 0
        self.food  = []

         # obtain game window
        self.window = self.get_window (height, width)
        
    def init_curses (self): 
        curses.initscr ()
        curses.noecho ()
        curses.curs_set (0)

    def get_window (self, height, width):
        window = curses.newwin (
            height, width, 0, 0)
        window.keypad (1)
        window.border (0)
        window.nodelay(1)

        return window 
    
    def update_window (self):
        self.window.border (0)
        
        # Printing 'Score'
        self.window.addstr (0, self.margin, 
            'Score : ' + str(self.score) + ' ')             
        
        # 'SNAKE' strings
        self.window.addstr (0, 
            self.width // 2 - 
            self.margin - 1, ' SNAKE ')                                   
        
        # Increases the speed of 
        # Snake as its length increases
        self.window.timeout (150 - 
            (self.snake.length () // 5 + 
             self.snake.length () // 10) % 
             120)          
    

    def place_food (self):
        while self.food == []:
            self.food = [randint(1, height - margin), randint(1, 58)]                 # Calculating next food's coordinates
            if food in snake: food = []
        win.addch(food[0], food[1], '*')

    def handle_keypress (key):
        if key == KEY_LEFT:
            self.snake.move_left ()
        elif key == KEY_RIGHT:
            self.snake.move_right () 
        elif key == KEY_DOWN:
            self.snake.move_down ()
        elif key == KEY_UP:
            self.snake.move_up ()
        elif key == KEY_SPACE:
            pause_game ()
        elif key == KEY_ESCAPE:
            close_game ()
        else:
            self.snake.follow_path ()  

    def pause_game (self):
        # wait until next space
        while self.get_keypress () != KEY_SPACE:
            pass

    def close_game (self):
        curses.endwin ()
        print("\nScore - " + str (score))
    
    def get_keypress (self):
        event = self.window.getch ()
        key = key if event == -1 else event
        return key 

    def run_game (self):
        while True:
            self.update_window ()
            key = self.get_keypress ()
            self.handle_keypress (key)
            
            if key == KEY_ESCAPE:
                break
            
            self.snake.adjust_to_boundary (
                self.height, self.width, self.margin)

                                                                                                                                                                                     
