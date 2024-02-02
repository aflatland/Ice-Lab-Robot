import pygame
import numpy as np

# Initialize Pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((300, 300))
pygame.display.set_caption("IceBot")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load and play audio
pygame.mixer.music.load("gptResponse.mp3")
pygame.mixer.music.play()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear screen
    screen.fill(WHITE)

    # Draw face
    # Eyes
    pygame.draw.circle(screen, BLACK, (100, 100), 10)
    pygame.draw.circle(screen, BLACK, (200, 100), 10)

    # Mouth
    if pygame.mixer.music.get_busy():  # Check if audio is playing
        mouth_width = 100
        mouth_height = 10 * np.abs(np.sin(pygame.time.get_ticks() / 200))  # Sinusoidal movement
    else:
        mouth_width = 100
        mouth_height = 10

    pygame.draw.rect(screen, BLACK, [100, 200, mouth_width, mouth_height])

    # Update the screen
    pygame.display.flip()
    pygame.time.delay(8)

pygame.quit()
