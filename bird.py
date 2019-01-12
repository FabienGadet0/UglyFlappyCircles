from config import *
import pygame
from pygame.locals import *
import random
class Bird():

    def __init__(self, x, y):
        self.x , self.y = int(x) , int(y)
        self.radius = 25
        self.velocity = GRAVITY
        self.jump = 0
        self.jumping = False
        self.collid = Rect(self.x - self.radius, self.y - self.radius, self.radius / 0.5 , self.radius / 0.5)
        self.isDead = False
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def pos(self):
        return (self.x, int(self.y))

    def up(self):
        if not self.jumping:
            self.jumping = True
            self.jump = self.y

    def move_y(self):
        self.y += self.velocity
        self.collid = Rect(self.x - self.radius, self.y - self.radius, self.radius / 0.5 , self.radius / 0.5)

    def collision(self, pipe):
        if self.collid.collidelist(pipe.rect()) != -1:
            self.isDead = True         
            self.color = RED

    def update(self, delta):
        if self.y > SIZE[1] or self.y < 0:
            self.isDead = True
        if self.jumping:
            self.velocity -= GRAVITY  * delta
        if self.y <= (self.jump - JUMP_HEIGHT):
            self.velocity = GRAVITY
            self.jumping = False
        self.move_y()
