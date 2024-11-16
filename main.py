import pygame
import time
import sys   
import random
from pygame.math import Vector2

pygame.init()

GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)

cell_size = 30
number_of_cells = 25

class Food:
    def __init__(seft):
        seft.position = seft.generate_random_pos()
    
    def draw(seft):
        food_rect = pygame.Rect(seft.position.x * cell_size, seft.position.y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, DARK_GREEN, food_rect)
    
    def generate_random_pos(seft):
        x = random.randint(0, number_of_cells -1)
        y = random.randint(0, number_of_cells -1)
        position = Vector2(x, y)
        return position   

class Snake:
    def __init__(seft):
        seft.body = [Vector2(1, 1), Vector2(2,1),Vector2(3,1)]
    def draw(seft):
        for segment in seft.body:
            segment_rect = (segment.x * cell_size, segment.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, DARK_GREEN, segment_rect)    
    
screen = pygame.display.set_mode ((cell_size*number_of_cells, cell_size*number_of_cells))

pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

food = Food()

snake = Snake()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    screen.fill(GREEN)        
    food.draw()
    snake.draw()
    pygame.display.update()
    clock.tick(60)
