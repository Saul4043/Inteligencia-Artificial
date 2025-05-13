# -*- coding: utf-8 -*-
"""
Created on Sat Apr 20 00:02:05 2024

@author: Admin
"""

import pygame
import random
import sys

# Configuración de la pantalla
WIDTH, HEIGHT = 400, 600
PIPE_WIDTH = 80
PIPE_GAP = 200
FPS = 60

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.4
        self.lift = -10
        self.radius = 20

    def show(self, screen):
        pygame.draw.circle(screen, BLUE, (self.x, int(self.y)), self.radius)

    def update(self):
        self.velocity += self.gravity
        self.velocity *= 0.9 # Añadir resistencia de aire
        self.y += self.velocity

        if self.y > HEIGHT:
            self.y = HEIGHT
            self.velocity = 0
        elif self.y < 0:
            self.y = 0
            self.velocity = 0

    def up(self):
        self.velocity += self.lift

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, HEIGHT - PIPE_GAP - 50)

    def show(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - (self.height + PIPE_GAP)))

    def update(self):
        self.x -= 3

    def offscreen(self):
        return self.x < -PIPE_WIDTH

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("pajarito volador en este caso circulo volador")
    clock = pygame.time.Clock()

    bird = Bird()
    pipes = []
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.up()

        screen.fill(WHITE)

        # Control del pájaro
        bird.update()
        bird.show(screen)

        # Control de los tubos
        if len(pipes) == 0 or pipes[-1].x < WIDTH - 200:
            pipes.append(Pipe(WIDTH))
        for pipe in pipes:
            pipe.show(screen)
            pipe.update()
            if pipe.x + PIPE_WIDTH == bird.x:
                score += 1
            if pipe.offscreen():
                pipes.remove(pipe)
            if pipe.x < bird.x < pipe.x + PIPE_WIDTH and (bird.y < pipe.height or bird.y > pipe.height + PIPE_GAP):
                print("fin del juego")
                running = False

        # Mostrar la puntuación
        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(score), True, BLACK)
        screen.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()  
 