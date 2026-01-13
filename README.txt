# Pacman in Pygame

This project is a comprehensive implementation of the classic arcade game Pacman, developed using the Pygame library in Python. It aims to recreate the original game's mechanics, including ghost AI, level progression, and scoring.

## Features

*   **Classic Pacman Gameplay:** Navigate the maze, eat pellets, and avoid the ghosts.
*   **Four Unique Ghosts:** Each ghost (Blinky, Pinky, Inky, and Clyde) has its own distinct AI and targeting scheme.
*   **Ghost AI Modes:** Ghosts switch between three modes:
    *   **Chase:** Actively hunt Pacman.
    *   **Scatter:** Retreat to their respective corners.
    *   **Freight:** Become vulnerable after Pacman eats a power pellet.
*   **Power Pellets:** Turn the tables on the ghosts and eat them for extra points.
*   **Fruit Spawns:** Bonus fruit appears twice per level, providing extra points.
*   **Multiple Levels:** The game includes multiple maze layouts that change as you progress through levels.
*   **Scoring System:** Score points for eating pellets, ghosts, and fruit.
*   **Lives System:** Start with a set number of lives, and lose a life when caught by a ghost.
*   **Animated Sprites:** Smooth animations for Pacman and the ghosts, based on a spritesheet.
*   **Sound Effects:** (Not implemented in the provided code, but the structure allows for it).

## How to Play

### Prerequisites

*   Python 3.x
*   Pygame library

### Running the Game

1.  **Install Pygame:**
    ```bash
    pip install pygame
    ```
2.  **Run the game:**
    ```bash
    python Pacman_Complete/run.py
    ```

### Controls

*   **Arrow Keys:** Move Pacman (Up, Down, Left, Right).
*   **Spacebar:** Pause and unpause the game.

## Project Structure

The project is organized into several Python modules, each responsible for a specific part of the game.

| File                 | Description                                                                                                                              |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `run.py`             | The main entry point of the game. Contains the `GameController` class which manages the main game loop, game states, and events.          |
| `constants.py`       | Defines all the global constants used throughout the project, such as colors, screen dimensions, and game states.                        |
| `vector.py`          | A simple 2D vector class used for position, velocity, and other geometric calculations.                                                  |
| `entity.py`          | Contains the base `Entity` class for all moving objects in the game (Pacman and Ghosts). It handles movement, direction, and collision.     |
| `pacman.py`          | Defines the `Pacman` class, which inherits from `Entity`. It handles player input and interactions with pellets and ghosts.                |
| `ghosts.py`          | Defines the `Ghost` base class and the four individual ghost classes (`Blinky`, `Pinky`, `Inky`, `Clyde`), each with its unique AI.         |
| `nodes.py`           | Manages the maze's node-based graph structure. The `NodeGroup` class reads a maze file and creates a network of interconnected nodes.      |
| `mazedata.py`        | Contains the data for the different maze layouts.                                                                                        |
| `pellets.py`         | Manages the pellets in the maze. The `PelletGroup` class creates and keeps track of normal pellets and power pellets.                      |
| `fruit.py`           | Defines the `Fruit` entity that appears as a bonus item.                                                                                 |
| `sprites.py`         | Handles loading and managing all the game's sprites from a single spritesheet. It includes classes for Pacman, Ghost, and other sprites. |
| `animation.py`       | A simple animator class to handle frame-based animations for the sprites.                                                                |
| `modes.py`           | Manages the different AI modes for the ghosts (Chase, Scatter, Freight).                                                                 |
| `pauser.py`          | A simple class to handle pausing and unpausing the game.                                                                                 |
| `text.py`            | Manages the rendering of all text on the screen, including the score, level, and game status messages.                                   |
| `maze1.txt`, `maze2.txt` | Text files that define the layout of the mazes.                                                                                        |
| `spritesheet_mspacman.png` | The spritesheet containing all the images for the game's characters and UI elements.                                                 |

## Code Overview

### `GameController` (`run.py`)

This is the heart of the game. The `GameController` class is responsible for:

*   Initializing Pygame and the game window.
*   Managing the main game loop.
*   Handling user input and other events.
*   Updating the state of all game objects.
*   Rendering everything to the screen.
*   Managing game states like starting a new game, advancing to the next level, and game over.

### `Entity` (`entity.py`)

The `Entity` class is a base class for Pacman and the ghosts. It provides common functionality for all moving entities, such as:

*   **Position and Direction:** Using `Vector2` for position and direction vectors.
*   **Movement:** Updating the entity's position based on its speed and direction.
*   **Node-based Navigation:** Moving between nodes in the maze graph.
*   **Collision Detection:** A simple radius-based collision check.

### `Pacman` (`pacman.py`)

The `Pacman` class, inheriting from `Entity`, adds player-specific behavior:

*   **Player Control:** Reads keyboard input to change Pacman's direction.
*   **Eating Pellets:** Detects collisions with pellets and removes them from the maze.
*   **Collision with Ghosts:** Handles interactions with ghosts, either dying or eating them in Freight mode.

### `Ghost` (`ghosts.py`)

The `Ghost` class is the base for the four enemy ghosts. It implements the core ghost logic:

*   **AI Modes:** The `ModeController` class manages the ghost's current mode (Chase, Scatter, or Freight).
*   **Targeting:** Each ghost has a `goal` position that it tries to reach. The `goalDirection` method determines the best direction to move towards the goal.
*   **Individual AI:** The subclasses for each ghost (`Blinky`, `Pinky`, `Inky`, `Clyde`) implement their own unique `chase` method to set their target based on Pacman's position and other factors.

### `NodeGroup` (`nodes.py`)

This class is responsible for building the maze's navigation graph from a text file.

*   **Maze Parsing:** Reads a text file where characters represent different parts of the maze (nodes, paths, walls).
*   **Node Creation:** Creates `Node` objects for each junction in the maze.
*   **Connecting Nodes:** Connects the nodes horizontally and vertically to form a graph that entities can traverse.

### Sprites and Animations (`sprites.py`, `animation.py`)

*   **`Spritesheet`:** A class to load the main spritesheet and extract individual images from it.
*   **`PacmanSprites`, `GhostSprites`, etc.:** Classes that manage the animations for each entity. They use the `Animator` class to cycle through a sequence of images to create the illusion of movement.

## Game Mechanics

### Ghost AI

The ghost AI is a key feature of the game. Each ghost has a distinct personality, determined by its targeting logic in Chase mode.

*   **Blinky (Red):** The most aggressive ghost. Blinky's target is always Pacman's current position.
*   **Pinky (Pink):** The ambusher. Pinky tries to get ahead of Pacman by targeting a few tiles in front of Pacman's current direction.
*   **Inky (Cyan):** The unpredictable one. Inky's target is calculated based on both Pacman's and Blinky's positions, making him flank Pacman from unexpected angles.
*   **Clyde (Orange):** The one who does his own thing. Clyde's target is Pacman's position, but if he gets too close to Pacman, he switches his target to his scatter corner, making him seem shy or unpredictable.

### Scoring

*   **Pellet:** 10 points
*   **Power Pellet:** 50 points
*   **Ghosts (Freight Mode):**
    *   1st ghost: 200 points
    *   2nd ghost: 400 points
    *   3rd ghost: 800 points
    *   4th ghost: 1600 points
*   **Fruit:** Points vary depending on the level (100, 300, 500, etc.).

## Dependencies

*   **Python 3:** The game is written in Python 3.
*   **Pygame:** A cross-platform set of Python modules designed for writing video games.
*   **NumPy:** Used for reading the maze and pellet data from text files.
