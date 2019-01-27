import pprint
import random
from math import pi

import pygame
from pygame.locals import *

from bird import *
from config import *
from pipe import *


def add_pipes(pipes):
    pipe_x = 150
    p = []
    if (len(pipes) > 1):
        pipe_x = pipes[-1].x
    while pipe_x < SIZE[0] + 200:
        pipe_x += DISTANCE_BT_PIPES
        pipes.append(Pipe(pipe_x))


def reset(deadBirds):
    print('before :', len(deadBirds))
    deadBirds.sort(key=lambda x: x.fitness, reverse=True)
    deadBirds_filtered = list(filter(lambda x: x.fitness != 0, deadBirds))
    if len(deadBirds_filtered) != 0:
        totalDead = len(deadBirds)
        for idx, deadBird in enumerate(deadBirds_filtered):
            if idx < int(0.5 * totalDead) and idx > int(0.2 * totalDead):
                deadBird.mutate()
            else:
                deadBird.reset()
            deadBird.revive()
    else:
        for deadBird in deadBirds:
            deadBird.reset()


def loop(pipes, birds, screen):

    done = False
    myfont = pygame.font.SysFont("comicsansms", 25)
    every = 0
    dead_number = 0
    score = 0
    generation = 0
    display = 0
    clock = pygame.time.Clock()
    deadBirds = []

    while not done:

        delta = clock.tick(FPS)
        display += delta
        every += delta
        delta /= 50

        if(dead_number == NB_BIRDS):
            print(dead_number)
            score = 0
            if pipes[0].x < 200:
                pipes.pop(0)
                add_pipes(pipes)
            reset(birds)
            generation += 1
            dead_number = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.K_SPACE:
                del birds[:]
        if every >= 400:
            for bird in birds:
                bird.brainDEAD(pipes[0].height,
                               pipes[0].bot_rect.top, pipes[0].x)
                every = 0
        for bird in birds:
            if bird.update(delta):
                bird.fitness = score
                dead_number += 1

        for idx, pipe in enumerate(pipes):
            pipe.update()
            if pipe.isdead:
                del pipes[idx]
                add_pipes(pipes)
                score += 1
            for bird in birds:
                if bird.collision(pipe):
                    bird.fitness = score
                    dead_number += 1
                    bird.die()

        screen.fill(BLACK)

        for bird in birds:
            bird.draw(screen)

        for pipe in pipes:
            for single_pipe in pipe.rect():
                pygame.draw.rect(screen, WHITE, single_pipe)

        label = myfont.render(
            "Generation :" + str(generation), 1, (255, 255, 0))
        label2 = myfont.render(
            "Current score: " + str(score), 1, (255, 255, 0))
        screen.blit(label, ((SIZE[0] / 2.5), 5))
        screen.blit(label2, ((SIZE[0] / 2.5), 35))
        pygame.display.flip()


def init_all():
    pipes = []
    birds = []
    add_pipes(pipes)
    birds = [Bird() for x in range(NB_BIRDS)]
    return pipes, birds


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Ugly Flappy Circles")
    pipes, birds = init_all()
    loop(pipes, birds, screen)
    pygame.quit()


if __name__ == "__main__":
    main()
