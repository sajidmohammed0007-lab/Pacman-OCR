import pygame
from .vector import Vector2
from .constants import *
from .sprites import FruitSprites

class Projectile(object):
    def __init__(self, x, y, direction):
        self.position = Vector2(x, y)
        self.direction = direction
        self.speed = 200
        self.radius = 8
        self.color = (255, 0, 0) # Red
        self.fruit_sprites = FruitSprites(self, 0)
        self.image = self.fruit_sprites.getStartImage(0)


    def update(self, dt):
        self.position += self.direction * self.speed * dt

    def render(self, screen):
        pos = self.position.asInt()
        screen.blit(self.image, (pos[0] - TILEWIDTH / 2, pos[1] - TILEHEIGHT / 2))
