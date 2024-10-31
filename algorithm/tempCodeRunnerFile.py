import time
import tracemalloc
import os
import heapq
from utils import read_maze_from_file, find_positions, all_stones_on_targets, is_valid_move

def heuristic_distance(stones, targets, weights):
    # Tính toán heuristic bằng cách nhân khoảng cách đến mục tiêu với trọng lượng của từng viên đá
    total_heuristic = 0
    for stone, weight in zip(stones, weights):
        distance_to_closest_target = min(abs(stone[0] - target[0]) + abs(stone[1] - target[1]) for target in targets)
        total_heuristic += weight * distance_to_closest_target
    return total_heuristic

def a_star_optimized(maze, start_x, start_y, stones, targets, weights):
    priority_queue = [(0, 0, start_x, start_y, stones, [])]  # (total_cost, path_cost, x, y, stones, path)
    visited = set()
    expanded_nodes = 0

    while priority_queue:
        total_cost, path_cost, x, y, current_stones, path = heapq.heappop(priority_queue)

        # Kiểm tra nếu tất cả các viên đá đã nằm trên công tắc
        if all_stones_on_targets(current_stones, targets):
            return path, path_cost, expanded_nodes

        # Lưu trạng thái đã duyệt
        state = (x, y, tuple(sorted(current_stones)))
        if state in visited:
            continue
        visited.add(state)
        expanded_nodes += 1

        # Các hướng di chuyển cố định (trên, dưới, trái, phải)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        move_directions = ['u', 'd', 'l', 'r']

        for move, direction in zip(moves, move_directions):
            next_x, next_y = x + move[0], y + move[1]
            new_stones = list(current_stones)

            if (next_x, next_y) in current_stones:
                # Nếu di chuyển vào ô có đá, kiểm tra xem có thể đẩy đá hay không
                stone_index = current_stones.index((next_x, next_y))
                new_stone_x, new_stone_y = next_x + move[0], next_y + move[1]

                # Kiểm tra điều kiện đẩy đá hợp lệ
                if stone_index < len(weights) and is_valid_move(maze, new_stone_x, new_stone_y, current_stones):
                    new_stones[stone_index] = (new_stone_x, new_stone_y)
                    new_path_cost = path_cost + weights[stone_index]  # Tăng chi phí bằng trọng lượng đá
                    heuristic = heuristic_distance(new_stones, targets, weights)
                    heapq.heappush(priority_queue, (new_path_cost + heuristic, new_path_cost, next_x, next_y, new_stones, path + [direction.upper()]))
            elif is_valid_move(maze, next_x, next_y, current_stones):
                # Nếu di chuyển bình thường mà không đẩy đá, tăng chi phí thêm 1
                new_path_cost = path_cost + 1
                heuristic = heuristic_distance(new_stones, targets, weights)
                heapq.heappush(priority_queue, (new_path_cost + heuristic, new_path_cost, next_x, next_y, current_stones, path + [direction]))

    return None, 0, expanded_nodes

def solve_maze(filename):
    weights, maze = read_maze_from_file(filename)
    ares, stones, targets = find_positions(maze)

    if ares is None or not stones or not targets or len(stones) != len(targets):
        print("Mê cung không có vị trí hợp lệ hoặc số lượng đá và đích không khớp.")
        return

    tracemalloc.start()
    start_time = time.time()

    path, total_cost, expanded_nodes = a_star_optimized(maze, ares[0], ares[1], stones, targets, weights)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    output_filename = "output/output-" + os.path.basename(filename).split('-')[1]
    if path:
        with open(output_filename, "a") as output_file:  # Mở file ở chế độ append
            output_file.write("A*\n")
            output_file.write(f"Steps: {len(path)}, Weight: {total_cost}, Node: {expanded_nodes}, "
                              f"Time (ms): {(end_time - start_time) * 1000:.2f}, "
                              f"Memory (MB): {peak / (1024 * 1024):.2f}\n")
            output_file.write("".join(path) + "\n")
        print(f"Kết quả đã được ghi vào {output_filename}")
    else:
        print("Không tìm thấy đường đi trong giới hạn độ sâu cho phép.")
