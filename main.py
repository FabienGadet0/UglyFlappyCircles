import pprint
import random
from math import pi

import pygame
import math
from pygame.locals import *

from bird import *
from config import *
from pipe import *


def add_pipes(pipes):
    pipe_x = 150
    if (len(pipes) > 1):
        pipe_x = pipes[-1].x
    while pipe_x < SIZE[0] + 200:
        pipe_x += DISTANCE_BT_PIPES
        pipes.append(Pipe(pipe_x))


def reset(deadBirds):
    idx = 0
    deadBirds.sort(key=lambda x: x.fitness, reverse=True)
    deadBirds_filtered = list(filter(lambda x: x.fitness != 0, deadBirds))
    if len(deadBirds_filtered) != 0:
        for deadBird in deadBirds_filtered:
            if idx < math.ceil(int(0.2 * len(deadBirds_filtered))):
                deadBird.keep_this_bird_HEISVERYINTELLIGENT()
            elif idx < math.ceil(int(0.5 * len(deadBirds_filtered))):
                deadBird.mutate()
            else:
                deadBird.reset()
            deadBird.revive()
            idx += 1
    while idx != len(deadBirds):
        if deadBirds[idx].inherit > 0:
            deadBirds[idx].mutate()
        else:
            deadBirds[idx].reset()
        deadBirds[idx].revive()
        idx += 1


def loop(pipes, birds, screen):

    done = False
    best_score = 0
    myfont = pygame.font.SysFont("comicsansms", 25)
    every = 0
    dead_number = 0
    score = 0
    generation = 0
    display = 0
    clock = pygame.time.Clock()

    while not done:

        delta = clock.tick(FPS)
        display += delta
        every += delta
        delta /= 50

        if(dead_number >= NB_BIRDS):
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
            if bird.update(delta, pipes[0]):
                bird.fitness = score
                dead_number += 1

        for idx, pipe in enumerate(pipes):
            pipe.update()
            if pipe.isdead:
                del pipes[idx]
                add_pipes(pipes)
                score += 1

        screen.fill(BLACK)

        for bird in birds:
            bird.draw(screen)

        for pipe in pipes:
            for single_pipe in pipe.rect():
                pygame.draw.rect(screen, WHITE, single_pipe)

        best_score = (best_score, score)[score > best_score]

        label = myfont.render(
            "Generation :" + str(generation), 1, (255, 255, 0))
        label2 = myfont.render(
            "Current score: " + str(score), 1, (255, 255, 0))
        label3 = myfont.render(
            "Best score: " + str(best_score), 1, (255, 255, 0))
        label4 = myfont.render(
            "WE FOUND A GENIUS", 1, (0, 255, 0))
        screen.blit(label, ((SIZE[0] / 2.5), 5))
        screen.blit(label2, ((SIZE[0] / 2.5), 35))
        screen.blit(label3, ((SIZE[0] / 2.5), 65))
        if score > 20:
            screen.blit(label4, ((SIZE[0] / 2) - 200, SIZE[1] / 2 - 100))
        pygame.display.flip()


def init_all():
    pipes = []
    add_pipes(pipes)
    return pipes, [Bird() for x in range(NB_BIRDS)]


def main():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Ugly Flappy Circles")
    pipes, birds = init_all()
    loop(pipes, birds, screen)
    pygame.quit()


if __name__ == "__main__":
    main()
