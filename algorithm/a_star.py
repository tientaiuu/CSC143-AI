import time as TIME
import tracemalloc
import os
import psutil
from utils import readMap, typeOfAction, heuristicCost, all_stones_on_targets, is_valid_move, dx, dy, actionsMap, PriorityQueue, checkAllSwitch

def a_star(file_name='input-01.txt'):
    
    process = psutil.Process()
    actions_taken, total_weight, nodes_expanded, elapsed_time, memory_usage = '', 0, 0, 0, 0
    memory_usage = process.memory_info().rss
    player_position, stones_position, switches_position, walls_position, _ = readMap(file_name)
    
    frontier = PriorityQueue(0)
    frontier.push((player_position, stones_position, actions_taken, total_weight, 0), 0)    
    explored_states = set()
    elapsed_time = TIME.time()
    max_memory_usage = memory_usage
    path_length = 0
    
    while not frontier.is_empty():
        current_state = frontier.pop()
        player_position = current_state[0]
        stones_position = current_state[1]
        actions_taken = current_state[2]
        total_weight = current_state[3]
        cost_so_far = current_state[4]
        
        if (player_position, stones_position) in explored_states:
            continue
        
        explored_states.add((player_position, stones_position))

        if checkAllSwitch(stones_position, switches_position):
            elapsed_time = TIME.time() - elapsed_time
            max_memory_usage = max(max_memory_usage, process.memory_info().rss)
            memory_usage = max_memory_usage - memory_usage
            path_length = len(actions_taken)
            break
        
        for direction in range(4):
            new_x = dx[direction] + player_position[0]
            new_y = dy[direction] + player_position[1]
            
            action_type = typeOfAction(direction, (new_x, new_y), stones_position, switches_position, walls_position)
            if action_type == 1:
                continue
            
            updated_stones_position = stones_position
            updated_weight = total_weight
            push_cost = 0.01
            
            if action_type == 4:
                push_cost = [stone for stone in updated_stones_position if (stone[0], stone[1]) == (new_x, new_y)][0][-1]
                updated_stones_position = tuple(stone for stone in updated_stones_position if (stone[0], stone[1]) != (new_x, new_y))
                updated_stones_position += ((new_x + dx[direction], new_y + dy[direction], push_cost), )
                updated_weight += push_cost
            
            updated_stones_position = tuple(sorted(updated_stones_position, key=lambda pos: (pos[0], pos[1])))
            
            if ((new_x, new_y), updated_stones_position) in explored_states:
                continue
            
            nodes_expanded += 1
            total_cost = cost_so_far + push_cost
            priority = total_cost + heuristicCost(updated_stones_position, switches_position)
            frontier.push(((new_x, new_y), updated_stones_position, actions_taken + actionsMap[direction + action_type], updated_weight, total_cost), priority)
    
    return actions_taken, path_length, total_weight, nodes_expanded, elapsed_time, memory_usage

def solve_maze(file_name='input-01.txt'):
    tracemalloc.start()
    start_time = TIME.time()
    
    # Gọi hàm a_star và nhận kết quả
    actions, steps, weight, nodes, exec_time, memory = a_star(file_name)
    
    end_time = TIME.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    # Xác định tên file đầu ra
    output_filename = "output/output-" + os.path.basename(file_name).split('-')[1]

    if steps != 0:  # Kiểm tra nếu tìm thấy kết quả
        with open(output_filename, "a") as output_file:
            output_file.write("A*\n")
            output_file.write(f"Steps: {steps}, Weight: {weight}, Nodes: {nodes}, "
                              f"Time (ms): {(end_time - start_time) * 1000:.2f}, "
                              f"Memory (MB): {peak / (1024 * 1024):.2f}\n")
            output_file.write("".join(actions) + "\n")
        print(f"Result saved to {output_filename}")
    else:  # Nếu không tìm thấy kết quả
        print("Không tìm thấy đường đi với A*.")