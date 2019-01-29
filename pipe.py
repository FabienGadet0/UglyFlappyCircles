from config import *
import pygame
from pygame.locals import *
import random


class Pipe():

    def __init__(self, x):
        self.x = x
        self.height = random.randint(200, 600)
        self.y_bot = self.height + GAP_BETWEEN_PIPES
        self.isdead = False
        self.top_rect = Rect(self.x, 0, 50, self.height)
        self.bot_rect = Rect(self.x, self.y_bot, 50, (SIZE[1] - self.height))

    def update(self):
        self.x -= 2
        self.top_rect = self.top_rect.move(-2, 0)
        self.bot_rect = self.bot_rect.move(-2, 0)
        if self.top_rect.left < SIZE[0] / 6:
            self.isdead = True

    def rect(self):
        return [self.top_rect, self.bot_rect]
