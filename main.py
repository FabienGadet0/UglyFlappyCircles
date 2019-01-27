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
    birds = []
    deadBirds_filtered = list(filter(lambda x: x.fitness != 0, deadBirds))
    print(len(deadBirds))
    if len(deadBirds_filtered) != 0:
        deadBirds = deadBirds_filtered
        deadBirds.sort(key=lambda x: x.fitness, reverse=True)
        for idx, deadBird in enumerate(deadBirds):
            if idx < int(0.2 * len(deadBirds)):
                print('cp')
                birds.append(deadBird)
            elif idx < int(0.5 * len(deadBirds)):
                birds.append(deadBird.mutate())
            else:
                birds.append(deadBird.reset())
    else:
        print('reset_ALL')
        for deadBird in deadBirds:
            birds.append(deadBird.reset())
    del deadBirds[:]
    return birds


def loop(pipes, birds, screen):

    done = False
    myfont = pygame.font.SysFont("comicsansms", 25)
    every_sec = 0
    score = 0
    generation = 0
    display = 0
    clock = pygame.time.Clock()
    deadBirds = []

    while not done:

        delta = clock.tick(FPS)
        display += delta
        every_sec += delta
        delta /= 50

        if(len(birds) == 0):
            score = 0
            if pipes[0].x < 200:
                pipes.pop(0)
                add_pipes(pipes)
            birds = reset(deadBirds)
            generation += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        if every_sec >= 400:
            for bird in birds:
                bird.brainDEAD(pipes[0].height,
                               pipes[0].bot_rect.top, pipes[0].x)
                every_sec = 0
        for idx, bird in enumerate(birds):
            bird.update(delta)
            if bird.isDead:
                bird.fitness = score
                deadBirds.append(birds.pop(idx))

        for idx, pipe in enumerate(pipes):
            pipe.update()
            for bird in birds:
                bird.collision(pipe)
            if pipe.isdead:
                del pipes[idx]
                add_pipes(pipes)
                score += 1
        screen.fill(BLACK)

        for bird in birds:
            if not bird.isDead:
                pygame.draw.circle(screen, bird.color, bird.pos(), bird.radius)

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
    for i in range(NB_BIRDS):
        birds.append(Bird())
    return pipes, birds


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Ugly Flappy Circle")
    pipes, birds = init_all()
    loop(pipes, birds, screen)
    pygame.quit()


if __name__ == "__main__":
    main()
