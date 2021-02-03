import pygame
import numpy as np
import random

pygame.init()
 
# Define the colors we will use
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
GREEN = (100, 255, 0)
GRAY = (73, 73, 73)

screen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()

pygame.display.set_caption("Life")

#size of each box
width = height = 20

# number of boxes
N_WIDTH = screen_width // width
N_HEIGHT = screen_height // height

#how many of the squares start as 1
percentage_start = 50

#how fast to generate the next generation
refresh = 15
 
border = 20

font = pygame.font.Font('freesansbold.ttf', 14)
font_large = pygame.font.Font('freesansbold.ttf', 15)

#Loop until the user clicks the close button.
done = False
 
state = np.zeros((N_HEIGHT, N_WIDTH))
new_state = np.zeros((N_HEIGHT, N_WIDTH))

frame_count = 0

ripple_freq = 25 #every ripple_freq frames, execute a ripple
ripple_delay = 100

def initialize_state(state):
    for x in range(0, N_WIDTH):
        for y in range(0, N_HEIGHT):
            if ((y < 6 or y > N_HEIGHT - 6) or (x < 6 or x > N_WIDTH - 6)) and random.randint(0, 100) < percentage_start:
                state[y][x] = 1

def v(x, y, state):
    if x < 0 or y < 0 or x >= len(state[0]) or y >= len(state):
        return 0
    else:
        return state[y][x]

def number_live_neighbors(x, y, state):
    return v(x-1, y-1, state) + v(x, y-1, state) + v(x+1, y-1, state) + \
    v(x-1, y, state) + v(x+1, y, state) + \
    v(x-1, y+1, state) + v(x, y+1, state) + v(x+1, y+1, state)

def update_state(x, y, state, new_state):
    status = state[y][x]
    num_neighbors = number_live_neighbors(x, y, state)
    if status == 1: # if live
        if num_neighbors < 2 or num_neighbors > 3:
            new_state[y][x] = 0
        else:
            new_state[y][x] = 1
    elif status == 0:
        if num_neighbors == 3:
            new_state[y][x] = 1
        else:
            new_state[y][x] = 0

def ripple(radius, state, new_state):
    #pick a random starting point
    x = random.randint(5, N_WIDTH - 5)
    y = random.randint(5, N_HEIGHT - 5)

    current_radius = 0

    #every delay, grow the ripple in size by 1
    while current_radius <= radius:
        next_generation(state, new_state)

        old = state
        state = new_state
        new_state = old

        set_diamond(x, y, current_radius, state, 1)

        for i in range(0, current_radius - 1):
            set_diamond(x, y, i, state, 0)

        current_radius += 1

        render_state(state)

def set_diamond(x, y, radius, state, value):
    #turn on appropriate cells
    state[y - radius][x] = value #north most one

    for i in range(0, radius):
        if is_valid_indices(x + i, y - radius + i):
            state[y - radius + i][x + i] = value

    for i in range(0, radius):
        if is_valid_indices(x + radius - i, y + i):
            state[y + i][x + radius - i] = value  

    for i in range(0, radius):
        if is_valid_indices(x - i, y + radius - i):
            state[y + radius - i][x - i] = value

    for i in range(0, radius):
        if is_valid_indices(x - radius + i, y - i):
            state[y - i][x - radius + i] = value

def is_valid_indices(x, y):
    return x >= 0 and y >= 0 and x < N_WIDTH and y < N_HEIGHT

initialize_state(state)

def render_state(state):
    screen.fill(BLACK)

    for x in range(0, N_WIDTH):
        for y in range(0, N_HEIGHT):
            color = GREEN if state[y][x] == 1 else GRAY

            text = None

            if state[y][x] == 1:
                text = font_large.render('1', True, color)
            else:
                text = font.render('0', True, color)
            
            textRect = text.get_rect()
            textRect.center = (x * width, y * height)
            screen.blit(text, textRect)
    
    pygame.time.delay(refresh)
    pygame.display.flip()

def next_generation(state, new_state):
    #update states
    for x in range(0, N_WIDTH):
        for y in range(0, N_HEIGHT):
            update_state(x, y, state, new_state)
    
    return new_state

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            done=True

    render_state(state)

    frame_count += 1

    if frame_count >= ripple_delay and frame_count % ripple_freq == 0:
        ripple_delay = 0 #only run the ripple delay the first time
        frame_count = 0
        radius = random.randint(10, 50)

        ripple(radius, state, new_state)

    next_generation(state, new_state)

    old = state
    state = new_state
    new_state = old

# Be IDLE friendly
pygame.quit()