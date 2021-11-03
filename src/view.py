import pygame
import time
from random import randrange

pygame.init()

height = 6
width = 42
window = pygame.display.set_mode((1360 ,180)) #Mi monitor es chico, cambio un pco la reso
block_size = 20



grid = [[],[],[],[],[],[]]

for i in range(height):
    for j in range(width):
        grid[i].append(0)

rect = pygame.Rect(0, 0, 120, 180)
pygame.draw.rect(window, (0,150,0), rect)

rect = pygame.Rect(1420, 0, 120, 180)
pygame.draw.rect(window, (0,150,0), rect)


myfont = pygame.font.SysFont("Comic Sans MS", 20)
label = myfont.render("Waiting Area", 1, (0,0,0))
window.blit(label, (1430, 10))
window.blit(label, (10, 10))
step = 0.5

while True:
    if (randrange(11) <= 5):
        grid[randrange(6)][0] = 1

    for fila in range(height):
        for columna in range(width):
            rect = pygame.Rect(columna*(block_size+1) + 120, fila*(block_size+1), block_size, block_size)
            pygame.draw.rect(window, (255,255,255), rect)
            if (grid[fila][columna] == 1):
                rect = pygame.Rect(columna*(block_size+1) + 120, fila*(block_size+1), block_size, block_size)
                pygame.draw.rect(window, (255,0,0), rect)

    
    grid_copy = [[],[],[],[],[],[]]
    
    for fila in range(6):
        for columna in range(42):
            grid_copy[fila].append(0)
    for fila in range(6):
        for columna in range(42):
            if (grid[fila][columna] == 1):
                if (columna + 1 < 42):
                    grid_copy[fila][columna + 1] = 1
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and step > 0:
            if event.key == pygame.K_w:
                step += 0.05
            if event.key == pygame.K_s:
                step -= 0.05
    grid = grid_copy
    pygame.display.update()
    time.sleep(step)
