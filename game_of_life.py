# import the pygame module
import pygame
from pygame import surfarray
import numpy as np
from numpy import int32, uint8, uint
import random

cell_size = 10
display_size = 1000 
# Define the background colour
# using RGB color coding.
background_colour = (255, 255, 255)

def all_white():
    return 255 * np.ones((display_size, display_size, 3), int32)

def color_cell(pixel_array, i, j):
    pixel_array[i*cell_size:(i+1)*cell_size, j*cell_size:(j+1)*cell_size] = np.array([0, 0, 0])

# cells -> pixels
def cells2pixs(board):
    pixel_array = all_white()
    dims = board.shape
    for i in range(dims[0]):
        for j in range(dims[1]):
            if board[i][j]:
                color_cell(pixel_array, i, j)
    return pixel_array

allWhite = all_white()

# Define the dimensions of
# screen object(width,height)
screen = pygame.display.set_mode((display_size, display_size))

# Set the caption of the screen
pygame.display.set_caption('Life')
  
# Fill the background colour to the screen
surfarray.blit_array(screen, allWhite)

# Update the display using flip
pygame.display.flip()


def is_valid(coord):
    x, y = coord
    return x >= 0 and x < display_size/cell_size and y >= 0 and y <  display_size/cell_size
   
# if the cell is alive, then it stays alive if it has either 2 or 3 live neighbors
# if the cell is dead, then it springs to life only in the case it has 3 live neighbors
board = np.zeros((int(display_size/cell_size), int(display_size/cell_size)), bool) 

def random_board(board):
    dims = board.shape
    for i in range(dims[0]):
        for j in range(dims[1]):
            board[i][j] = random.random() > .5

random_board(board)
surfarray.blit_array(screen, cells2pixs(board))
pygame.display.flip()

offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 1), (1, 0), (1, -1)]

def step(board):
    """board is an array of booleans, returns array of booleans"""
    dims = board.shape
    new_board = np.zeros(dims, bool)
    for i in range(dims[0]):
        for j in range(dims[1]):
            counter = 0
            neighbor_count = sum([1 if  is_valid((i + offset[0], j + offset[1])) and board[i + offset[0]][j + offset[1]] else 0 for offset in offsets])
            if board[i][j]:
                # cell alive
                new_board[i][j] = neighbor_count == 2 or neighbor_count == 3
            else:
                # cell dead
                new_board[i][j] = neighbor_count == 3
    return new_board

# Variable to keep our game loop running
running = True
# game loop
while running:
    board = step(board)
    surfarray.blit_array(screen, cells2pixs(board))
    pygame.display.flip()
    # for loop through the event queue  
    for event in pygame.event.get():
      
        # Check for QUIT event      
        if event.type == pygame.QUIT:
            running = False
