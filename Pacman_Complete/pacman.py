import pygame
from pygame.locals import *
from .vector import Vector2
from .constants import *
from .entity import Entity
from .sprites import PacmanSprites, FruitSprites
from .projectile import Projectile

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node )
        self.name = PACMAN    
        self.color = YELLOW
        self.direction = LEFT
        self.last_valid_direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.sprites = PacmanSprites(self)
        self.fruit_sprites = FruitSprites(self, 0)
        self.fire_cooldown = 0.5 # seconds
        self.last_fire_time = 0
        self.ammo = 20

    def reset(self):
        Entity.reset(self)
        self.direction = LEFT
        self.last_valid_direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True
        self.image = self.sprites.getStartImage()
        self.sprites.reset()

    def die(self):
        self.alive = False
        self.direction = STOP

    def update(self, dt):	
        self.sprites.update(dt)
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        if direction != STOP:
            self.last_valid_direction = direction
        if self.overshotTarget():
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None:
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)

            if self.target is self.node:
                self.direction = STOP
            self.setPosition()
        else: 
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP  

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            if self.collideCheck(pellet):
                return pellet
        return None    
    
    def collideGhost(self, ghost):
        return self.collideCheck(ghost)

    def collideCheck(self, other):
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False

    def fire(self):
        current_time = pygame.time.get_ticks() / 1000.0
        if current_time - self.last_fire_time > self.fire_cooldown and self.ammo > 0:
            self.last_fire_time = current_time
            self.ammo -= 1
            fire_direction = self.direction if self.direction != STOP else self.last_valid_direction
            projectile = Projectile(self.position.x, self.position.y, self.directions[fire_direction])
            projectile.image = self.fruit_sprites.getStartImage(0)
            return projectile
        return None
