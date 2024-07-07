import pygame

class Fighter():
    def __init__(self, player, x, y, flip, data, image, animation_steps):
        self.player = player
        self.size = data[0]
        self.image_scale = data[1]
        self.flip = flip
        self.image = pygame.transform.scale(image, (self.size // self.image_scale, 175))
        self.rect = pygame.Rect((x, y, self.size // self.image_scale, self.size // self.image_scale))
        self.vel_y = 0
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100
        self.alive = True
        self.attack_timer = 0
        self.attack_duration = 25  # Adjust this value as needed

    def move(self, screen_width, screen_height, surface, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.attack_type = 0

        # Get keypresses
        key = pygame.key.get_pressed()

        # Only perform other actions if not attacking
        if not self.attacking and self.alive == True:
            #check player 1 controls
            if self.player == 1:
                # Movement
                if key[pygame.K_a]:
                    dx = -SPEED
                if key[pygame.K_d]:
                    dx = SPEED
                # Jump
                if key[pygame.K_w] and not self.jump:
                    self.vel_y = -30
                    self.jump = True

                # Attack
                if key[pygame.K_r] or key[pygame.K_t]:
                    self.attack(target)
                    # Determine which attack type was used
                    if key[pygame.K_r]:
                        self.attack_type = 1
                    if key[pygame.K_t]:
                        self.attack_type = 2


            #check player 2 controls
            if self.player == 2:
                # Movement
                if key[pygame.K_LEFT]:
                    dx = -SPEED
                if key[pygame.K_RIGHT]:
                    dx = SPEED
                # Jump
                if key[pygame.K_UP] and not self.jump:
                    self.vel_y = -30
                    self.jump = True

                # Attack
                if key[pygame.K_KP1] or key[pygame.K_KP2]:
                    self.attack(target)
                    # Determine which attack type was used
                    if key[pygame.K_KP1]:
                        self.attack_type = 1
                    if key[pygame.K_KP2]:
                        self.attack_type = 2

        # Apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.vel_y = 0
            self.jump = False
            dy = screen_height - 110 - self.rect.bottom

        # Ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            # print("Fighter Dead")
        if self.attacking:
            self.attack_timer += 1
            if self.attack_timer >= self.attack_duration:
                self.attacking = False
                self.attack_timer = 0
        

    def attack(self, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (1.25 * self.rect.width * self.flip), self.rect.y, 1.25 * self.rect.width, self.rect.height)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x, self.rect.y))
