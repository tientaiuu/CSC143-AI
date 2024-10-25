from collections import deque
import heapq
import time

# BFS
def bfs(maze):
    import tracemalloc
    start_time = time.time()
    tracemalloc.start()
    
    start = maze.start
    queue = deque([(start, [], 0)])  # Thêm trọng lượng tổng đẩy vào hàng đợi
    visited = set()
    visited.add(start)
    nodes_generated = 0
    total_weight_pushed = 0

    while queue:
        (x, y), path, weight_pushed = queue.popleft()
        nodes_generated += 1

        if maze.is_switch(x, y):
            elapsed_time = time.time() - start_time
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            return path, nodes_generated, elapsed_time, weight_pushed, peak / 1024 / 1024  # Chuyển thành MB

        for dx, dy, action in [(-1, 0, 'u'), (1, 0, 'd'), (0, -1, 'l'), (0, 1, 'r')]:
            new_x, new_y = x + dx, y + dy
            if maze.is_valid(new_x, new_y) and (new_x, new_y) not in visited:
                visited.add((new_x, new_y))
                if maze.is_stone(new_x, new_y):
                    # Nếu đẩy đá, thêm trọng lượng của đá vào
                    stone_weight = maze.get_stone_weight(new_x, new_y)
                    queue.append(((new_x, new_y), path + [action.upper()], weight_pushed + stone_weight))
                else:
                    queue.append(((new_x, new_y), path + [action], weight_pushed))

    tracemalloc.stop()
    return None, nodes_generated, time.time() - start_time, 0, 0

