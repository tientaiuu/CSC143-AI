import time
import tracemalloc
import os

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

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Các nước đi: Lên, Xuống, Trái, Phải
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
    ares, stones, targets = find_positions(maze)

    if ares is None or not stones or not targets or len(stones) != len(targets):
        print("Mê cung không có vị trí hợp lệ hoặc số lượng đá và đích không khớp.")
        return

    tracemalloc.start()
    start_time = time.time()

    path, weight, expanded_nodes = None, 0, 0
    current_depth = initial_depth

    # Tăng dần max_depth cho đến khi tìm được lời giải hoặc đạt giới hạn max_limit
    while current_depth <= max_limit:
        path, weight, expanded_nodes = dfs(maze, ares[0], ares[1], stones, targets, weights, current_depth)
        
        if path:
            break  # Tìm được lời giải, thoát vòng lặp
        current_depth += max_increment  # Tăng max_depth thêm một giá trị cố định

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    output_filename = "output/output-" + os.path.basename(filename).split('-')[1]
    if path:
        with open(output_filename, "w") as output_file:
            output_file.write("DFS\n")
            output_file.write(f"Steps: {len(path)}, Weight: {weight}, Node: {expanded_nodes}, "
                              f"Time (ms): {(end_time - start_time) * 1000:.2f}, "
                              f"Memory (MB): {peak / (1024 * 1024):.2f}\n")
            output_file.write("".join(path) + "\n")
        print(f"Kết quả đã được ghi vào {output_filename}")
    else:
        print("Không tìm thấy đường đi trong giới hạn độ sâu cho phép.")

def all_stones_on_targets(stones, targets):
    return set(stones) == set(targets)

def is_valid_move(maze, x, y, stones):
    rows, cols = len(maze), len(maze[0])
    return 0 <= x < rows and 0 <= y < cols and maze[x][y] != '#' and (x, y) not in stones

if __name__ == "__main__":
    solve_maze("input/input-06.txt", initial_depth=10, max_increment=5, max_limit=1000)
