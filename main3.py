import time
import tracemalloc

def read_maze_from_file(filename):
    with open(filename, 'r') as file:
        weights = list(map(int, file.readline().strip().split()))  # Đọc khối lượng
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

def heuristic_distance(pos, targets):
    return min(abs(pos[0] - target[0]) + abs(pos[1] - target[1]) for target in targets)

def dfs(maze, visited, path, x, y, stones, targets, weights, depth, max_depth, stats, weight_temp):
    if depth > max_depth:
        return False

    if all_stones_on_targets(stones, targets):
        stats["weight"] = weight_temp  # Cập nhật trọng lượng cuối cùng khi tìm được đường đi
        return True

    state = (x, y, tuple(stones))
    if state in visited:
        return False
    visited.add(state)
    stats["expanded_nodes"] += 1

    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    move_directions = ['u', 'd', 'l', 'r']

    # Sắp xếp các hướng đi để tối ưu hóa việc tiếp cận mục tiêu
    moves_sorted = sorted(zip(moves, move_directions), key=lambda m: heuristic_distance((x + m[0][0], y + m[0][1]), targets))

    for move, direction in moves_sorted:
        next_x, next_y = x + move[0], y + move[1]
        new_stones = list(stones)
        stone_moved = False

        # Kiểm tra đá ở vị trí di chuyển tới
        if (next_x, next_y) in stones:
            i = stones.index((next_x, next_y))
            new_stone_x, new_stone_y = next_x + move[0], next_y + move[1]
            if is_valid_move(maze, new_stone_x, new_stone_y, stones):
                new_stones[i] = (new_stone_x, new_stone_y)
                stone_moved = True
                weight_temp += weights[i]  # Thêm khối lượng vào khi đẩy đá
        elif is_valid_move(maze, next_x, next_y, stones):
            path.append(direction)
            stats["steps"] += 1
            if dfs(maze, visited, path, next_x, next_y, stones, targets, weights, depth + 1, max_depth, stats, weight_temp):
                return True
            path.pop()
            stats["steps"] -= 1

        if stone_moved:
            path.append(direction.upper())
            stats["steps"] += 1
            if dfs(maze, visited, path, next_x, next_y, new_stones, targets, weights, depth + 1, max_depth, stats, weight_temp):
                return True
            path.pop()
            stats["steps"] -= 1
            weight_temp -= weights[i]

    visited.remove(state)
    return False

def solve_maze(filename, max_depth=20):
    weights, maze = read_maze_from_file(filename)
    ares, stones, targets = find_positions(maze)

    if ares is None or not stones or not targets or len(stones) != len(targets):
        print("Mê cung không có vị trí hợp lệ hoặc số lượng đá và đích không khớp.")
        return

    path = []
    visited = set()
    stats = {"steps": 0, "weight": 0, "expanded_nodes": 0}
    weight_temp = 0

    tracemalloc.start()
    start_time = time.time()

    if dfs(maze, visited, path, ares[0], ares[1], stones, targets, weights, depth=0, max_depth=max_depth, stats=stats, weight_temp=weight_temp):
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Ghi kết quả vào file output.txt
        with open("output3.txt", "w") as output_file:
            output_file.write("DFS\n")
            output_file.write(f"Steps: {stats['steps']}, Weight: {stats['weight']}, "
                              f"Node: {stats['expanded_nodes']}, Time (ms): {(end_time - start_time) * 1000:.2f}, "
                              f"Memory (MB): {peak / (1024 * 1024):.2f}\n")
            output_file.write("".join(path) + "\n")

        print("Kết quả đã được ghi vào output.txt")
    else:
        tracemalloc.stop()
        print("Không tìm thấy đường đi hoặc vượt quá giới hạn độ sâu.")

def all_stones_on_targets(stones, targets):
    return set(stones) == set(targets)

def is_valid_move(maze, x, y, stones):
    rows, cols = len(maze), len(maze[0])
    return 0 <= x < rows and 0 <= y < cols and maze[x][y] != '#' and (x, y) not in stones

if __name__ == "__main__":
    solve_maze("input4.txt", max_depth=30)
