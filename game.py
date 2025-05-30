import os
import sys
sys.stdout = open(os.devnull, 'w')
import pygame
sys.stdout = sys.__stdout__
import random
from pygame.locals import *

SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 800

def load_game_font(size):
    try:
        return pygame.font.Font("./assets/game_font.ttf", size)
    except:
        return pygame.font.SysFont("Comic Sans MS", size)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("./assets/DiaSkin.png")
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 10)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("./assets/missile.png")
        self.rect = self.surf.get_rect(
            center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT))
        )
        if difficulty == 'easy':
            self.speed = random.randint(5, 30)
        elif difficulty == 'medium':
            self.speed = random.randint(30, 60)
        elif difficulty == 'hard':
            self.speed = random.randint(60, 100)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("./assets/NightCloud.png")
        self.rect = self.surf.get_rect(
            center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT))
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

def show_main_menu():
    screen.fill((0, 0, 0))
    title_font = load_game_font(72)
    menu_font = load_game_font(48)
    credit_font = load_game_font(24)  # Smaller font for the credit line

    title = title_font.render("TopGun Infinite", True, (255, 255, 0))
    credit = credit_font.render("Made By: Chanitha Abeygunawardena", True, (180, 180, 180))

    option1 = menu_font.render("Press [1] for EASY", True, (150, 255, 150))
    option2 = menu_font.render("Press [2] for MEDIUM", True, (255, 255, 150))
    option3 = menu_font.render("Press [3] for HARD", True, (255, 100, 100))

    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
    screen.blit(credit, (SCREEN_WIDTH//2 - credit.get_width()//2, 230))  # Position under title
    screen.blit(option1, (SCREEN_WIDTH//2 - option1.get_width()//2, 300))
    screen.blit(option2, (SCREEN_WIDTH//2 - option2.get_width()//2, 380))
    screen.blit(option3, (SCREEN_WIDTH//2 - option3.get_width()//2, 460))
    pygame.display.flip()

    level = None
    while level is None:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_1:
                    level = 'easy'
                elif event.key == K_2:
                    level = 'medium'
                elif event.key == K_3:
                    level = 'hard'
    return level


# Load high score if available
score_file = "highscore.txt"
try:
    with open(score_file, "r") as f:
        high_score = int(f.read())
except:
    high_score = 0

pygame.init()
clock = pygame.time.Clock()
font = load_game_font(36)
game_over_font = load_game_font(64)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

difficulty = show_main_menu()

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

player = Player()
all_sprites = pygame.sprite.Group(player)
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()

pygame.mixer.music.load("./assets/Gun.mp3")
pygame.mixer.music.play(loops=-1)
collision_sound = pygame.mixer.Sound("./assets/collision.wav")
explosion = pygame.image.load("./assets/explosion.png")

running = True
score = 0

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == ADDENEMY:
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)
        elif event.type == ADDCLOUD:
            cloud = Cloud()
            clouds.add(cloud)
            all_sprites.add(cloud)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()
    clouds.update()

    screen.fill((35, 32, 46))

    if pygame.sprite.spritecollideany(player, enemies):
        if player.alive():
            collision_sound.play()
            screen.blit(explosion, player.rect)
            pygame.display.flip()
            pygame.time.delay(1000)
        running = False

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    score += 1
    score_surface = font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))

    pygame.display.flip()
    clock.tick(30)

# Game Over screen
screen.fill((0, 0, 0))
final_score = game_over_font.render(f'Final Score: {score}', True, (255, 0, 0))
screen.blit(final_score, (SCREEN_WIDTH//2 - final_score.get_width()//2, SCREEN_HEIGHT//2 - 80))

if score > high_score:
    high_score = score
    with open(score_file, "w") as f:
        f.write(str(high_score))

high_score_text = font.render(f'High Score: {high_score}', True, (255, 255, 255))
screen.blit(high_score_text, (SCREEN_WIDTH//2 - high_score_text.get_width()//2, SCREEN_HEIGHT//2 - 10))

play_again_text = font.render("Press [R] to Play Again or [Q] to Quit", True, (200, 200, 200))
screen.blit(play_again_text, (SCREEN_WIDTH//2 - play_again_text.get_width()//2, SCREEN_HEIGHT//2 + 60))

pygame.display.flip()

# Wait for input
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_r:
                os.execv(sys.executable, ['python'] + sys.argv)
            elif event.key == K_q:
                waiting = False

pygame.quit()
sys.exit()

#hehe 
