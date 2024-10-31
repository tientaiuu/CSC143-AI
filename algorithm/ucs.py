import time
import tracemalloc
import os
import heapq

# Đọc mê cung từ file
def read_maze_from_file(filename):
    with open(filename, 'r') as file:
        weights = list(map(int, file.readline().strip().split()))
        maze = [list(line.strip()) for line in file.readlines()]
    return weights, maze

# Tìm vị trí ban đầu của Ares, đá, và công tắc
def find_positions(maze):
    ares, stones, targets = None, [], []
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            if cell == '@':
                ares = (x, y)
            elif cell == '$':
                stones.append((x, y))
            elif cell == '.':
                targets.append((x, y))
    return ares, stones, targets

# Kiểm tra nếu tất cả đá đã ở trên công tắc
def all_stones_on_targets(stones, targets):
    return all(stone in targets for stone in stones)

# Kiểm tra nếu di chuyển hợp lệ
def is_valid_move(maze, x, y, stones):
    rows, cols = len(maze), len(maze[0])
    return 0 <= x < cols and 0 <= y < rows and maze[y][x] != '#' and (x, y) not in stones

# UCS để tìm chi phí tối ưu nhất
def ucs(maze, start_x, start_y, stones, targets, weights):
    priority_queue = [(0, 0, start_x, start_y, stones, [])]  # (total_cost, stone_push_weight, x, y, stones, path)
    visited = {}
    expanded_nodes = 0
    best_solution = None

    while priority_queue:
        total_cost, stone_push_weight, x, y, current_stones, path = heapq.heappop(priority_queue)

        # Điều kiện đích: Nếu đạt, tiếp tục tìm để đảm bảo tối ưu
        if all_stones_on_targets(current_stones, targets):
            if best_solution is None or total_cost < best_solution[0]:
                best_solution = (total_cost, path, stone_push_weight)
            continue  # Duyệt tiếp các trạng thái khác có chi phí thấp hơn

        # Chỉ mở rộng nếu trạng thái là tối ưu
        state = (x, y, tuple(sorted(current_stones)))
        if state in visited and visited[state] <= total_cost:
            continue
        visited[state] = total_cost
        expanded_nodes += 1

        # Các hướng di chuyển có thể (lên, xuống, trái, phải)
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        move_directions = ['u', 'd', 'l', 'r']

        for move, direction in zip(moves, move_directions):
            next_x, next_y = x + move[0], y + move[1]
            new_stones = list(current_stones)

            # Xử lý đẩy đá
            if (next_x, next_y) in current_stones:
                stone_index = current_stones.index((next_x, next_y))
                new_stone_x, new_stone_y = next_x + move[0], next_y + move[1]

                if stone_index < len(weights) and is_valid_move(maze, new_stone_x, new_stone_y, current_stones):
                    new_stones[stone_index] = (new_stone_x, new_stone_y)
                    heapq.heappush(priority_queue, (
                        total_cost + weights[stone_index],
                        stone_push_weight + weights[stone_index],
                        next_x, next_y, new_stones, path + [direction.upper()]
                    ))
            elif is_valid_move(maze, next_x, next_y, current_stones):
                # Di chuyển không đẩy đá, tăng chi phí 1
                heapq.heappush(priority_queue, (
                    total_cost + 1,
                    stone_push_weight,
                    next_x, next_y, current_stones, path + [direction]
                ))

    # Trả về giải pháp có chi phí thấp nhất
    return best_solution[1], best_solution[0], best_solution[2], expanded_nodes if best_solution else (None, 0, 0, expanded_nodes)

def solve_maze(filename):
    weights, maze = read_maze_from_file(filename)
    ares, stones, targets = find_positions(maze)

    if ares is None or not stones or not targets or len(stones) != len(targets):
        print("Mê cung không hợp lệ hoặc số lượng đá và đích không khớp.")
        return

    tracemalloc.start()
    start_time = time.time()

    path, total_cost, stone_push_weight, expanded_nodes = ucs(maze, ares[0], ares[1], stones, targets, weights)

    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    output_filename = "output/output-" + os.path.basename(filename).split('-')[1]
    if path:
        with open(output_filename, "a") as output_file:
            output_file.write("UCS\n")
            output_file.write(f"Steps: {len(path)}, Cost: {total_cost}, Weight: {stone_push_weight}, "
                              f"Nodes Expanded: {expanded_nodes}, Time (ms): {(end_time - start_time) * 1000:.2f}, "
                              f"Memory (MB): {peak / (1024 * 1024):.2f}\n")
            output_file.write("".join(path) + "\n")
        print(f"Kết quả đã được ghi vào {output_filename}")
    else:
        print("Không tìm thấy đường đi trong giới hạn độ sâu cho phép.")
