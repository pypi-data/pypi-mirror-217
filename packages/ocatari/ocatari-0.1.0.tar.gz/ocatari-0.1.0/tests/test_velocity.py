from ocatari.core import OCAtari
import pygame
import numpy as np

# import faulthandler


# faulthandler.enable()

env_name = "ALE/Seaquest-v5"

env = OCAtari(env_name, mode='revised', hud=False, render_mode="rgb_array", frameskip=1)
env.reset()

transition = 0
episode = 0

# Initialize GUI
frame = env.render()
screen = pygame.display.set_mode((frame.shape[1], frame.shape[0]), flags=pygame.SCALED)
pygame.init()


def render():
    # Get RGB image from env
    rgb_array = env.render()

    # Render RGB image
    rgb_array = np.transpose(rgb_array, (1, 0, 2))
    pygame.pixelcopy.array_to_surface(screen, rgb_array)

    # Render object coordinates and velocity vectors
    for obj in env.objects:
        x = obj.x + obj.w / 2
        y = obj.y + obj.h / 2
        dx = obj.dx
        dy = obj.dy

        # Draw an 'X' at object center
        pygame.draw.line(screen, color=(255, 255, 255),
                         start_pos=(x - 2, y - 2), end_pos=(x + 2, y + 2))
        pygame.draw.line(screen, color=(255, 255, 255),
                         start_pos=(x - 2, y + 2), end_pos=(x + 2, y - 2))

        # Draw velocity vector
        if dx != 0 or dy != 0:
            pygame.draw.line(screen, color=(100, 200, 255),
                             start_pos=(float(x), float(y)), end_pos=(x + 8 * dx, y + 8 * dy))

    pygame.display.flip()
    pygame.event.pump()


render()
clock = pygame.time.Clock()

print("Playing...")

# Iterate over episodes
while True:
    done = False

    # Iterate over transitions
    while not done:
        # Choose action
        action = np.random.choice(env.action_space.n)

        # Perform transition
        _, _, done, _, _ = env.step(action)

        # Render environment for human
        clock.tick(60)  # reduce FPS
        render()
