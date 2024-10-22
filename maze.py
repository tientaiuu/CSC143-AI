class Maze:
    def __init__(self, filename):
        self.grid = []
        self.stone_weights = []
        self.ares_position = None
        self.stones = []
        self.switches = []
        self.load_maze(filename)

    def load_maze(self, filename):
        with open(filename, 'r') as file:
            # First line contains stone weights
            self.stone_weights = list(map(int, file.readline().strip().split()))
            
            # Read the grid
            for y, line in enumerate(file):
                row = list(line.rstrip())
                self.grid.append(row)
                
                # Locate positions of Ares, stones, and switches
                for x, char in enumerate(row):
                    if char == '@':  # Ares start position
                        self.ares_position = (y, x)
                    elif char == '$':  # Stone position
                        self.stones.append((y, x))
                    elif char == '.':  # Switch position
                        self.switches.append((y, x))

    def print_maze(self):
        for row in self.grid:
            print("".join(row))

# Example of loading a maze
maze = Maze('input-01.txt')
maze.print_maze()