# dfs.py
import time
import tracemalloc
import os
from utils import read_maze_from_file, find_positions, all_stones_on_targets, is_valid_move

def dfs(maze, x, y, stones, targets, weights, max_depth):
    stack = [(x, y, stones, [], 0, 0)]
    visited = set()
    expanded_nodes = 0

    while stack:
        x, y, stones, path, depth, weight_temp = stack.pop()

        if depth > max_depth:
            continue

        if all_stones_on_targets(stones, targets):
            return path, weight_temp, expanded_nodes

        state = (x, y, tuple(sorted(stones)))
        if state in visited:
            continue
        visited.add(state)
        expanded_nodes += 1

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        move_directions = ['u', 'd', 'l', 'r']

        for move, direction in zip(moves, move_directions):
            next_x, next_y = x + move[0], y + move[1]
            new_stones = list(stones)

            if (next_x, next_y) in stones:
                i = stones.index((next_x, next_y))
                new_stone_x, new_stone_y = next_x + move[0], next_y + move[1]
                if i < len(weights) and is_valid_move(maze, new_stone_x, new_stone_y, stones):
                    new_stones[i] = (new_stone_x, new_stone_y)
                    stack.append((next_x, next_y, new_stones, path + [direction.upper()], depth + 1, weight_temp + weights[i]))
            elif is_valid_move(maze, next_x, next_y, stones):
                stack.append((next_x, next_y, stones, path + [direction], depth + 1, weight_temp))

    return None, 0, expanded_nodes

def solve_maze(filename, initial_depth=10, max_increment=10, max_limit=1000):
    weights, maze = read_maze_from_file(filename)
    player_pos, stones, targets = find_positions(maze)

    tracemalloc.start()
    start_time = time.time()

    path, weight, expanded_nodes = None, 0, 0
    current_depth = initial_depth

    while current_depth <= max_limit:
        path, weight, expanded_nodes = dfs(maze, player_pos[0], player_pos[1], stones, targets, weights, current_depth)
        if path:
            break
        current_depth += max_increment

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    output_filename = "output/output-" + os.path.basename(filename).split('-')[1]
    with open(output_filename, "a") as output_file:
        output_file.write("DFS\n")
        output_file.write(f"Steps: {len(path)}, Weight: {weight}, Nodes: {expanded_nodes}, "
                          f"Time (ms): {(end_time - start_time) * 1000:.2f}, "
                          f"Memory (MB): {peak / (1024 * 1024):.2f}\n")
        output_file.write("".join(path) + "\n")
    print(f"Result saved to {output_filename}")
