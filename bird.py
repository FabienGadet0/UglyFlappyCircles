from config import *
import pygame
from pygame.locals import *
import random
from keras.models import Sequential
from keras.layers import Dense
from keras import losses
from keras import optimizers
# from keras.layers import Input
# import keras
import numpy as np

class Bird():

    def init_model(self):
        self.model = Sequential()
        self.model.add(Dense(4,  activation='relu', input_dim=1, kernel_initializer='RandomNormal'))
        # self.model.add(Dense(4,  activation='relu', input_dim=1, kernel_initializer='RandomNormal'))
        # self.model.add(Dense(4,  activation='relu', input_dim=1, kernel_initializer='RandomNormal'))
        self.model.add(Dense(1, activation='sigmoid',kernel_initializer='RandomNormal'))
        self.model.compile(loss='categorical_crossentropy',
              optimizer='sgd',
              metrics=['accuracy'])
        self.model.compile(loss=losses.categorical_crossentropy,
              optimizer=optimizers.SGD(lr=0.01, momentum=0.9, nesterov=True))



    def __init__(self, x, y):
        self.x , self.y = int(x) , int(y)
        self.radius = 25
        self.velocity = GRAVITY
        self.jump = 0
        self.jumping = False
        self.collid = Rect(self.x - self.radius, self.y - self.radius, (self.radius / 2), (self.radius / 2))
        self.isDead = False
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.init_model()
        self.fitness = 0

    def brainDEAD(self, a,b,c):
        inputs = np.array([a,b,c, self.velocity])
        r = self.model.predict(inputs)
        if r.mean() <= 0.5:
            self.up()

    def pos(self):
        return (self.x, int(self.y))

    def up(self):
        if not self.jumping:
            self.jumping = True
            self.jump = self.y

    def move_y(self):
        self.y += self.velocity
        self.collid = Rect(self.x , self.y , (self.radius / 1.5), (self.radius / 1.5))

    def collision(self, pipe):
        if self.collid.collidelist(pipe.rect()) != -1:
            self.isDead = True         
            self.color = RED

    def update(self, delta):
        if self.y > SIZE[1] or self.y < 0:
            self.isDead = True
        if not self.isDead:
            if self.jumping:
                self.velocity -= GRAVITY  * delta
            if self.y <= (self.jump - JUMP_HEIGHT):
                self.velocity = GRAVITY
                self.jumping = False
            self.move_y()
