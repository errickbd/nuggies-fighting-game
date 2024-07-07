import pygame
from fighter import Fighter

pygame.init()

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("NUGGIE FIGHTERS")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define colours
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE= (255, 255, 255)

#define fighter variables
NUGGIE01_SIZE = 162
NUGGIE01_DATA = [NUGGIE01_SIZE]
NUGGIE02_SIZE = 162
NUGGIE02_DATA = [NUGGIE02_SIZE]

#load background image
bg_image = pygame.image.load("assets/background01.jpeg").convert_alpha()

#load spritesheets
nuggie01_sheet = pygame.image.load("assets/fighter01.webp").convert_alpha()
nuggie02_sheet = pygame.image.load("assets/fighter02.webp").convert_alpha()

#define number of steps in each animation
NUGGIE01_ANIMATION_STEPS = [1]
NUGGIE02_ANIMATION_STEPS = [1]

#function for drawing background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0,0))

def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# create two instances of fighters
fighter_1 = Fighter(200, 310,NUGGIE01_DATA, nuggie01_sheet, NUGGIE01_ANIMATION_STEPS)
fighter_2 = Fighter(700, 310,NUGGIE02_DATA, nuggie02_sheet, NUGGIE02_ANIMATION_STEPS)


#game loop
run = True
while run:

    clock.tick(FPS)

    #draw background
    draw_bg()

    #show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)

    #move fighters
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
    

    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)


    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()

#exit pygame
pygame.quit()

