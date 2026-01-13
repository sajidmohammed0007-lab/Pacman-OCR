import pygame
from pygame.locals import *
from .vector import Vector2
from .constants import *
from .entity import Entity
from .modes import ModeController
from .sprites import GhostSprites

class Ghost(Entity):
    def __init__(self, node, pacman=None, blinky=None, ai_level=MEDIUM):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node
        self.ai_level = ai_level

        if self.ai_level == EASY:
            self.speed_multiplier = 0.8
        elif self.ai_level == HARD:
            self.speed_multiplier = 1.2
        else: # MEDIUM or default
            self.speed_multiplier = 1.0

    def reset(self):
        Entity.reset(self)
        self.points = 200
        self.directionMethod = self.goalDirection

    def update(self, dt):
        self.sprites.update(dt)
        self.mode.update(dt)
        if self.mode.current is SCATTER:
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt)

    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position

    def spawn(self):
        self.goal = self.spawnNode.position

    def setSpawnNode(self, node):
        self.spawnNode = node

    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.setSpeed(150 * self.speed_multiplier)
            self.directionMethod = self.goalDirection
            self.spawn()

    def startFreight(self):
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT:
            self.setSpeed(50 * self.speed_multiplier)
            self.directionMethod = self.randomDirection         

    def normalMode(self):
        self.setSpeed(100 * self.speed_multiplier)
        self.directionMethod = self.goalDirection
        self.homeNode.denyAccess(DOWN, self)

    def die(self):
        self.startSpawn()




class Blinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None, ai_level=MEDIUM):
        Ghost.__init__(self, node, pacman, blinky, ai_level)
        self.name = BLINKY
        self.color = RED
        self.sprites = GhostSprites(self)


class Pinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None, ai_level=MEDIUM):
        Ghost.__init__(self, node, pacman, blinky, ai_level)
        self.name = PINKY
        self.color = PINK
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, 0)

    def chase(self):
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


class Inky(Ghost):
    def __init__(self, node, pacman=None, blinky=None, ai_level=MEDIUM):
        Ghost.__init__(self, node, pacman, blinky, ai_level)
        self.name = INKY
        self.color = TEAL
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)

    def chase(self):
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2


class Clyde(Ghost):
    def __init__(self, node, pacman=None, blinky=None, ai_level=MEDIUM):
        Ghost.__init__(self, node, pacman, blinky, ai_level)
        self.name = CLYDE
        self.color = ORANGE
        self.sprites = GhostSprites(self)

    def scatter(self):
        self.goal = Vector2(0, TILEHEIGHT*NROWS)

    def chase(self):
        d = self.pacman.position - self.position
        ds = d.magnitudeSquared()
        if ds <= (TILEWIDTH * 8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4


class GhostGroup(object):
    def __init__(self, node, pacman, ai_level=MEDIUM):
        self.blinky = Blinky(node, pacman, blinky=None, ai_level=ai_level)
        self.pinky = Pinky(node, pacman, blinky=None, ai_level=ai_level)
        self.inky = Inky(node, pacman, blinky=self.blinky, ai_level=ai_level)
        self.clyde = Clyde(node, pacman, blinky=None, ai_level=ai_level)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]

    def __iter__(self):
        return iter(self.ghosts)

    def update(self, dt):
        for ghost in self:
            ghost.update(dt)

    def startFreight(self):
        for ghost in self:
            ghost.startFreight()
        self.resetPoints()

    def setSpawnNode(self, node):
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        for ghost in self:
            ghost.points = 200

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def show(self):
        for ghost in self:
            ghost.visible = True

    def reset(self):
        for ghost in self:
            ghost.reset()

    def render(self, screen):
        for ghost in self:
            ghost.render(screen)

