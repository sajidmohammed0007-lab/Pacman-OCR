from .constants import *

class MainMode(object):
    def __init__(self, ai_level=MEDIUM):
        self.ai_level = ai_level
        self.timer = 0
        self.scatter()

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()

    def scatter(self):
        self.mode = SCATTER
        if self.ai_level == EASY:
            self.time = 10
        elif self.ai_level == HARD:
            self.time = 5
        else: # MEDIUM or default
            self.time = 7
        self.timer = 0

    def chase(self):
        self.mode = CHASE
        if self.ai_level == EASY:
            self.time = 15
        elif self.ai_level == HARD:
            self.time = 25
        else: # MEDIUM or default
            self.time = 20
        self.timer = 0


class ModeController(object):
    def __init__(self, entity, ai_level=MEDIUM):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode(ai_level)
        self.current = self.mainmode.mode
        self.entity = entity 
        self.ai_level = ai_level 

    def update(self, dt):
        self.mainmode.update(dt)
        if self.current is FREIGHT:
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                self.entity.normalMode()
                self.current = self.mainmode.mode
        elif self.current in [SCATTER, CHASE]:
            self.current = self.mainmode.mode

        if self.current is SPAWN:
            if (self.entity.position - self.entity.spawnNode.position).magnitude() < 1:
                self.entity.normalMode()
                self.current = self.mainmode.mode

    def setFreightMode(self):
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            if self.ai_level == EASY:
                self.time = 10
            elif self.ai_level == HARD:
                self.time = 5
            else: # MEDIUM or default
                self.time = 7
            self.current = FREIGHT
        elif self.current is FREIGHT:
            self.timer = 0

    def setSpawnMode(self):
        if self.current in [FREIGHT, CHASE, SCATTER]:
            self.current = SPAWN