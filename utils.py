# utils.py
import heapq
from itertools import permutations

# Các hướng di chuyển (lên, phải, xuống, trái)
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
actionsMap = 'urdlURDL'

# Hàng đợi ưu tiên dùng cho A* và UCS
class PriorityQueue:
    def __init__(self, max_heap=False):
        self.heap = []
        self.max_heap = max_heap

    def push(self, item, priority):
        heapq.heappush(self.heap, ((-priority if self.max_heap else priority), item))

    def pop(self):
        return heapq.heappop(self.heap)[1]

    def is_empty(self):
        return len(self.heap) == 0

# Đọc bản đồ từ file
def readMap(file_name):
    """Đọc và xử lý mê cung từ file, trả về vị trí người chơi, đá, công tắc và tường."""
    with open(file_name, 'r') as file:
        lines = file.read().splitlines()

    stones_cost = list(map(int, lines[0].split()))
    maze = [list(line) for line in lines[1:]]
    player_pos, stones_pos, switches_pos, walls_pos = None, [], [], []

    cnt = 0
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == ' ':
                continue
            elif cell == '#':
                walls_pos.append((i, j))
            elif cell == '$':
                stones_pos.append((i, j, stones_cost[cnt]))
                cnt += 1
            elif cell == '@':
                player_pos = (i, j)
            elif cell == '.':
                switches_pos.append((i, j))
            elif cell == '*':
                stones_pos.append((i, j, stones_cost[cnt]))
                cnt += 1
                switches_pos.append((i, j))
            elif cell == '+':
                player_pos = (i, j)
                switches_pos.append((i, j))
    
    return player_pos, tuple(stones_pos), tuple(switches_pos), tuple(walls_pos), maze

# Tính toán chi phí heuristic dựa trên khoảng cách Manhattan
def heuristicCost(stones_pos, switches_pos):
    min_cost = float('inf')
    for target_permutation in permutations(switches_pos):
        current_cost = sum(
            (abs(stone[0] - target[0]) + abs(stone[1] - target[1])) * stone[2]
            for stone, target in zip(stones_pos, target_permutation)
        )
        min_cost = min(min_cost, current_cost)
    return min_cost

# Kiểm tra nếu tất cả đá đã ở trên công tắc
def all_stones_on_targets(stones, switches_pos):
    return all((stone[0], stone[1]) in switches_pos for stone in stones)

# Kiểm tra tính hợp lệ của một bước di chuyển
def is_valid_move(x, y, stones, walls_pos):
    return (x, y) not in walls_pos and (x, y) not in [(stone[0], stone[1]) for stone in stones]

def typeOfAction(direction, player_pos, stones_pos, switches_pos, walls_pos):
    if player_pos in walls_pos:
        return 1 
    
    for i in stones_pos:
        if player_pos == (i[0], i[1]):
            pushed_stones = (i[0] + dx[direction], i[1] + dy[direction])
            if pushed_stones in walls_pos: return 1
            return 4 if pushed_stones not in ((j[0], j[1]) for j in stones_pos) else 1
    
    return 0

def checkAllSwitch(stones_pos, switches_pos):
    return all((sx, sy) in [(stone[0], stone[1]) for stone in stones_pos] for sx, sy in switches_pos)