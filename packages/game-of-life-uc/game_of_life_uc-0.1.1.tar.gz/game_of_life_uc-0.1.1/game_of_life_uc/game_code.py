#!/opt/homebrew/bin/python3

#Conway's game of life

import curses
from curses import wrapper
import random
import time
import copy

#Cell class
class Cell:
    def __init__(self, alive: bool = False):
        self.alive = alive

    #Toggle cell state
    def toggle(self):
        self.alive = not self.alive

    #Set cell state depending on number of neighbors
    def set_state(self, neighbors: int):
        if self.alive:
            if neighbors < 2 or neighbors > 3:
                self.alive = False
        else:
            if neighbors == 3:
                self.alive = True

#Grid class
class Grid:
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        self.cells = [[Cell() for i in range(width)] for j in range(height)]
        self.generation = 0

    #Toggle cell state
    def toggle(self, y: int, x: int):
        self.cells[y][x].toggle()

    #Get number of neighbors
    def get_neighbors(self, y: int, x: int):
        neighbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0: continue
                if y + i < 0 or y + i >= self.height: continue
                if x + j < 0 or x + j >= self.width: continue
                if self.cells[y + i][x + j].alive: neighbors += 1
        return neighbors
    
    #Get number of neighbors wrapping around the edges
    def get_neighbors_wrapped(self, y: int, x: int):
        neighbors = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0: continue
                if self.cells[(y + i) % self.height][(x + j) % self.width].alive: neighbors += 1
        return neighbors

    #Run one iteration of the game
    def run(self):
        stateCopy = copy.deepcopy(self)
        for y in range(self.height):
            for x in range(self.width):
                neighbors = stateCopy.get_neighbors(y, x)
                self.cells[y][x].set_state(neighbors)

        self.generation += 1

    #Run iteration of the game wrapping around the edges
    def run_wrapped(self):
        stateCopy = copy.deepcopy(self)
        for y in range(self.height):
            for x in range(self.width):
                neighbors = stateCopy.get_neighbors_wrapped(y, x)
                self.cells[y][x].set_state(neighbors)

        self.generation += 1 

    #Assign random state to cells
    def randomize(self):
        self.generation = 0

        for y in range(self.height):
            for x in range(self.width):
                self.cells[y][x].alive = random.choice([True, False])

    #Count alive cells
    def count_alive(self):
        alive = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.cells[y][x].alive: alive += 1
        return alive
    
#Function to handle adding colour to the program
def colour_item(stdscr, y, x, text, colour):
    stdscr.addstr(y, x, text, colour)

