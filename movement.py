from maze import *
from collections import deque

DIRECTIONS = {
    'UP': (-1, 0),
    'DOWN': (1, 0),
    'LEFT': (0, -1),
    'RIGHT': (0, 1)
}

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze

    def is_valid_move(self, pos):
        y, x = pos
        return 0 <= y < len(self.maze.grid) and 0 <= x < len(self.maze.grid[0]) and self.maze.grid[y][x] != '#'

    def move(self, position, direction):
        dy, dx = DIRECTIONS[direction]
        new_position = (position[0] + dy, position[1] + dx)
        if self.is_valid_move(new_position):
            return new_position
        return None

    def push_stone(self, position, stone, direction):
        dy, dx = DIRECTIONS[direction]
        new_stone_position = (stone[0] + dy, stone[1] + dx)
        if self.is_valid_move(new_stone_position) and new_stone_position not in self.maze.stones:
            return new_stone_position
        return None
    def bfs(self):
        start = (self.maze.ares_position, tuple(self.maze.stones))
        queue = deque([start])
        visited = set([start])
        
        while queue:
            (ares_pos, stones) = queue.popleft()

            if self.is_goal_state(stones):
                print("Goal reached!")
                return

            for direction in DIRECTIONS:
                new_ares_pos = self.move(ares_pos, direction)
                
                if new_ares_pos:
                    # Check if Ares is next to a stone
                    if new_ares_pos in stones:
                        stone_index = stones.index(new_ares_pos)
                        new_stone_pos = self.push_stone(ares_pos, stones[stone_index], direction)

                        if new_stone_pos:
                            new_stones = list(stones)
                            new_stones[stone_index] = new_stone_pos
                            new_state = (new_ares_pos, tuple(new_stones))
                            if new_state not in visited:
                                queue.append(new_state)
                                visited.add(new_state)
                    else:
                        # No stone, just move Ares
                        new_state = (new_ares_pos, stones)
                        if new_state not in visited:
                            queue.append(new_state)
                            visited.add(new_state)
    
    def is_goal_state(self, stones):
        return all(stone in self.maze.switches for stone in stones)

# Solve the maze using BFS
solver = MazeSolver(maze)
solver.bfs()