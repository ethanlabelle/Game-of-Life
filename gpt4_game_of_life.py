import pygame
from pygame import surfarray
import numpy as np
import random

cell_size = 1
display_size = 1000

def cells2pixs(board):
    # Use NumPy operations to convert cells to pixels
    return np.where(board[:, :, None], np.array([0, 0, 0]), np.array([255, 255, 255])).astype(np.int32)

def random_board(dims):
    return np.random.rand(dims[0], dims[1]) < 0.3

def step(board):
    # Pad the board to handle edge cases
    padded_board = np.pad(board, ((1, 1), (1, 1)), mode='constant', constant_values=0)
    # Count neighbors using convolution
    neighbors = sum(np.roll(np.roll(padded_board, i, axis=0), j, axis=1)
                    for i in (-1, 0, 1) for j in (-1, 0, 1)
                    if (i != 0 or j != 0))

    # Trim the padded neighbors array to match board size
    neighbors_trimmed = neighbors[1:-1, 1:-1]

    # Apply Game of Life rules
    return (neighbors_trimmed == 3) | (board & (neighbors_trimmed == 2))


# Initialize Pygame and screen
pygame.init()
screen = pygame.display.set_mode((display_size, display_size))
pygame.display.set_caption('Life')

# Create and display the initial board
board = random_board((int(display_size / cell_size), int(display_size / cell_size)))
surfarray.blit_array(screen, cells2pixs(board))
pygame.display.flip()

running = True
while running:
    board = step(board)
    surfarray.blit_array(screen, cells2pixs(board))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()

