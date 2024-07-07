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

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#[p1, p2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#define fighter variables
NUGGIE01_SIZE = 275
NUGGIE01_SCALE = 2
NUGGIE01_DATA = [NUGGIE01_SIZE, NUGGIE01_SCALE]
NUGGIE02_SIZE = 275
NUGGIE02_SCALE = 2
NUGGIE02_DATA = [NUGGIE02_SIZE, NUGGIE02_SCALE]

#load background image
bg_image = pygame.image.load("assets/background01.jpeg").convert_alpha()

#load spritesheets
nuggie01_image = pygame.image.load("assets/fighter01.webp").convert_alpha()
nuggie02_image = pygame.image.load("assets/fighter02.webp").convert_alpha()

#load victory image
victory_img = pygame.image.load("assets/victory.png").convert_alpha()

# scale down the victory image
victory_img = pygame.transform.scale(victory_img, (200, 100)) 

#define number of steps in each animation
NUGGIE01_ANIMATION_STEPS = [1]
NUGGIE02_ANIMATION_STEPS = [1]

#define font
count_font = pygame.font.Font("assets/fonts/Turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/Turok.ttf", 30)

#function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

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
fighter_1 = Fighter(1, 200, 353, False, NUGGIE01_DATA, nuggie01_image, NUGGIE01_ANIMATION_STEPS)
fighter_2 = Fighter(2, 700, 353, True, NUGGIE02_DATA, nuggie02_image, NUGGIE02_ANIMATION_STEPS)


#game loop
run = True
while run:

    clock.tick(FPS)

    #draw background
    draw_bg()

    #show player stats
    draw_health_bar(fighter_1.health, 20, 20)
    draw_health_bar(fighter_2.health, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
    draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

    #update countdown
    if intro_count <= 0:
        #move fighters
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2)
        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1)
    else:
        #dispaly count timer
        draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        #update count timer
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()
            
        
    #update fighters
    fighter_1.update()
    fighter_2.update()

    #draw fighters
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    #check for player defeat
    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        #display victory image
        screen.blit(victory_img, (390, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Fighter(1, 200, 353, False, NUGGIE01_DATA, nuggie01_image, NUGGIE01_ANIMATION_STEPS)
            fighter_2 = Fighter(2, 700, 353, True, NUGGIE02_DATA, nuggie02_image, NUGGIE02_ANIMATION_STEPS)

    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.update()

#exit pygame
pygame.quit()

