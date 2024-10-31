from utils import readMap, all_stones_on_targets, is_valid_move, dx, dy, actionsMap
import time
import tracemalloc
import os
from collections import deque

# Thuật toán DFS với giới hạn độ sâu và tối ưu hóa
def dfs(matrix, start_x, start_y, stones, targets, weights, walls_pos, max_depth):
    # Sử dụng deque thay vì list để làm ngăn xếp
    stack = deque([(start_x, start_y, stones, [], 0, 0)])  # (x, y, stones, path, depth, accumulated_weight)
    visited = set()
    expanded_nodes = 0

    while stack:
        x, y, stones, path, depth, weight_temp = stack.pop()

        # Giới hạn độ sâu
        if depth > max_depth:
            continue

        # Kiểm tra trạng thái đích
        if all_stones_on_targets(stones, targets):
            return path, weight_temp, expanded_nodes

        # Tạo khóa trạng thái để tránh trùng lặp
        state = (x, y, tuple(sorted((sx, sy) for sx, sy, _ in stones)))
        if state in visited:
            continue
        visited.add(state)
        expanded_nodes += 1

        # Duyệt tất cả các hướng
        for i in range(4):
            next_x, next_y = x + dx[i], y + dy[i]
            new_stones = list(stones)  # Sao chép trạng thái đá

            # Kiểm tra nếu di chuyển đến một viên đá
            if (next_x, next_y) in [(sx, sy) for sx, sy, _ in stones]:
                stone_index = [(sx, sy) for sx, sy, _ in stones].index((next_x, next_y))
                new_stone_x, new_stone_y = next_x + dx[i], next_y + dy[i]

                # Kiểm tra tính hợp lệ của việc di chuyển viên đá
                if stone_index is not None and is_valid_move(new_stone_x, new_stone_y, stones, walls_pos):
                    new_stones[stone_index] = (new_stone_x, new_stone_y, weights[stone_index])
                    # Đẩy vào ngăn xếp với cập nhật vị trí và hành động
                    stack.append((next_x, next_y, new_stones, path + [actionsMap[i].upper()], depth + 1, weight_temp + weights[stone_index]))
            # Kiểm tra tính hợp lệ của di chuyển không đẩy đá
            elif is_valid_move(next_x, next_y, stones, walls_pos):
                stack.append((next_x, next_y, stones, path + [actionsMap[i]], depth + 1, weight_temp))

    return None, 0, expanded_nodes

# Hàm giải mê cung và lưu kết quả
def solve_maze(filename, initial_depth=10, max_increment=10, max_limit=1000):
    # Đọc dữ liệu từ file
    player_pos, stones, switches, walls, maze = readMap(filename)
    weights = [stone[2] for stone in stones]

    tracemalloc.start()
    start_time = time.time()

    path, weight, expanded_nodes = None, 0, 0
    current_depth = initial_depth

    # Thực hiện DFS với tăng độ sâu tối đa
    while current_depth <= max_limit:
        path, weight, expanded_nodes = dfs(maze, player_pos[0], player_pos[1], stones, switches, weights, walls, current_depth)
        if path:
            break
        current_depth += max_increment

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Lưu kết quả vào file
    output_filename = "output/output-" + os.path.basename(filename).split('-')[1]
    
    if path:
        # Ghi kết quả nếu tìm thấy đường đi
        with open(output_filename, "a") as output_file:
            output_file.write("DFS\n")
            output_file.write(f"Steps: {len(path)}, Weight: {weight}, Nodes: {expanded_nodes}, "
                              f"Time (ms): {(end_time - start_time) * 1000:.2f}, "
                              f"Memory (MB): {peak / (1024 * 1024):.2f}\n")
            output_file.write("".join(path) + "\n")
        print(f"Kết quả đã được ghi vào {output_filename}")
    else:
        # Thông báo nếu không tìm thấy đường đi
        print("Không tìm thấy đường đi với DFS.")
