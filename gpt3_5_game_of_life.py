import pygame
from pygame import surfarray
import numpy as np
import random

cell_size = 1
display_size = 1000
dims = int(display_size / cell_size)

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((display_size, display_size))
pygame.display.set_caption('Life')

def all_white():
    return 255 * np.ones((dims, dims, 3), np.uint8)

def random_board():
    return np.random.rand(dims, dims) > 0.5

def get_neighbors(i, j):
    offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, 1), (1, 0), (1, -1)]
    neighbors = [(i + x, j + y) for x, y in offsets]
    valid_neighbors = [(x, y) for x, y in neighbors if 0 <= x < dims and 0 <= y < dims]
    return valid_neighbors

def step(board):
    neighbor_counts = np.zeros((dims, dims), int)
    for i in range(dims):
        for j in range(dims):
            for x, y in get_neighbors(i, j):
                neighbor_counts[i, j] += board[x, y]

    new_board = np.logical_or(np.logical_and(board, neighbor_counts == 2), neighbor_counts == 3)
    return new_board

board = random_board()

# Create the initial pixel array
pixel_array = surfarray.make_surface(all_white())

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    board = step(board)

    # Update the pixel array
    pixel_array = surfarray.make_surface(np.repeat(np.repeat(board, cell_size, axis=0), cell_size, axis=1) * 255)

    # Blit the pixel array to the screen
    screen.blit(pixel_array, (0, 0))
    pygame.display.flip()

# Quit pygame
pygame.quit()