#When editing the cells, the grid is not updated until the user presses enter
def edit(stdscr, grid: Grid, use_colour: bool):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    DEAD = curses.color_pair(1)
    ALIVE = curses.color_pair(2)
    TEXT = curses.color_pair(3)
    YELLOW = curses.color_pair(4)

    #Get screen size
    height, width = stdscr.getmaxyx()

    #Show the cursor
    curses.curs_set(1)

    #Move cursor to top left corner
    cursor_y = 1
    cursor_x = 1
    stdscr.move(cursor_y, cursor_x)

    while True:
        #If q is pressed, exit edit mode, if r is pressed randomize grid, if space is pressed toggle cell state
        #If arrow keys are pressed move cursor, if c is pressed clear grid
        try:
            key_pressed = stdscr.getch()
        except:
            key_pressed = None

        if key_pressed == 113:
            break
        elif key_pressed == 114:
            grid.randomize()
        elif key_pressed == 99:
            grid = Grid(grid.height, grid.width)

        #Add window border
        stdscr.border()

        if use_colour:
            text_colour = YELLOW + curses.A_BOLD
        else:
            text_colour = TEXT

        # #Move cursor
        # if key_pressed == curses.KEY_UP:
        #     if cursor_y > 1:
        #         cursor_y -= 1
        #         stdscr.addstr(height-1, width-7,"^", text_colour)
        # elif key_pressed == curses.KEY_DOWN:
        #     if cursor_y < grid.height:
        #         cursor_y += 1
        #         stdscr.addstr(height-1, width-7,"_", text_colour)
        # elif key_pressed == curses.KEY_LEFT:
        #     if cursor_x > 1:
        #         cursor_x -= 1
        #         stdscr.addstr(height-1, width-7,"<", text_colour)
        # elif key_pressed == curses.KEY_RIGHT:
        #     if cursor_x < grid.width:
        #         cursor_x += 1
        #         stdscr.addstr(height-1, width-7,">", text_colour)
        # #Toggle cell state when space is pressed
        # elif key_pressed == 32:
        #     grid.toggle(cursor_y-1, cursor_x-1)
        #     stdscr.addstr(height-1, width-7," ", ALIVE)

        stdscr.addstr(0,1,"q: game r: randomize c: clear", text_colour)
        stdscr.addstr(0, width//2 + width//4, "Gen: " + str(grid.generation), text_colour)
        stdscr.addstr(0, width//2 + 1, "Alive: " + str(grid.count_alive()), text_colour)
        stdscr.addstr(height-1, 1, "by Pedro Juan Royo - @parzival1918", text_colour)
        stdscr.addstr(height-1, width - 5, "EDIT", text_colour)

        #Print grid
        for y in range(grid.height):
            for x in range(grid.width):
                if grid.cells[y][x].alive:
                    pass
                    stdscr.addstr(1+y, 1+x, " ", ALIVE)
                else:
                    pass
                    stdscr.addstr(1+y, 1+x, " ", DEAD)

        #Move cursor back to its position
        stdscr.move(cursor_y, cursor_x)

        stdscr.refresh()
        #time.sleep(0.1)

    #Hide the cursor
    curses.curs_set(0)
    #Exit edit mode

    return grid

#Main function
def main(stdscr, wrap: bool, speed: float, use_colour: bool):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    DEAD = curses.color_pair(1)
    ALIVE = curses.color_pair(2)
    TEXT = curses.color_pair(3)
    YELLOW = curses.color_pair(4)

    #Do not wait for keypress
    stdscr.nodelay(True)
    #Disable cursor
    curses.curs_set(0)

    #Get screen size
    height, width = stdscr.getmaxyx()

    #Create grid
    grid = Grid(height-2, width-2) #Leave space for border

    #Check if display is too small
    if height < 3 or width < 60:
        stdscr.clear()
        stdscr.border()
        stdscr.addstr(1, 1, "Please resize the window to at least 60x3", TEXT)
        stdscr.refresh()
        while True:
            try:
                key_pressed = stdscr.getch()
            except:
                key_pressed = None
            if key_pressed == 113:
                return

    #Randomize grid
    grid.randomize()

    #Run game
    while True:
        stdscr.clear()

        #Add window border
        stdscr.border()

        #Print text
        if use_colour:
            text_colour = YELLOW|curses.A_BOLD
        else:
            text_colour = TEXT

        stdscr.addstr(0, 1, "q: quit r: randomize", text_colour)
        stdscr.addstr(0, width//2 + width//4, "Gen: " + str(grid.generation), text_colour)
        stdscr.addstr(0, width//2 + 1, "Alive: " + str(grid.count_alive()), text_colour)
        stdscr.addstr(height-1, 1, "by Pedro Juan Royo - @parzival1918", text_colour)

        try:
            key_pressed = stdscr.getch()
        except:
            key_pressed = None
        
        #Exit if q is pressed, if r is pressed randomize grid, if e is pressed edit grid
        if key_pressed == 113:
            break
        elif key_pressed == 114:
            grid.randomize()
        elif key_pressed == 101:
            grid = edit(stdscr, grid, use_colour)

        #Print grid
        for y in range(grid.height):
            for x in range(grid.width):
                if grid.cells[y][x].alive:
                    stdscr.addstr(1+y, 1+x, " ", ALIVE)
                    # stdscr.addstr(1+y, 1+x, f"{grid.get_neighbors(y, x)}", TEXT)
                else:
                    stdscr.addstr(1+y, 1+x, " ", DEAD)
                    # stdscr.addstr(1+y, 1+x, f"{grid.get_neighbors(y, x)}", TEXT)

        stdscr.refresh()

        #Run one iteration
        if wrap:
            grid.run_wrapped()
        else:
            stdscr.addstr(0, 0, "NORMAL STEP", TEXT)
            grid.run()

        #Wait for keypress
        time.sleep(speed)

    #Exit

if __name__ == "__main__":
    wrapper(main, False, 0.1, False)

def call_game_of_life(args):
    wrap = args.wrap
    speed = args.speed
    use_colour = args.colour

    wrapper(main, wrap, speed, use_colour)