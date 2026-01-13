import pygame
import random
from pygame.locals import *
from .constants import *
from .pacman import Pacman
from .nodes import NodeGroup
from .pellets import PelletGroup
from .ghosts import GhostGroup
from .fruit import Fruit
from .pauser import Pause
from .text import TextGroup
from .sprites import LifeSprites
from .sprites import MazeSprites
from .mazedata import MazeData
from .projectile import Projectile

class GameController(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32)
        self.eat_ghost_sound = pygame.mixer.Sound("pacman_eatghost.wav")
        self.ghost_died_sound = pygame.mixer.Sound("ghost_died.mp3")
        self.pacman_beginning_sound = pygame.mixer.Sound("pacman_beginning.wav")
        self.pacman_beginning_sound.play()
        self.background = None
        self.background_norm = None
        self.background_flash = None
        self.clock = pygame.time.Clock()
        self.fruits = []
        self.max_fruits = 3
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textgroup = TextGroup()
        self.lifesprites = LifeSprites(self.lives)
        self.flashBG = False
        self.flashTime = 0.2
        self.flashTimer = 0
        self.fruitCaptured = []
        self.fruitNode = None
        self.mazedata = MazeData()
        self.projectiles = []
        self.state = MAIN_MENU
        self.main_menu_textgroup = TextGroup(setup=False)
        self.controls_menu_textgroup = TextGroup(setup=False)
        self.setupMainMenu()
        self.setupControlsMenu()
        self.fruit_timer = 0
        self.fruit_spawn_time = 7.5
        self.ai_level = MEDIUM # Default AI level

    def setupMainMenu(self):
        self.main_menu_textgroup.addText("PACMAN", YELLOW, int(SCREENWIDTH/2 - 100), int(SCREENHEIGHT/2 - 100), 32)
        self.main_menu_textgroup.addText("Start Game (S)", WHITE, int(SCREENWIDTH/2 - 150), int(SCREENHEIGHT/2), 16)
        self.main_menu_textgroup.addText("Controls (M)", WHITE, int(SCREENWIDTH/2 - 150), int(SCREENHEIGHT/2) + 50, 16)
        self.main_menu_textgroup.addText("Easy (E)", WHITE, int(SCREENWIDTH/2 - 150), int(SCREENHEIGHT/2) + 100, 16)
        self.main_menu_textgroup.addText("Medium (D)", WHITE, int(SCREENWIDTH/2 - 150), int(SCREENHEIGHT/2) + 150, 16)
        self.main_menu_textgroup.addText("Hard (H)", WHITE, int(SCREENWIDTH/2 - 150), int(SCREENHEIGHT/2) + 200, 16)

    def setupControlsMenu(self):
        self.controls_menu_textgroup.addText("Controls", YELLOW, int(SCREENWIDTH/2 - 100), int(SCREENHEIGHT/2 - 100), 32)
        self.controls_menu_textgroup.addText("Arrow Keys - Move", WHITE, int(SCREENWIDTH/2 - 150), int(SCREENHEIGHT/2), 16)
        self.controls_menu_textgroup.addText("F - Fire", WHITE, int(SCREENWIDTH/2 - 150), int(SCREENHEIGHT/2) + 50, 16)
        self.controls_menu_textgroup.addText("Space - Pause", WHITE, int(SCREENWIDTH/2 - 150), int(SCREENHEIGHT/2) + 100, 16)
        self.controls_menu_textgroup.addText("Press ESC to go back", WHITE, int(SCREENWIDTH/2 - 150), int(SCREENHEIGHT/2) + 150, 16)

    def setBackground(self):
        self.background_norm = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_norm.fill(BLACK)
        self.background_flash = pygame.surface.Surface(SCREENSIZE).convert()
        self.background_flash.fill(BLACK)
        self.background_norm = self.mazesprites.constructBackground(self.background_norm, self.level%5)
        if self.level == 2:
            self.background_norm = self.mazesprites.constructBackground(self.background_norm, 1) # Use y=1 for Level 3 color
        self.background_flash = self.mazesprites.constructBackground(self.background_flash, 5)
        self.flashBG = False
        self.background = self.background_norm

    def startGame(self):      
        self.mazedata.loadMaze(self.level)
        self.mazesprites = MazeSprites(self.mazedata.obj.name+".txt", self.mazedata.obj.name+"_rotation.txt")
        self.setBackground()
        self.nodes = NodeGroup(self.mazedata.obj.name+".txt")
        self.mazedata.obj.setPortalPairs(self.nodes)
        self.mazedata.obj.connectHomeNodes(self.nodes)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(*self.mazedata.obj.pacmanStart))
        self.pellets = PelletGroup(self.mazedata.obj.name+".txt")
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman, self.ai_level)

        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(0, 3)))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(4, 3)))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 3)))
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles(*self.mazedata.obj.addOffset(2, 0)))

        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.mazedata.obj.denyGhostsAccess(self.ghosts, self.nodes)

    def update(self):
        if self.state == MAIN_MENU:
            self.main_menu_update()
        elif self.state == CONTROLS_MENU:
            self.controls_menu_update()
        elif self.state == PLAY:
            self.play_update()

    def main_menu_update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_s:
                    self.state = PLAY
                    self.startGame()
                elif event.key == K_m:
                    self.state = CONTROLS_MENU
                elif event.key == K_e:
                    self.ai_level = EASY
                    print(f"AI Level set to Easy: {self.ai_level}")
                    self.state = PLAY
                    self.startGame()
                elif event.key == K_d:
                    self.ai_level = MEDIUM
                    print(f"AI Level set to Medium: {self.ai_level}")
                    self.state = PLAY
                    self.startGame()
                elif event.key == K_h:
                    self.ai_level = HARD
                    print(f"AI Level set to Hard: {self.ai_level}")
                    self.state = PLAY
                    self.startGame()
        self.render()

    def controls_menu_update(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state = MAIN_MENU
        self.render()

    def play_update(self):
        dt = self.clock.tick(30) / 1000.0
        self.textgroup.update(dt)
        self.textgroup.updateAmmo(self.pacman.ammo)
        self.pellets.update(dt)
        self.fruit_timer += dt
        if self.fruit_timer >= self.fruit_spawn_time:
            if len(self.fruits) < self.max_fruits:
                node = self.nodes.getRandomNode()
                self.fruits.append(Fruit(node, self.level))
            self.fruit_timer = 0
        if not self.pause.paused:
            self.ghosts.update(dt)      
            for fruit in self.fruits:
                fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()
            self.checkProjectileEvents()

        for projectile in self.projectiles:
            projectile.update(dt)

        if self.pacman.alive:
            if not self.pause.paused:
                self.pacman.update(dt)
        else:
            self.pacman.update(dt)

        if self.flashBG:
            self.flashTimer += dt
            if self.flashTimer >= self.flashTime:
                self.flashTimer = 0
                if self.background == self.background_norm:
                    self.background = self.background_flash
                else:
                    self.background = self.background_norm

        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def render(self):
        if self.state == MAIN_MENU:
            self.main_menu_render()
        elif self.state == CONTROLS_MENU:
            self.controls_menu_render()
        elif self.state == PLAY:
            self.play_render()

    def main_menu_render(self):
        self.screen.fill(BLACK)
        self.main_menu_textgroup.render(self.screen)
        pygame.display.update()

    def controls_menu_render(self):
        self.screen.fill(BLACK)
        self.controls_menu_textgroup.render(self.screen)
        pygame.display.update()

    def play_render(self):
        self.screen.blit(self.background, (0, 0))
        self.pellets.render(self.screen)
        for fruit in self.fruits:
            fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        for projectile in self.projectiles:
            projectile.render(self.screen)
        self.textgroup.render(self.screen)

        for i in range(len(self.lifesprites.images)):
            x = self.lifesprites.images[i].get_width() * i
            y = SCREENHEIGHT - self.lifesprites.images[i].get_height()
            self.screen.blit(self.lifesprites.images[i], (x, y))

        for i in range(len(self.fruitCaptured)):
            x = SCREENWIDTH - self.fruitCaptured[i].get_width() * (i+1)
            y = SCREENHEIGHT - self.fruitCaptured[i].get_height()
            self.screen.blit(self.fruitCaptured[i], (x, y))

        pygame.display.update()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive:
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            self.textgroup.showText(PAUSETXT)
                elif event.key == K_g:
                    self.level = 2
                    self.nextLevel()
                elif event.key == K_f:
                    projectile = self.pacman.fire()
                    if projectile:
                        self.projectiles.append(projectile)
                        self.textgroup.updateAmmo(self.pacman.ammo)
                        print(f"Projectile added. Total projectiles: {len(self.projectiles)}")

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if pellet:
            self.pellets.numEaten += 1
            self.eat_ghost_sound.play()
            self.updateScore(pellet.points)
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.startFreight()
            if self.pellets.isEmpty():
                self.flashBG = True
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)

    def checkGhostEvents(self):
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.updateScore(ghost.points)                  
                    self.eat_ghost_sound.play()
                    self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pause.setPause(pauseTime=1, func=self.showEntities)
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost)
                elif ghost.mode.current is not SPAWN:
                    if self.pacman.alive:
                        self.lives -=  1
                        self.lifesprites.removeImage()
                        self.pacman.die()               
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.textgroup.showText(GAMEOVERTXT)
                            self.pause.setPause(pauseTime=3, func=self.restartGame)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)
    
    def checkFruitEvents(self):
        for fruit in self.fruits:
            if self.pacman.collideCheck(fruit):
                self.updateScore(fruit.points)
                self.pacman.ammo = 20
                self.textgroup.updateAmmo(self.pacman.ammo)
                self.textgroup.addText(str(fruit.points), WHITE, fruit.position.x, fruit.position.y, 8, time=1)
                fruitCaptured = False
                for f in self.fruitCaptured:
                    if f.get_offset() == fruit.image.get_offset():
                        fruitCaptured = True
                        break
                if not fruitCaptured:
                    self.fruitCaptured.append(fruit.image)
                self.fruits.remove(fruit)
            elif fruit.destroy:
                self.fruits.remove(fruit)

    def checkProjectileEvents(self):
        for projectile in self.projectiles:
            for ghost in self.ghosts:
                if ghost.mode.current is not SPAWN:
                    d = projectile.position - ghost.position
                    dSquared = d.magnitudeSquared()
                    rSquared = (projectile.radius + ghost.collideRadius)**2
                    if dSquared <= rSquared:
                        self.updateScore(ghost.points)
                        self.ghost_died_sound.play()
                        ghost.die()
                        self.projectiles.remove(projectile)
                        break

    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideEntities(self):
        self.pacman.visible = False
        self.ghosts.hide()

    def nextLevel(self):
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)

    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruits = []
        self.startGame()
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)
        self.lifesprites.resetLives(self.lives)
        self.fruitCaptured = []

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset()
        self.ghosts.reset()
        self.fruits = []
        self.textgroup.showText(READYTXT)

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)


if __name__ == "__main__":
    game = GameController()
    while True:
        game.update()
