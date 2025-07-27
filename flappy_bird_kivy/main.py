import pygame, sys, random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Load images
bg = pygame.image.load("assets/background.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

bird_img = pygame.image.load("assets/bird.png")
bird_img = pygame.transform.scale(bird_img, (40, 30))

pipe_img = pygame.image.load("assets/pipe.png")
pipe_img = pygame.transform.scale(pipe_img, (60, 400))

ground_img = pygame.image.load("assets/ground.png")
ground_img = pygame.transform.scale(ground_img, (WIDTH, 100))

# Game variables
bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -7
bird_rect = bird_img.get_rect(center=(bird_x, bird_y))

pipes = []
pipe_gap = 150
pipe_speed = 3

def create_pipe():
    height = random.randint(150, 350)
    top_rect = pipe_img.get_rect(midbottom=(WIDTH + 50, height))
    bottom_rect = pipe_img.get_rect(midtop=(WIDTH + 50, height + pipe_gap))
    return top_rect, bottom_rect

# Initial pipe
pipes.append(create_pipe())

# Score and font
score = 0
font = pygame.font.Font(None, 40)

# Game state
game_active = False

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Spacebar handling
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_active:
                # Restart game when SPACE is pressed at start screen
                game_active = True
                bird_y = HEIGHT // 2
                bird_velocity = 0
                pipes = [create_pipe()]
                score = 0
            else:
                bird_velocity = jump_strength

    # Draw background always
    screen.blit(bg, (0, 0))

    if game_active:
        # Bird physics
        bird_velocity += gravity
        bird_y += bird_velocity
        bird_rect.centery = bird_y

        # Move pipes
        for i in range(len(pipes)):
            pipes[i] = (pipes[i][0].move(-pipe_speed, 0), pipes[i][1].move(-pipe_speed, 0))

        # Add new pipes
        if pipes[-1][0].centerx < WIDTH // 2:
            pipes.append(create_pipe())

        # Remove old pipes
        if pipes[0][0].right < 0:
            pipes.pop(0)
            score += 1

        # Draw pipes
        for top_rect, bottom_rect in pipes:
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, top_rect)    # top pipe flipped
            screen.blit(pipe_img, bottom_rect)     # bottom pipe normal

        # Draw bird
        screen.blit(bird_img, bird_rect)

        # Draw ground
        screen.blit(ground_img, (0, HEIGHT - 100))

        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Collision detection
        for top_rect, bottom_rect in pipes:
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                game_active = False

        if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT - 100:
            game_active = False

    else:
        # Start screen message
        start_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        screen.blit(start_text, (WIDTH//2 - 120, HEIGHT//2))

    pygame.display.flip()
    clock.tick(60)
