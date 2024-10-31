import heapq
import time
import tracemalloc
import os
from utils import *

def ucs(maze, x, y, stones, targets, weights):
    targets_set = set(targets)
    rows, cols = len(maze), len(maze[0])
    moves = [(-1, 0, 'u'), (1, 0, 'd'), (0, -1, 'l'), (0, 1, 'r')]

    deadlock_corners = {(i, j) 
        for i in range(1, rows-1) 
        for j in range(1, cols-1) 
        if maze[i][j] != '#' and (i,j) not in targets_set and (
            (maze[i-1][j] == '#' and maze[i][j-1] == '#') or
            (maze[i-1][j] == '#' and maze[i][j+1] == '#') or
            (maze[i+1][j] == '#' and maze[i][j-1] == '#') or
            (maze[i+1][j] == '#' and maze[i][j+1] == '#')
        )}

    priority_queue = [(0, x, y, tuple(stones), [])]
    visited = {}
    expanded_nodes = 0

    while priority_queue:
        cost, current_x, current_y, current_stones, path = heapq.heappop(priority_queue)
        
        state = (current_x, current_y, tuple(current_stones))
        if state in visited and visited[state] <= cost:
            continue
            
        if set(current_stones) == targets_set:
            return path, cost, expanded_nodes
            
        visited[state] = cost
        expanded_nodes += 1

        for dx, dy, direction in moves:
            next_x, next_y = current_x + dx, current_y + dy
            
            if not (0 <= next_x < rows and 0 <= next_y < cols) or maze[next_x][next_y] == '#':
                continue

            if (next_x, next_y) in current_stones:
                new_stone_x, new_stone_y = next_x + dx, next_y + dy
                
                if not (0 <= new_stone_x < rows and 
                       0 <= new_stone_y < cols and 
                       maze[new_stone_x][new_stone_y] != '#' and 
                       (new_stone_x, new_stone_y) not in current_stones):
                    continue
                
                if (new_stone_x, new_stone_y) in deadlock_corners:
                    continue
                    
                i = current_stones.index((next_x, next_y))
                new_stones = list(current_stones)
                new_stones[i] = (new_stone_x, new_stone_y)
                new_stones = tuple(new_stones)
                new_cost = cost + weights[i]
                
                new_state = (next_x, next_y, new_stones)
                if new_state not in visited or visited[new_state] > new_cost:
                    heapq.heappush(priority_queue, 
                                 (new_cost, next_x, next_y, new_stones, path + [direction.upper()]))

            else:
                new_state = (next_x, next_y, current_stones)
                if new_state not in visited or visited[new_state] > cost:
                    heapq.heappush(priority_queue, 
                                 (cost, next_x, next_y, current_stones, path + [direction]))

    return None, 0, expanded_nodes

def solve_maze(filename):
    weights, maze = read_maze_from_file(filename)
    ares, stones, targets = find_positions(maze)

    if ares is None or not stones or not targets or len(stones) != len(targets):
        print("Mê cung không có vị trí hợp lệ hoặc số lượng đá và đích không khớp.")
        return

    tracemalloc.start()
    start_time = time.time()
    
    path, weight, expanded_nodes = ucs(maze, ares[0], ares[1], stones, targets, weights)

    end_time = time.time()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    output_filename = "output/output-" + os.path.basename(filename).split('-')[1]
    if path:
        with open(output_filename, "a") as output_file:
            output_file.write("UCS\n")
            output_file.write(f"Steps: {len(path)}, Weight: {weight}, Node: {expanded_nodes}, "
                              f"Time (ms): {(end_time - start_time) * 1000:.2f}, "
                              f"Memory (MB): {peak / (1024 * 1024):.2f}\n")
            output_file.write("".join(path) + "\n")
        print(f"Kết quả đã được ghi vào {output_filename}")
    else:
        print("Không tìm thấy đường đi với UCS.")

