import heapq
from itertools import permutations
import psutil


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

def all_stones_on_targets(stones, targets):
    return set(stones) == set(targets)

def is_valid_move(maze, x, y, stones):
    rows, cols = len(maze), len(maze[0])
    return 0 <= x < rows and 0 <= y < cols and maze[x][y] != '#' and (x, y) not in stones

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
actionsMap = 'urdlURDL'

class PriorityQueue:
    def __init__(self, typeOfHeap: bool = True):
        """
        A priority queue class that uses a heap structure.
        - typeOfHeap=True for max-heap (default)
        - typeOfHeap=False for min-heap
        """
        self.heap = []
        self.type = typeOfHeap

    def push(self, item, priority):
        """
        Pushes an item onto the queue with the specified priority.
        """
        heapq.heappush(self.heap, (-priority if self.type else priority, item))

    def pop(self):
        """
        Pops the item with the highest priority from the queue.
        """
        return heapq.heappop(self.heap)[1]

    def is_empty(self):
        """
        Returns True if the queue is empty.
        """
        return len(self.heap) == 0

def readMap(matrix, file_name):
    inp = open(file_name).read().split('\n')
    w = list(map(int, inp[0].split()))
    stones_cost = list(map(int, inp[0].split()))
    inp = inp[1:]
    w = max([len(line) for line in inp])
    h = len(inp)
    matrix = [i for i in inp]
    matrix = [','.join(i).split(',') for i in matrix]
    player_pos, stones_pos, switches_pos, walls_pos = (), (), (), ()
    cnt = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == ' ': matrix[i][j] = 0 # space
            elif matrix[i][j] == '#': # walls
                matrix[i][j] = 1
                walls_pos += ((i, j), )
            elif matrix[i][j] == '$': # stones
                matrix[i][j] = 2
                stones_pos += ((i, j, stones_cost[cnt]), )
                cnt += 1
            elif matrix[i][j] == '@': # ares
                matrix[i][j] = 3
                player_pos = (i, j)
            elif matrix[i][j] == '.': # switches
                matrix[i][j] = 4
                switches_pos += ((i, j), )
            elif matrix[i][j] == '*': # stones + switches
                matrix[i][j] = 5
                stones_pos += ((i, j, stones_cost[cnt]), )
                cnt += 1
                switches_pos += ((i, j), )
            elif matrix[i][j] == '+': # ares + switches
                matrix[i][j] = 6
                player_pos = (i, j)
                switches_pos += ((i, j), )
    return player_pos, stones_pos, switches_pos, walls_pos

def heuristicCost(stones_pos, switches_pos):
    h = 1e18
    temp = permutations(switches_pos)
    for a in temp:
        temp_h = 0
        for i in range(len(a)):
            temp_h += (abs(stones_pos[i][0] - a[i][0]) + abs(stones_pos[i][1] - a[i][1])) * stones_pos[i][2]
        h = min(h, temp_h)
    return h

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
    remain = [x for x in stones_pos if (x[0], x[1]) not in switches_pos]
    return len(remain) == 0
