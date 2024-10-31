# astar.py
import time as TIME
import tracemalloc
import os
from utils import PriorityQueue, readMap, heuristicCost, typeOfAction, checkAllSwitch, psutil

def a_star(file_name='input-01.txt'):
    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]
    actionsMap = 'urdlURDL'
    
    process = psutil.Process()
    actions, weight, node, time, memory = '', 0, 0, 0, 0
    memory = process.memory_info().rss
    matrix = [[]]
    player_pos, stones_pos, switches_pos, walls_pos = readMap(matrix, file_name)
    frontier = PriorityQueue(0)
    frontier.push((player_pos, stones_pos, actions, weight, 0), 0)    
    explored_set = set()
    time = TIME.time()
    max_memory = memory
    steps = 0
    while not frontier.is_empty():
        topQueue = frontier.pop()
        player_pos = topQueue[0]
        stones_pos = topQueue[1]
        actions = topQueue[2]
        weight = topQueue[3]
        g = topQueue[4]
        if (player_pos, stones_pos) in explored_set:
            continue
        
        explored_set.add((player_pos, stones_pos))

        if checkAllSwitch(stones_pos, switches_pos):
            time = TIME.time() - time
            max_memory = max(max_memory, process.memory_info().rss)
            memory = max_memory - memory
            steps = len(actions)
            break
        
        for i in range(4):
            x = dx[i] + player_pos[0]
            y = dy[i] + player_pos[1]
            t = typeOfAction(i, (x, y), stones_pos, switches_pos, walls_pos)
            if t == 1:
                continue
            new_stones_pos = stones_pos
            new_weight = weight
            pushed_stones_weight = 0.01
            if t == 4:
                pushed_stones_weight = [i for i in new_stones_pos if (i[0], i[1]) == (x, y)][0][-1]
                new_stones_pos = tuple(i for i in new_stones_pos if (i[0], i[1]) != (x, y))
                new_stones_pos += ((x + dx[i], y + dy[i], pushed_stones_weight), )
                new_weight += pushed_stones_weight
            new_stones_pos = tuple(sorted(new_stones_pos, key=lambda x: (x[0], x[1])))
            if ((x, y), new_stones_pos) in explored_set:
                continue
            node += 1
            new_g = g + pushed_stones_weight
            frontier.push(((x, y), new_stones_pos, actions + actionsMap[i + t], new_weight, new_g), new_g + heuristicCost(new_stones_pos, switches_pos))
    return actions, steps, weight, node, time, memory

def solve_maze(file_name='input-01.txt'):
    tracemalloc.start()
    start_time = TIME.time()
    actions, steps, weight, nodes, exec_time, memory = a_star(file_name)
    
    end_time = TIME.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    output_filename = "output/output-" + os.path.basename(file_name).split('-')[1]
    with open(output_filename, "a") as output_file:
        output_file.write("A*\n")
        output_file.write(f"Steps: {steps}, Weight: {weight}, Nodes: {nodes}, "
                          f"Time (ms): {(end_time - start_time) * 1000:.2f}, "
                          f"Memory (MB): {peak / (1024 * 1024):.2f}\n")
        output_file.write("".join(actions) + "\n")
    print(f"Result saved to {output_filename}")
