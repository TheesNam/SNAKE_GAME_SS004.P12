import pygame
import time
import sys   
import random
from pygame.math import Vector2
from Button import Button


pygame.init()

title_font = pygame.font.Font("assets/font.ttf", 30)
score_title_font = pygame.font.Font("assets/font.ttf",20)
score_font = pygame.font.Font("assets/font.ttf", 25)

GREEN = (173, 204, 96)
DARK_GREEN = (43, 51, 24)
LIGHT_GREEN = (163, 194, 80)
snake_head=pygame.image.load("assets/meome.png")
snake_bodys= pygame.image.load("assets/meocon1.png")

cell_size = 30
number_of_cells = 25
BG_Game = pygame.image.load("assets/greenhill.jpg")
Snake_theme= [snake_head,snake_bodys,BG_Game]
OFFSET = 75

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

board_width = cell_size* number_of_cells
board_height = cell_size * number_of_cells
OFFSET_X = (screen_width - board_width) //2
OFFSET_Y = (screen_height - board_height) //2

pygame.mixer.music.load("gametheme.mp3")  
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)  

food_sound = pygame.mixer.Sound("eating.wav")  
food_sound.set_volume(0.3)
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)


class Food:
    def __init__(self, snake_body):
        self.types =[
            {"image": "assets/apple.png", "score": 1},
            {"image": "assets/banana.png", "score": 2},
            {"image": "assets/cherry.png", "score": 3},
        ]
        self.current_type = random.choice(self.types)
        self.position = self.generate_random_pos(snake_body)
        self.image = pygame.image.load(self.current_type["image"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.score_value = self.current_type["score"]

       
    
    def draw(self):
        food_rect = pygame.Rect( OFFSET_X + self.position.x * cell_size, 
                                OFFSET_Y + self.position.y * cell_size, 
                                cell_size, 
                                cell_size)
        screen.blit(self.image, food_rect)
        
    
    def generate_random_cell(self):
        x = random.randint(0, number_of_cells -1)
        y = random.randint(0, number_of_cells -1)
        return Vector2(x, y)
    
    def generate_random_pos(self, snake_body):
        position = self.generate_random_cell()
        while position in snake_body:
            position = self.generate_random_cell()
        return position

    def regenerate(self, snake_body):
        self.current_type = random.choice(self.types)
        self.image = pygame.image.load(self.current_type["image"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))
        self.score_value = self.current_type["score"]
        self.position = self.generate_random_pos(snake_body)

class Snake:
    def __init__(self):
        self.body = [Vector2(3, 1), Vector2(2,1), Vector2(1,1)]
        self.direction = Vector2(1, 0)
        self.add_segment = False
        self.head_images = {
            "UP": pygame.image.load("assets/headup.png").convert_alpha() ,
            "DOWN": pygame.image.load("assets/headdown.png").convert_alpha(),
            "LEFT": pygame.image.load("assets/headleft.png").convert_alpha(),
            "RIGHT": pygame.image.load("assets/headright.png").convert_alpha()
            
        }
        self.head_images = {key: pygame.transform.scale(image, (cell_size, cell_size)) 
                            for key, image in self.head_images.items()}
        self.head_image = self.head_images["RIGHT"] 
        self.body_image = pygame.image.load("assets/body.png").convert_alpha()
        self.body_image = pygame.transform.scale(self.body_image, (cell_size, cell_size))
        
    def draw(self):

        head_rect = pygame.Rect(OFFSET_X + self.body[0].x * cell_size, 
                                OFFSET_Y + self.body[0].y * cell_size, 
                                cell_size, cell_size)
        screen.blit(self.head_image, head_rect)

        for segment in self.body[1:]:
            segment_rect = self.body_image.get_rect(
                topleft=(OFFSET_X + segment.x * cell_size, OFFSET_Y + segment.y * cell_size))
            screen.blit(self.body_image, segment_rect)
            
    def update(self):
        self.body.insert(0, self.body[0] + self.direction)
        if self.add_segment == True:
            self.add_segment = False
        else:    
            self.body = self.body[:-1]
    
    def reset(self):
        self.body = [Vector2(3, 1), Vector2(2, 1), Vector2(1, 1)]
        self.head_image = self.head_images["RIGHT"] 
    
    def update_head_image(self):
        if self.direction == Vector2(0, -1):
            self.head_image = self.head_images["UP"]
        elif self.direction == Vector2(0, 1):
            self.head_image = self.head_images["DOWN"]
        elif self.direction == Vector2(-1, 0):
            self.head_image = self.head_images["LEFT"]
        elif self.direction == Vector2(1, 0):
            self.head_image = self.head_images["RIGHT"]
def mode():
    global toc_do_ran
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill("white")
        
        OPTIONS_EASY = Button(image=None, pos=(640, 150), 
                            text_input="EASY", font=get_font(75), base_color="Black", hovering_color="Green")
        
        OPTIONS_NORMAL = Button(image=None, pos=(640, 300), 
                            text_input="NORMAL", font=get_font(75), base_color="Black", hovering_color="Green")
        
        OPTIONS_HARD = Button(image=None, pos=(640, 450), 
                            text_input="HARD", font=get_font(75), base_color="Black", hovering_color="Green")
        
        OPTIONS_EASY.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_NORMAL.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_HARD.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_EASY.update(screen)
        OPTIONS_NORMAL.update(screen)
        OPTIONS_HARD.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_EASY.checkForInput(OPTIONS_MOUSE_POS):
                    toc_do_ran = 10
                    option = Options(screen)
                    option.options()
                if OPTIONS_NORMAL.checkForInput(OPTIONS_MOUSE_POS):
                    toc_do_ran=20
                    option = Options(screen)
                    option.options()
                if OPTIONS_HARD.checkForInput(OPTIONS_MOUSE_POS):
                    toc_do_ran=30
                    option = Options(screen)
                    option.options()
        
        pygame.display.update()
def theme():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        screen.fill("white")
        
        OPTIONS_MEOW = Button(image=None, pos=(640, 150), 
                            text_input="CAT", font=get_font(75), base_color="Black", hovering_color="Green")
        
        OPTIONS_FISH = Button(image=None, pos=(640, 300), 
                            text_input="FISH", font=get_font(75), base_color="Black", hovering_color="Green")
        
        OPTIONS_UFO = Button(image=None, pos=(640, 450), 
                            text_input="UFO", font=get_font(75), base_color="Black", hovering_color="Green")
        
        OPTIONS_MEOW.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_FISH.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_UFO.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_MEOW.update(screen)
        OPTIONS_FISH.update(screen)
        OPTIONS_UFO.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_MEOW.checkForInput(OPTIONS_MOUSE_POS):
                    Snake_theme[0]=pygame.image.load("assets/meome.png")
                    Snake_theme[0]=pygame.transform.scale(Snake_theme[0],(40,40))
                    
                    Snake_theme[1][0]=pygame.image.load("assets/meocon1.png")
                    Snake_theme[1][0]=pygame.transform.scale(Snake_theme[1][0],(40,40))
                    
                    Snake_theme[1][1]=pygame.image.load("assets/meocon2.png")
                    Snake_theme[1][1]=pygame.transform.scale(Snake_theme[1][1],(40,40))
                    
                    Snake_theme[1][2]=pygame.image.load("assets/meocon3.png")
                    Snake_theme[1][2]=pygame.transform.scale(Snake_theme[1][2],(40,40))
                    
                    Snake_theme[2]=pygame.image.load("assets/greenhill.jpg")
                    
                    option = Options(screen)
                    option.options()
                    
                if OPTIONS_FISH.checkForInput(OPTIONS_MOUSE_POS):
                    Snake_theme[0]=pygame.image.load("assets/clownfish.png")
                    Snake_theme[0]=pygame.transform.scale(Snake_theme[0],(40,40))
                    
                    Snake_theme[1][0]=pygame.image.load("assets/shark.png")
                    Snake_theme[1][0]=pygame.transform.scale(Snake_theme[1][0],(40,40))
                    
                    Snake_theme[1][1]=pygame.image.load("assets/turtle.png")
                    Snake_theme[1][1]=pygame.transform.scale(Snake_theme[1][1],(40,40))
                    
                    Snake_theme[1][2]=pygame.image.load("assets/bluefish.png")
                    Snake_theme[1][2]=pygame.transform.scale(Snake_theme[1][2],(40,40))
                    
                    Snake_theme[2]=pygame.image.load("assets/underwater.png")
                    option = Options(screen)
                    option.options()

                    
                if OPTIONS_UFO.checkForInput(OPTIONS_MOUSE_POS):
                    Snake_theme[0]=pygame.image.load("assets/theUFO.png")
                    Snake_theme[0]=pygame.transform.scale(Snake_theme[0],(40,40))
                    
                    Snake_theme[1][0]=pygame.image.load("assets/cow.png")
                    Snake_theme[1][0]=pygame.transform.scale(Snake_theme[1][0],(40,40))
                    
                    Snake_theme[1][1]=pygame.image.load("assets/person.png")
                    Snake_theme[1][1]=pygame.transform.scale(Snake_theme[1][1],(40,40))
                    
                    Snake_theme[1][2]=pygame.image.load("assets/plant.png")
                    Snake_theme[1][2]=pygame.transform.scale(Snake_theme[1][2],(40,40))
                    
                    Snake_theme[2]=pygame.image.load("assets/demdaysao.jpg")
                    option = Options(screen)
                    option.options()
        
        pygame.display.update()
class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = Food(self.snake.body)
        self.state = "RUNNING"
        self.score = 0
        self.best_score = 0
    
    def draw(self):
        for row in range(number_of_cells):
            for col in range(number_of_cells):
                color = LIGHT_GREEN if (row + col) % 2 == 0 else GREEN
                cell_rect = pygame.Rect(OFFSET_X + col * cell_size, 
                                        OFFSET_Y + row * cell_size, 
                                        cell_size, 
                                        cell_size)
                pygame.draw.rect(screen, color, cell_rect)
        
        self.snake.draw()
        self.food.draw()
    
    def update(self):
        if self.state == "RUNNING":
            self.snake.update()
            self.snake.update_head_image()
            self.check_collision_with_the_food()
            self.check_collision_with_edges()
            self.check_collision_with_tail()
    
    def check_collision_with_the_food(self):
        if self.snake.body[0] == self.food.position:
            self.score += self.food.score_value  
            self.food.regenerate(self.snake.body)
            self.snake.add_segment = True
            food_sound.play()
    
    def check_collision_with_edges(self):
        if self.snake.body[0].x == number_of_cells or self.snake.body[0].x == -1:
            self.game_over()
        if self.snake.body[0].y == number_of_cells or self.snake.body[0].y == -1:
            self.game_over()
    
    def game_over(self):
        if self.score > self.best_score:  
            self.best_score = self.score
        self.snake.reset()
        self.food.position = self.food.generate_random_pos(self.snake.body)
        self.state = "STOPPED"
        self.score = 0
        
    def check_collision_with_tail(self):
        headless_body = self.snake.body [1:]
        if self.snake.body[0] in headless_body:
            self.game_over()
    #def run(self):
        
class Options:
    def __init__(self, screen):
        self.screen = screen
        self.back_button = Button(image=None, pos=(640, 450), 
                                  text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
        self.mode_button = Button(image=None, pos=(640, 300), 
                                  text_input="MODE", font=get_font(75), base_color="Black", hovering_color="Green")
        self.theme_button = Button(image=None, pos=(640, 150), 
                                   text_input="THEME", font=get_font(75), base_color="Black", hovering_color="Green")



    def options(self):
        while True:
            options_mouse_pos = pygame.mouse.get_pos()

            self.screen.fill("white")

            self.back_button.changeColor(options_mouse_pos)
            self.back_button.update(self.screen)

            self.mode_button.changeColor(options_mouse_pos)
            self.mode_button.update(self.screen)

            self.theme_button.changeColor(options_mouse_pos)
            self.theme_button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.checkForInput(options_mouse_pos):
                        menu = Menu(screen, BG)
                        menu.main_menu()
                    if self.mode_button.checkForInput(options_mouse_pos):
                        mode()
                    if self.theme_button.checkForInput(options_mouse_pos):
                        theme()
            pygame.display.update()
class Menu:
    def __init__(self, screen, bg):
        self.screen = screen
        self.bg = bg
        self.buttons = [
            Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 350), 
                   text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White"),
           # Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
           #        text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White"),
           # Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
           #       text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        ]
    def main_menu(self):
        while True:
            self.screen.blit(self.bg, (0, 0))
            menu_mouse_pos = pygame.mouse.get_pos()
            menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
            menu_rect = menu_text.get_rect(center=(640, 100))
            self.screen.blit(menu_text, menu_rect)

            for button in self.buttons:
                button.changeColor(menu_mouse_pos)
                button.update(self.screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.buttons[0].checkForInput(menu_mouse_pos):
                        game= Game()
                        return
                    if self.buttons[1].checkForInput(menu_mouse_pos):
                                                option = Options(screen)
                                                option.options()
                    if self.buttons[2].checkForInput(menu_mouse_pos):
                                                pygame.quit()
                                                sys.exit()

                pygame.display.update()
#SCREEN = pygame.display.set_mode((1280, 720))
SCREEN = pygame.display.set_mode((1280, 720))
BG = pygame.image.load("assets/1.png")
menu = Menu(SCREEN,BG)
menu.main_menu()
screen = pygame.display.set_mode ((screen_width, 
                                   screen_height), 
                                  pygame.FULLSCREEN)
pygame.display.set_caption("SNAKE GAME")
clock = pygame.time.Clock()
game = Game()
SNAKE_UPDATE = pygame.USEREVENT 
pygame.time.set_timer(SNAKE_UPDATE, 200)
game.state = "STOPPED" 
while True:
    for event in pygame.event.get():
        if event.type == SNAKE_UPDATE:
            game.update()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.state = "PAUSE_MENU"  

            if game.state == "PAUSE_MENU":
                if event.key == pygame.K_1:  
                    game.state = "RUNNING"
                elif event.key == pygame.K_2:  
                    game = Game()
                    game.state = "RUNNING"
                elif event.key == pygame.K_3: 
                    pygame.quit()
                    sys.exit()
            if event.key == pygame.K_SPACE:
                if game.state == "RUNNING":
                    game.state = "PAUSED"  
                elif game.state == "PAUSED":
                    game.state = "RUNNING"     
            elif game.state == "STOPPED":
                game.state = "RUNNING"
            
            else:
                if event.key == pygame.K_UP and game.snake.direction != Vector2(0, 1):
                    game.snake.direction = Vector2(0, -1)
                    game.snake.update_head_image()
                if event.key == pygame.K_DOWN and game.snake.direction != Vector2(0, -1):
                    game.snake.direction = Vector2(0, 1)
                    game.snake.update_head_image()
                if event.key == pygame.K_LEFT and game.snake.direction != Vector2(1, 0):
                    game.snake.direction = Vector2(-1, 0)
                    game.snake.update_head_image()
                if event.key == pygame.K_RIGHT and game.snake.direction != Vector2(-1, 0):
                    game.snake.direction = Vector2(1, 0)
                    game.snake.update_head_image()
    
            
    screen.fill(GREEN)        
    pygame.draw.rect(screen, DARK_GREEN, 
                     (OFFSET_X - 5, 
                      OFFSET_Y - 5, 
                      board_width + 10, 
                      board_height + 10), 
                     5)
    if game.state != "PAUSE":
        game.draw()
    if game.state == "PAUSED":
        pause_surface = title_font.render("PAUSE GAME", True, DARK_GREEN)
        pause_X = (screen_width - pause_surface.get_width()) // 2
        pause_Y = (screen_height - pause_surface.get_height()) // 2
        screen.blit(pause_surface, (pause_X, pause_Y))
    title_surface_1 = title_font.render("SNAKE", True, DARK_GREEN)
    title_surface_2 = title_font.render("GAME", True, DARK_GREEN)
    score_title_surface = title_font.render("SCORE", True, DARK_GREEN)
    score_surface = score_font.render(str(game.score), True, DARK_GREEN)
    best_title_surface = score_font.render("BESTSCORE", True, DARK_GREEN)
    best_score_suface = score_font.render (str(game.best_score), True, DARK_GREEN)
    if game.state == "PAUSE_MENU":
        
        title_surface = title_font.render("PAUSE MENU", True, DARK_GREEN)
        title_rect = title_surface.get_rect(center=(screen_width // 2, screen_height // 4))
        screen.blit(title_surface, title_rect)

        resume_text = score_font.render("1: Resume", True, DARK_GREEN)
        reset_text = score_font.render("2: Reset", True, DARK_GREEN)
        quit_text = score_font.render("3: Quit", True, DARK_GREEN)

        screen.blit(resume_text, (screen_width // 2 - 100, screen_height // 2 - 50))
        screen.blit(reset_text, (screen_width // 2 - 100, screen_height // 2))
        screen.blit(quit_text, (screen_width // 2 - 100, screen_height // 2 + 50))    

    
    title_X = OFFSET_X - 10 - title_surface_1.get_width()
    title_Y_1 = OFFSET_Y
    title_Y_2 = title_Y_1 - title_surface_1.get_height()
    
    score_title_X = OFFSET_X +board_width + score_title_surface.get_width()
    score_title_Y = OFFSET_Y
    
    score_X = score_title_X - 12 + score_title_surface.get_width()/2 
    score_Y = OFFSET_Y*1.5 + score_title_surface.get_height()

    best_title_X = score_title_X - 30 
    best_title_Y = score_Y + score_surface.get_height() + 20

    best_score_X = score_X
    best_score_Y = best_title_Y + best_title_surface.get_height() + 10 

    
    screen.blit(title_surface_1, (title_X, title_Y_1))
    screen.blit(title_surface_2, (title_X, title_Y_2))
    screen.blit(score_title_surface, (score_title_X, score_title_Y))
    screen.blit(score_surface, (score_X , score_Y))
    screen.blit(best_title_surface, (best_title_X, best_title_Y)) 
    screen.blit(best_score_suface, (best_score_X, best_score_Y))

    pygame.display.update()
    clock.tick(60)
