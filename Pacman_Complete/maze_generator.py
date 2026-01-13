
import random

def generate_maze(width=28, height=31):
    """Generates a maze using a recursive backtracking algorithm."""
    maze = [["+" for _ in range(width)] for _ in range(height)]

    def is_valid(x, y):
        return 0 <= x < width and 0 <= y < height

    def carve_passages(cx, cy):
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if is_valid(nx, ny) and maze[ny][nx] == "+":
                maze[ny][nx] = "."
                maze[cy + dy // 2][cx + dx // 2] = "."
                carve_passages(nx, ny)

    # Start carving from a random odd position
    start_x, start_y = (random.randrange(1, width, 2), random.randrange(1, height, 2))
    maze[start_y][start_x] = "."
    carve_passages(start_x, start_y)

    # Add some random pellets
    for y in range(height):
        for x in range(width):
            if maze[y][x] == ".":
                if random.random() < 0.6:
                    maze[y][x] = "."

    # Add power pellets
    for _ in range(4):
        x, y = (random.randrange(1, width - 1), random.randrange(1, height - 1))
        if maze[y][x] == ".":
            maze[y][x] = "p"
            
    # Set home for ghost
    maze[14][12] = "h"
    maze[14][13] = "h"
    maze[14][14] = "h"
    maze[14][15] = "h"


    return ["".join(row) for row in maze]

if __name__ == "__main__":
    generated_maze = generate_maze()
    for row in generated_maze:
        print(row)
