# Import a library of functions called 'pygame'
import pygame
from pygame.locals import *
from math import pi
import random
from config import *
from pipe import *
from bird import *
import pprint

def add_pipes(pipes):
    pipe_x = 150
    p = []
    if (len(pipes) > 1):
        pipe_x = pipes[-1].x
    while pipe_x < SIZE[0] + 200:
        pipe_x += DISTANCE_BT_PIPES
        pipes.append(Pipe(pipe_x))
  

def add_birds():
    b = []
    for i in range(NB_BIRDS):
        b.append(Bird(SIZE[0] / 6, SIZE[1] / random.uniform(1, 2)))
    return b

def reset(deadBirds):
    birds = []
    birds = add_birds()
    deadBirds = list(filter(lambda x: x.fitness != 0, deadBirds))
    if len(deadBirds) == 0:
        print('all dumb')
    if len(deadBirds) != 0:
        deadBirds.sort(key=lambda x: x.fitness, reverse=True)
        for idx, deadBird in enumerate(deadBirds):
            birds[idx].model.set_weights(deadBird.model.get_weights())
    return birds

def loop(pipes, birds, screen):
    done = False
    every_sec = 0
    score = 0
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
            birds = reset(deadBirds)
            # birds = add_birds()
            # pipes, birds = init_all()
   
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
              


        for idx, bird in enumerate(birds):
            if (every_sec >= 150):
                bird.brainDEAD(pipes[0].height, pipes[0].bot_rect.top, pipes[0].x)
                every_sec = 0
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

        if display == 1000:
            for bird in birds:
                if not bird.isDead:
                    pygame.draw.circle(screen, bird.color, bird.pos(), bird.radius)
                    # pygame.draw.rect(screen, bird.color, bird.collid)
            for pipe in pipes:
                for single_pipe in pipe.rect():
                    pygame.draw.rect(screen, WHITE, single_pipe)

            pygame.display.flip()
            display = 0

def init_all():
    pipes = []
    birds = []
    add_pipes(pipes)
    birds = add_birds()
    return pipes, birds

def main():

    # Initialize the game engine
    pygame.init()

    
    screen = pygame.display.set_mode(SIZE)
    
    pygame.display.set_caption("Flapp tamere")
    #Loop until the user clicks the close button.
    
    
    pipes, birds = init_all()
    
    loop(pipes, birds, screen)
    

    pygame.quit()


if __name__ == "__main__":
    main()