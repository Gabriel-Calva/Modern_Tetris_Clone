# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
import random

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
each with their own rotations
"""

pygame.font.init()

# GLOBALS VARS

# SCREEN SIZE
s_width = 800
s_height = 700

# PLAY BOX SIZE
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

# COLLISION CHECK
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '0000.',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]


# Dictionary replaced the list of colors due to changes in the randomization of pieces
color_dict = {tuple(tuple(i) for i in S): (0, 255, 0), tuple(tuple(i) for i in Z): (255, 0, 0),
              tuple(tuple(i) for i in I): (0, 255, 255), tuple(tuple(i) for i in O): (255, 255, 0),
              tuple(tuple(i) for i in J): (0, 0, 255), tuple(tuple(i) for i in L): (255, 165, 0),
              tuple(tuple(i) for i in T): (128, 0, 128)}


# Class for the playable pieces
class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color_dict[tuple(tuple(i) for i in shape)] #Coincides with the dictionary above
        self.rotation = 0


# Class for the shadow piece at the bottom of the screen
class Shadow_piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = (50, 50, 50)
        self.rotation = 0


# Creates the grid
def create_grid(locked_pos={}):
    grid = [[(0,0,0)for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j,i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid


# Converts the shape into a list of positions to be placed onto the grid and be compared with other shapes
def convert_shape_format(shape):

    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4) # Offset for the display

    return positions


# Makes it so the pieces don't fly off the grid on the right side at the TOP of the grid
def valid_right(shape, x_coordinate):
    positions = []
    biggest_num = -1
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append(j) #positions is now a list of all the indexes of the x-coordinate of the given shape

    for i in positions:
        if i > biggest_num:
            biggest_num = i

    if x_coordinate + biggest_num < 11:
        return True
    else:
        return False


# Makes it so the pieces don't fly off the grid on the left side at the TOP of the grid
def valid_left(shape, x_coordinate):
    positions = []
    smallest_num = 10
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append(j) #positions is now a list of all the indexes of the x-coordinate of the given shape

    for i in positions:
        if i < smallest_num:
            smallest_num = i

    if x_coordinate + smallest_num > 2:
        return True
    else:
        return False


# Checks to see if our piece is on the grid and is in a valid position where there is no block/color
def valid_space(shape, grid):
    accepted_pos = [[(j,i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub] #Flattens the list out from a 2D list to a 1D list to more easily loop through

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


# Checks the top of the grid to see if we have lost the game
def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False


# Used to make the main menu. WIP
def draw_text_middle(text, size, color, surface):
    pass


# Draws out the lines on the grid
def draw_grid(surface, grid):

    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx + play_width, sy + i*block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy),(sx + j*block_size, sy + play_height))


# Function that both sees if a row is fully colored, as well as clears the row and drops all of the pieces down

# ORIGANL Clear rows function that was buggy. Kept it in the code for comparison's sake
def clear_row1(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    if inc > 0:
        for key in sorted(list(locked), key = lambda x:x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

# NEW Clear rows function that allows for rows to be cleared regardless of where the rows actually are within the grid
# There's most definitely a better/cleaner way to structure the code. Cleaning of this function is a WIP, but works atm
def clear_rows(grid, locked):

    inc = 0
    ind = []
    # For loop that looks through the grid from the bottom, and deletes any row that is complete
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind.append(i)
            print(ind)
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue
    if inc > 0:
        # For loop that goes through each deleted row's index
        for k in ind:
            print(k)
            # For loop that shifts every row above a deleted row down by 1
            for key in sorted(list(locked), key = lambda x:x[1])[::-1]:
                x, y = key
                if y < k:
                    newKey = (x, y + 1)
                    locked[newKey] = locked.pop(key)
            print(k)
            # For loop that shifts the indexes of the deleted rows down. Each deleted row is taken care of, 1 by 1
            # This means that if there is more than 1 row being deleted, the deleted rows are also being shifted down
            # To compensate for this, the indexes must also be shifted down, hence the need for this for loop
            for m in range(inc):
                ind[m] += 1
                print(ind)




# Function that draws the pieces that are in queue on the right side of the grid
# Added pos_x and pos_y to accommodate for drawing more pieces in different spots (3 more pieces in the project)
def draw_next_shape(shape, surface, pos_x, pos_y):
    font = pygame.font.SysFont('TimesNewRoman', 30)
    label = font.render('Next Shapes', 1, (255,255,255))

    sx = top_left_x + play_width + 45
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size + pos_x, sy + i*block_size + pos_y, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 175))


# Function that draws the holding piece on the left side of the grid
def draw_holding_piece(shape, surface, pos_x, pos_y): #New function to draw holding piece
    font = pygame.font.SysFont('TimesNewRoman', 30)
    label = font.render('Holding', 1, (255, 255, 255))

    sx = top_left_x + play_width + 45
    sy = top_left_y + play_height / 2 - 100

    if shape is not None:
        format = shape.shape[shape.rotation % len(shape.shape)]

        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color, (sx + j * block_size + pos_x, sy + i * block_size + pos_y, block_size, block_size), 0)

    surface.blit(label, (sx - 525, sy - 175))


#Draws the window that the grid lies in
def draw_window(surface, grid):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('TimesNewRoman', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - label.get_width() / 2, 30))

    for i in range(len(grid)):
        for j in range (len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255,0,0), (top_left_x, top_left_y, play_width, play_height),4)

    draw_grid(surface, grid)



def main(win):
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    holding_piece = None
    holding_used = False

    # Initializing first 7 pieces
    import queue
    piece_queue = queue.Queue()
    if piece_queue.empty():
        random.shuffle(shapes)
        for i in range(7):
            piece_queue.put(Piece(5, 0, shapes[i]))
        random.shuffle(shapes)
        for i in range(7):
            piece_queue.put(Piece(5, 0, shapes[i]))

    # SUGGESTION - Maybe put these variables into an array
    current_piece = piece_queue.get()
    next_piece = piece_queue.get()
    next_piece1 = piece_queue.get()
    next_piece2 = piece_queue.get()
    next_piece3 = piece_queue.get()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.75
    shadow_shape = Shadow_piece(5, 0, current_piece.shape)

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()
        shadow_shape.shape = current_piece.shape

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if (valid_space(current_piece, grid)) and (current_piece.x > 0) and valid_left(current_piece, current_piece.x):
                        current_piece.x -= 1
                    shadow_shape.y = current_piece.y
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1

                if event.key == pygame.K_RIGHT:
                    if (valid_space(current_piece, grid)) and (current_piece.x < 9) and valid_right(current_piece, current_piece.x):
                        current_piece.x += 1
                    shadow_shape.y = current_piece.y
                    if not(valid_space(current_piece, grid)):
                        current_piece.x -= 1


                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.y -= 1

                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    shadow_shape.y = current_piece.y
                    shadow_shape.rotation += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                        shadow_shape.rotation -= 1

                if event.key == pygame.K_LCTRL:
                    current_piece.rotation -= 1
                    shadow_shape.y = current_piece.y
                    shadow_shape.rotation -= 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation += 1
                        shadow_shape.rotation += 1

                if event.key == pygame.K_SPACE: #New fast drop addition
                    while valid_space(current_piece, grid):
                        current_piece.y += 1
                    current_piece.y -= 1  #Needed so game doesn't crash and so pieces don't clip into each other
                    change_piece = True

                if event.key == pygame.K_LSHIFT: #New holding addition
                    if holding_used == False:
                        if holding_piece == None:
                            current_piece.rotation = 0
                            shadow_shape.rotation = 0
                            holding_piece = current_piece
                            current_piece = next_piece
                            next_piece = next_piece1
                            next_piece1 = next_piece2
                            next_piece2 = next_piece3
                            next_piece3 = piece_queue.get()
                            current_piece.x = 5
                            current_piece.y = 0
                            shadow_shape.y = current_piece.y
                        else:
                            current_piece.rotation = 0
                            shadow_shape.rotation = 0
                            holding_piece, current_piece = current_piece, holding_piece
                            current_piece.x = 5
                            current_piece.y = 0
                            shadow_shape.y = current_piece.y
                        holding_used = True

        shape_pos = convert_shape_format(current_piece)

        shadow_shape.x = current_piece.x

        while valid_space(shadow_shape, grid):
            shadow_shape.y += 1
        shadow_shape.y -= 1

        shadow_pos = convert_shape_format(shadow_shape)

        for i in range(len(shadow_pos)):
            shadow_x, shadow_y = shadow_pos[i]
            if shadow_y > -1:
                grid[shadow_y][shadow_x] = shadow_shape.color

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        #New Randomization of pieces is here
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            if piece_queue.qsize() <= 7:
                random.shuffle(shapes)
                for i in range(7):
                    piece_queue.put(Piece(5,0, shapes[i]))
            current_piece = next_piece
            next_piece = next_piece1
            next_piece1 = next_piece2
            next_piece2 = next_piece3
            next_piece3 = piece_queue.get()
            shadow_shape.rotation = 0
            shadow_shape.y = current_piece.y

            holding_used = False
            change_piece = False
            clear_rows(grid, locked_positions)

        draw_window(win, grid)
        draw_holding_piece(holding_piece, win, -525, -125)
        draw_next_shape(next_piece, win, 10, -125)
        draw_next_shape(next_piece1, win, 10, 0)
        draw_next_shape(next_piece2, win, 10, 125)
        draw_next_shape(next_piece3, win, 10, 250)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False

    pygame.display.quit()



def main_menu(win):
    main(win)

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game

# See PyCharm help at https://www.jetbrains.com/help/pycharm/