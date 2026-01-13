import os
from Pacman_Complete.run import GameController

if __name__ == "__main__":
    # Change the working directory to the Pacman_Complete directory
    os.chdir(os.path.join(os.path.dirname(__file__), 'Pacman_Complete'))
    game = GameController()
    while True:
        game.update()