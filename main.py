import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = int(600 * 1.5), int(400 * 1.5)
BALL_SIZE = 20
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 40  # Adjusted size
PADDLE_DISTANCE = 20  # Distance from the screen edge
FPS = 60
WHITE = (255, 255, 255)
FONT_SIZE = 36

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Initialize game variables
ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_speed = [5, 5]
left_paddle_pos = [PADDLE_DISTANCE, HEIGHT // 2 - PADDLE_HEIGHT // 2]
right_paddle_pos = [WIDTH - PADDLE_WIDTH - PADDLE_DISTANCE, HEIGHT // 2 - PADDLE_HEIGHT // 2]
left_paddle_speed = 0
right_paddle_speed = 0
score_left = 0
score_right = 0
start_time = pygame.time.get_ticks()

# Game loop
clock = pygame.time.Clock()

def reset_ball():
    return [WIDTH // 2, HEIGHT // 2]

def display_text(text, position, color=WHITE, font_size=FONT_SIZE):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                right_paddle_speed = -5
            elif event.key == pygame.K_DOWN:
                right_paddle_speed = 5
            elif event.key == pygame.K_w:
                left_paddle_speed = -5
            elif event.key == pygame.K_s:
                left_paddle_speed = 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                right_paddle_speed = 0
            elif event.key == pygame.K_w or event.key == pygame.K_s:
                left_paddle_speed = 0

    # Update paddles and ball
    left_paddle_pos[1] += left_paddle_speed
    right_paddle_pos[1] += right_paddle_speed

    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # Bounce the ball off the top and bottom walls
    if ball_pos[1] <= 0 or ball_pos[1] >= HEIGHT - BALL_SIZE:
        ball_speed[1] = -ball_speed[1]

    # Reset the game when the ball hits the left or right edge
    if ball_pos[0] <= 0:
        score_right += 1
        ball_pos = reset_ball()
    elif ball_pos[0] >= WIDTH - BALL_SIZE:
        score_left += 1
        ball_pos = reset_ball()

    # Bounce the ball off paddles
    if (
        left_paddle_pos[0] <= ball_pos[0] <= left_paddle_pos[0] + PADDLE_WIDTH
        and left_paddle_pos[1] <= ball_pos[1] <= left_paddle_pos[1] + PADDLE_HEIGHT
    ) or (
        right_paddle_pos[0] <= ball_pos[0] + BALL_SIZE <= right_paddle_pos[0] + PADDLE_WIDTH
        and right_paddle_pos[1] <= ball_pos[1] <= right_paddle_pos[1] + PADDLE_HEIGHT
    ):
        ball_speed[0] = -ball_speed[0]
        ball_speed[1] = random.uniform(-7, 7)  # Randomize the vertical speed

    # Draw everything
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, WHITE, (left_paddle_pos[0], left_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(screen, WHITE, (right_paddle_pos[0], right_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.ellipse(screen, WHITE, (ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE))

    # Display scores
    display_text(str(score_left), (WIDTH // 4, 20))
    display_text(str(score_right), (WIDTH * 3 // 4 - FONT_SIZE, 20))

    # Display timer
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    display_text(f"Time: {elapsed_time}s", (WIDTH // 2 - 70, HEIGHT - 50), color=WHITE, font_size=24)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)