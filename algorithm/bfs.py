# bfs.py
from collections import deque
from utils import readMap, all_stones_on_targets, is_valid_move, dx, dy, actionsMap
import time
import tracemalloc
import os


def bfs(matrix, start_x, start_y, stones, targets, weights, walls_pos):
    queue = deque([(start_x, start_y, stones, [], 0, 0)]) 
    visited = set()
    expanded_nodes = 0

    while queue:
        x, y, stones, path, weight_temp, _ = queue.popleft()

        if all_stones_on_targets(stones, targets):
            return path, weight_temp, expanded_nodes

        state = (x, y, tuple(sorted(stones)))
        if state in visited:
            continue
        visited.add(state)
        expanded_nodes += 1

        for i in range(4):
            next_x, next_y = x + dx[i], y + dy[i]
            new_stones = list(stones)

            if (next_x, next_y) in [(sx, sy) for sx, sy, _ in stones]:
                stone_index = [(sx, sy) for sx, sy, _ in stones].index((next_x, next_y))
                new_stone_x, new_stone_y = next_x + dx[i], next_y + dy[i]

                if stone_index is not None and is_valid_move(new_stone_x, new_stone_y, stones, walls_pos):
                    new_stones[stone_index] = (new_stone_x, new_stone_y, weights[stone_index])
                    queue.append((next_x, next_y, new_stones, path + [actionsMap[i].upper()], weight_temp + weights[stone_index], 0))
            elif is_valid_move(next_x, next_y, stones, walls_pos):
                queue.append((next_x, next_y, stones, path + [actionsMap[i]], weight_temp, 0))

    return None, 0, expanded_nodes

# Hàm giải mê cung và lưu kết quả
def solve_maze(filename):
    player_pos, stones, switches, walls, maze = readMap(filename)
    weights = [stone[2] for stone in stones]

    tracemalloc.start()
    start_time = time.time()
    
    path, weight, expanded_nodes = bfs(maze, player_pos[0], player_pos[1], stones, switches, weights, walls)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    output_filename = "output/output-" + os.path.basename(filename).split('-')[1]
    if path:
        with open(output_filename, "a") as output_file:
            output_file.write("BFS\n")
            output_file.write(f"Steps: {len(path)}, Weight: {weight}, Nodes: {expanded_nodes}, "
                              f"Time (ms): {(end_time - start_time) * 1000:.2f}, "
                              f"Memory (MB): {peak / (1024 * 1024):.2f}\n")
            output_file.write("".join(path) + "\n")
        print(f"Kết quả đã được ghi vào {output_filename}")
    else:
        print("Không tìm thấy đường đi với BFS.")