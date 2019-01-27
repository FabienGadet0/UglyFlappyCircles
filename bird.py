import random
from pygame.locals import *
import pygame
from config import *
from keras.models import Sequential
from keras.layers import Dense, Reshape
from keras import losses
from keras import optimizers
import numpy as np


class Brain():
    def __init__(self):
        num_inputs = 5
        hidden_nodes = 4
        num_outputs = 1

        self.model = Sequential()
        self.model.add(
            Dense(hidden_nodes, activation='relu', kernel_initializer='RandomNormal', input_dim=num_inputs))
        self.model.add(
            Dense(num_outputs,  activation='sigmoid'))
        self.model.compile(loss='mse', optimizer='adam')

    def compute(self, *args):
        inputs = np.array([args])
        r = self.model.predict(inputs)
        return r

    def cp(self, brain):
        self.model.set_weights(brain.get_weights())
        print('cp')

    def reset(self):
        self.__init__()

    def mutate(self):

        for i in range(len(self.model.layers)):
            weights = self.model.layers[i].get_weights()
            for j in range(len(weights[0])):
                for k in range(len(weights[0][j])):
                    if np.random.random() < MUTATION_RATE:
                        weights[0][j][k] += np.random.normal(
                            scale=MUTATION_SCALE) * 0.5

            self.model.layers[i].set_weights(weights)
        print('mutate')


class Bird():

    def init_params(self):
        self.radius = 25
        self.x, self.y = int(SIZE[0] / 6), int(SIZE[1] / random.uniform(1, 2))
        self.velocity = GRAVITY
        self.jump = 0
        self.jumping = False
        self.collid = Rect(self.x - self.radius, self.y -
                           self.radius, (self.radius / 2), (self.radius / 2))
        self.isDead = False

        self.color = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        self.fitness = 0

    def __init__(self):
        self.brain = Brain()
        self.init_params()

    def brainDEAD(self, a, b, c):
        if not self.isDead:
            r = self.brain.compute(a, b, c, self.y, (self.jumping == True))
            if r <= 0.5:
                self.up()

    def reset(self):
        self.brain.reset()
        self.init_params()

    def mutate(self):
        self.brain.mutate()
        self.fitness = 0

    def cp_birds_VERYINTELLIGENTBRAIN(self, b):
        self.brain.cp(b.brain.model)
        self.fitness = 0

    def pos(self):
        return (self.x, int(self.y))

    def die(self):
        self.isDead = True

    def revive(self):
        self.isDead = False

    def up(self):
        if not self.jumping:
            self.jumping = True
            self.jump = self.y

    def move_y(self):
        self.y += self.velocity
        self.collid = Rect(
            self.x, self.y, (self.radius / 1.5), (self.radius / 1.5))

    def collision(self, pipe):
        return self.collid.collidelist(pipe.rect()) != -1

    def update(self, delta):
        if not self.isDead:
            if self.y > SIZE[1] or self.y < 0:
                self.die()
                print('died')
            if self.jumping:
                self.velocity -= GRAVITY * delta
            if self.y <= (self.jump - JUMP_HEIGHT):
                self.velocity = GRAVITY
                self.jumping = False
            self.move_y()
        return self.isDead

    def draw(self, screen):
        if not self.isDead:
            pygame.draw.circle(screen, self.color, self.pos(), self.radius)
