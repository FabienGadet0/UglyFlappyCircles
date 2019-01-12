# Import a library of functions called 'pygame'
import pygame
from pygame.locals import *
from math import pi
import random
from config import *
from pipe import *
from bird import *


def add_pipes(pipes):
    pipe_x = 150
    if (len(pipes) > 1):
        pipe_x = pipes[-1].x
    while pipe_x < SIZE[0] + 200:
        pipe_x += DISTANCE_BT_PIPES
        pipes.append(Pipe(pipe_x))

def main():

    # Initialize the game engine
    pygame.init()
    pause = False
   
    screen = pygame.display.set_mode(SIZE)
    
    pygame.display.set_caption("Flapp tamere")
    
    #Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()
    birds = list()
    bird = Bird(SIZE[0] / 6, SIZE[1] / 1.5)
    pipes = list()
    add_pipes(pipes)
    for i in range(NB_BIRDS):
        birds.append(Bird(SIZE[0] / 6, SIZE[1] / random.uniform(1, 2)))
    while not done:
        delta = clock.tick(FPS)
        delta /= 50
   
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done=True # Flag that we are done so we exit this loop
            if event.type == pygame.KEYUP:
                for bird in birds:
                    bird.up()


        for idx, bird in enumerate(birds):
            bird.update(delta)
            if bird.isDead:
                del birds[idx]
     

        for idx, pipe in enumerate(pipes):
            pipe.update()
            if pipe.isdead:
                del pipes[idx]
                add_pipes(pipes)
            for bird in birds:
               bird.collision(pipe)
        screen.fill(BLACK)

 
        for bird in birds:
            pygame.draw.circle(screen, bird.color, bird.pos(), bird.radius)
            # pygame.draw.rect(screen, bird.color, bird.collid)
        for pipe in pipes:
            for single_pipe in pipe.rect():
                pygame.draw.rect(screen, WHITE, single_pipe)
        # Go ahead and update the screen with what we've drawn.
        # This MUST happen after all the other drawing commands.
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()