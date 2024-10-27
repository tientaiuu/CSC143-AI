def read_maze_from_file(filename):
    with open(filename, 'r') as file:
        weights = list(map(int, file.readline().strip().split()))
        maze = [list(line.strip()) for line in file.readlines()]
    return weights, maze

def find_positions(maze):
    ares = None
    stones = []
    targets = []
    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            if col == '@':
                ares = (i, j)
            elif col == '$':
                stones.append((i, j))
            elif col == '.':
                targets.append((i, j))
    return ares, stones, targets

def all_stones_on_targets(stones, targets):
    return set(stones) == set(targets)

def is_valid_move(maze, x, y, stones):
    rows, cols = len(maze), len(maze[0])
    return 0 <= x < rows and 0 <= y < cols and maze[x][y] != '#' and (x, y) not in stones
