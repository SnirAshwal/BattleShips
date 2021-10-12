import sys
import pygame
import os

pygame.init()

# game photos and variables
SCREEN_HEIGHT = 700
SCREEN_WIDTH = 1100
GAME_NAME = "BATTLESHIPS"
GAME_LOGO = pygame.image.load(os.path.join('Assets', 'game_logo.png'))
SPACESHIP_WIDTH = 80
SPACESHIP_LENGTH = 80
SPACESHIP_SIZE = (SPACESHIP_WIDTH, SPACESHIP_LENGTH)
MIDDLE_LINE_WIDTH = 10
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load(os.path.join("Assets", "red_spaceship.png")), SPACESHIP_SIZE), 90)
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(pygame.image.load(os.path.join("Assets", "yellow_spaceship.png")), SPACESHIP_SIZE), -90)
VEL = 10  # velocity
BULLET_VEL = 20  # bullet velocity
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BULLET_WIDTH = 8
BULLET_HEIGHT = 8
LIVES = 10
MAX_BULLETS = 3
SCORES_Y_POS = 20
SCORE_FONT = pygame.font.Font('freesansbold.ttf', 42)
WINNER_FONT = pygame.font.Font('freesansbold.ttf', 42)
RED_WINNER_TEXT = "RED PLAYER WINS!"
YELLOW_WINNER_TEXT = "YELLOW PLAYER WINS!"

# sounds
LASER_SOUND = pygame.mixer.Sound('Assets/laser_shot_sound.wav')
SPACESHIP_HIT_SOUND = pygame.mixer.Sound('Assets/spaceship_hit_sound.wav')
WIN_SOUND = pygame.mixer.Sound('Assets/win_sound.wav')

# creates events when there is a hit
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

# the middle line that separates the board
MIDDLE_LINE = pygame.Surface((MIDDLE_LINE_WIDTH, SCREEN_HEIGHT))

# the space background
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space_background.jpg")),
                                    (SCREEN_WIDTH, SCREEN_HEIGHT))

# create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)
pygame.display.set_icon(GAME_LOGO)


# the game play
def game(red_bullets, yellow_bullets, red_spaceship, yellow_spaceship, yellow_player_lives, red_player_lives):
    screen.blit(BACKGROUND, (0, 0))
    screen.blit(MIDDLE_LINE, ((SCREEN_WIDTH - MIDDLE_LINE.get_width()) // 2, 0))
    screen.blit(YELLOW_SPACESHIP, yellow_spaceship)
    screen.blit(RED_SPACESHIP, red_spaceship)
    for bullet in red_bullets:
        pygame.draw.rect(screen, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(screen, YELLOW, bullet)
    scores(yellow_player_lives, red_player_lives)
    pygame.display.update()


# handles collisions and bullets getting out of the screen
def handle_bullets(red_bullets, yellow_bullets, red_spaceship, yellow_spaceship):
    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow_spaceship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red_spaceship.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > SCREEN_WIDTH:
            yellow_bullets.remove(bullet)


def yellow_movement(key_input, yellow_spaceship):
    if key_input[pygame.K_w] and yellow_spaceship.y > 0:
        yellow_spaceship.y -= VEL
    if key_input[pygame.K_s] and yellow_spaceship.y < SCREEN_HEIGHT - YELLOW_SPACESHIP.get_height():
        yellow_spaceship.y += VEL
    if key_input[pygame.K_d] and yellow_spaceship.x < (SCREEN_WIDTH // 2) - YELLOW_SPACESHIP.get_width():
        yellow_spaceship.x += VEL
    if key_input[pygame.K_a] and yellow_spaceship.x > 0:
        yellow_spaceship.x -= VEL


def red_movement(key_input, red_spaceship):
    if key_input[pygame.K_UP] and red_spaceship.y > 0:
        red_spaceship.y -= VEL
    if key_input[pygame.K_DOWN] and red_spaceship.y < SCREEN_HEIGHT - RED_SPACESHIP.get_height():
        red_spaceship.y += VEL
    if key_input[pygame.K_RIGHT] and red_spaceship.x < SCREEN_WIDTH - RED_SPACESHIP.get_width():
        red_spaceship.x += VEL
    if key_input[pygame.K_LEFT] and red_spaceship.x > SCREEN_WIDTH // 2 + MIDDLE_LINE.get_width():
        red_spaceship.x -= VEL


def scores(yellow_player_lives, red_player_lives):
    red_text = SCORE_FONT.render(str(red_player_lives), True, RED)
    red_text_rect = pygame.Rect((SCREEN_WIDTH // 2) + 20, SCORES_Y_POS, red_text.get_width(), red_text.get_height())
    screen.blit(red_text, red_text_rect)
    yellow_text = SCORE_FONT.render(str(yellow_player_lives), True, YELLOW)
    yellow_text_rect = pygame.Rect((SCREEN_WIDTH // 2) - 20 - yellow_text.get_width(),
                                   SCORES_Y_POS, red_text.get_width(), red_text.get_height())
    screen.blit(yellow_text, yellow_text_rect)


def draw_winner(text, color):
    winner_text = SCORE_FONT.render(text, True, color)
    winner_rect = pygame.Rect((SCREEN_WIDTH - winner_text.get_width()) // 2, SCREEN_HEIGHT // 2,
                              winner_text.get_width(),
                              winner_text.get_height())
    screen.blit(winner_text, winner_rect)
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    red_spaceship = pygame.Rect(SCREEN_WIDTH - (RED_SPACESHIP.get_width() * 1.5),
                                (SCREEN_HEIGHT - RED_SPACESHIP.get_height()) // 2, SPACESHIP_WIDTH, SPACESHIP_LENGTH)
    yellow_spaceship = pygame.Rect(YELLOW_SPACESHIP.get_width() // 2,
                                   (SCREEN_HEIGHT - YELLOW_SPACESHIP.get_height()) // 2, SPACESHIP_WIDTH,
                                   SPACESHIP_LENGTH)

    # the arrays that contains the bullets
    yellow_bullets = []
    red_bullets = []

    yellow_player_lives = LIVES
    red_player_lives = LIVES
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    red_bullet = pygame.Rect(red_spaceship.x, red_spaceship.y + (RED_SPACESHIP.get_height() // 2),
                                             BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(red_bullet)
                    LASER_SOUND.play()

                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    yellow_bullet = pygame.Rect(yellow_spaceship.x + YELLOW_SPACESHIP.get_width(),
                                                yellow_spaceship.y + (YELLOW_SPACESHIP.get_height() // 2),
                                                BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(yellow_bullet)
                    LASER_SOUND.play()

            if event.type == RED_HIT:
                yellow_player_lives -= 1
                SPACESHIP_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                red_player_lives -= 1
                SPACESHIP_HIT_SOUND.play()

        winner = ''

        if yellow_player_lives <= 0:
            winner = RED_WINNER_TEXT
            color = RED

        if red_player_lives <= 0:
            winner = YELLOW_WINNER_TEXT
            color = YELLOW

        if winner != '':
            WIN_SOUND.play()
            draw_winner(winner, color)
            break

        key_input = pygame.key.get_pressed()
        red_movement(key_input, red_spaceship)
        yellow_movement(key_input, yellow_spaceship)
        handle_bullets(red_bullets, yellow_bullets, red_spaceship, yellow_spaceship)
        game(red_bullets, yellow_bullets, red_spaceship, yellow_spaceship, yellow_player_lives, red_player_lives)

    main()


if __name__ == '__main__':
    main()
