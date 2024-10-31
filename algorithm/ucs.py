from utils import PriorityQueue, readMap, all_stones_on_targets, is_valid_move, dx, dy, actionsMap, heuristicCost
import time
import tracemalloc
import os

# Thuật toán UCS với các tối ưu hóa
def ucs(start_x, start_y, stones, switches_pos, walls_pos, weights):
    priority_queue = PriorityQueue()
    # Đưa trạng thái ban đầu vào hàng đợi với chi phí 0
    priority_queue.push((0, 0, start_x, start_y, stones, []), 0)
    visited = {}
    expanded_nodes = 0

    while not priority_queue.is_empty():
        # Lấy trạng thái có chi phí thấp nhất từ hàng đợi
        total_cost, stone_push_weight, x, y, current_stones, path = priority_queue.pop()

        # Kiểm tra điều kiện đích: tất cả đá đã được đặt trên công tắc
        if all_stones_on_targets(current_stones, switches_pos):
            return path, total_cost, stone_push_weight, expanded_nodes

        # Trạng thái hiện tại với đá đã sắp xếp để kiểm tra trùng lặp
        state = (x, y, tuple(sorted(current_stones)))
        if state in visited and visited[state] <= total_cost:
            continue
        visited[state] = total_cost
        expanded_nodes += 1

        # Thử tất cả các hướng di chuyển
        for i in range(4):
            next_x, next_y = x + dx[i], y + dy[i]
            new_stones = list(current_stones)  # Cập nhật đá khi cần thiết
            action_cost = 1  # Chi phí di chuyển thông thường

            # Nếu vị trí tiếp theo là một viên đá
            if (next_x, next_y) in [(stone[0], stone[1]) for stone in current_stones]:
                stone_index = next((index for index, stone in enumerate(current_stones) if (stone[0], stone[1]) == (next_x, next_y)), None)
                new_stone_x, new_stone_y = next_x + dx[i], next_y + dy[i]

                # Kiểm tra tính hợp lệ của di chuyển đá
                if stone_index is not None and is_valid_move(new_stone_x, new_stone_y, current_stones, walls_pos):
                    # Cập nhật vị trí của viên đá bị đẩy
                    new_stones[stone_index] = (new_stone_x, new_stone_y, weights[stone_index])
                    new_cost = total_cost + weights[stone_index]
                    new_stone_push_weight = stone_push_weight + weights[stone_index]
                    
                    # Tính heuristic cho trạng thái mới để ưu tiên mở rộng
                    heuristic = heuristicCost(new_stones, switches_pos)
                    priority_queue.push(
                        (new_cost, new_stone_push_weight, next_x, next_y, new_stones, path + [actionsMap[i + 4]]),
                        new_cost + heuristic
                    )
            # Nếu di chuyển là hợp lệ mà không đẩy đá
            elif is_valid_move(next_x, next_y, current_stones, walls_pos):
                new_cost = total_cost + action_cost
                heuristic = heuristicCost(current_stones, switches_pos)
                priority_queue.push(
                    (new_cost, stone_push_weight, next_x, next_y, current_stones, path + [actionsMap[i]]),
                    new_cost + heuristic
                )

    return None, 0, 0, expanded_nodes

# Hàm giải mê cung và lưu kết quả
def solve_maze(filename):
    player_pos, stones, switches, walls, maze = readMap(filename)
    weights = [stone[2] for stone in stones]

    tracemalloc.start()
    start_time = time.time()

    path, total_cost, stone_push_weight, expanded_nodes = ucs(player_pos[0], player_pos[1], stones, switches, walls, weights)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    output_filename = "output/output-" + os.path.basename(filename).split('-')[1]
    if path:
        with open(output_filename, "a") as output_file:
            output_file.write("UCS\n")
            output_file.write(f"Steps: {len(path)}, Weight: {stone_push_weight}, Nodes: {expanded_nodes}, "
                              f"Time (ms): {(end_time - start_time) * 1000:.2f}, "
                              f"Memory (MB): {peak / (1024 * 1024):.2f}\n")
            output_file.write("".join(path) + "\n")
        print(f"Kết quả đã được ghi vào {output_filename}")
    else:
        print("Không tìm thấy đường đi với UCS.")
