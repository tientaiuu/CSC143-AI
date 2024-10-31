from collections import deque
from utils import *
import time
import tracemalloc
import os

def bfs(maze, x, y, stones, targets, weights):
    queue = deque([(x, y, tuple(stones), [], 0)]) 
    visited = set() 
    expanded_nodes = 0  

    while queue:
        x, y, stones, path, weight_temp = queue.popleft()

        # kiểm tra điều kiện
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

            # di chuyển vào stone
            if (next_x, next_y) in stones:
                i = stones.index((next_x, next_y))
                new_stone_x, new_stone_y = next_x + move[0], next_y + move[1]
                
                # kiểm tra điều kiện đẩy đá
                if i < len(weights) and is_valid_move(maze, new_stone_x, new_stone_y, stones):
                    new_stones[i] = (new_stone_x, new_stone_y)
                    queue.append((next_x, next_y, new_stones, path + [direction.upper()], weight_temp + weights[i]))
            
            # kiểm tra nếu vị trí kế là hợp lệ và không có đá
            elif is_valid_move(maze, next_x, next_y, stones):
                queue.append((next_x, next_y, stones, path + [direction], weight_temp))

    return None, 0, expanded_nodes 

def solve_maze(filename):
    weights, maze = read_maze_from_file(filename)
    ares, stones, targets = find_positions(maze)

    if ares is None or not stones or not targets or len(stones) != len(targets):
        print("Mê cung không có vị trí hợp lệ hoặc số lượng đá và đích không khớp.")
        return

    tracemalloc.start()
    start_time = time.time()
    
    path, weight, expanded_nodes = bfs(maze, ares[0], ares[1], stones, targets, weights)

    end_time = time.time()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    output_filename = "output/output-" + os.path.basename(filename).split('-')[1]
    if path:
        with open(output_filename, "a") as output_file:
            output_file.write("BFS\n")
            output_file.write(f"Steps: {len(path)}, Weight: {weight}, Node: {expanded_nodes}, "
                              f"Time (ms): {(end_time - start_time) * 1000:.2f}, "
                              f"Memory (MB): {peak / (1024 * 1024):.2f}\n")
            output_file.write("".join(path) + "\n")
        print(f"Kết quả đã được ghi vào {output_filename}")
    else:
        print("Không tìm thấy đường đi với BFS.")