from maze import Maze
from algorithms import *
from GUI import *

def read_input(file_name):
    with open(file_name, 'r') as f:
        # Đọc trọng lượng của các viên đá từ dòng đầu tiên
        stone_weights = list(map(int, f.readline().split()))  
        stones = []
        switches = []
        grid = []
        start = None
        stone_index = 0  # Chỉ mục cho trọng lượng của các viên đá

        # Đọc từng dòng của mê cung
        for i, line in enumerate(f.readlines()):
            row = []
            for j, char in enumerate(line.strip()):
                row.append(char)
                if char == '@':
                    start = (i, j)  # Vị trí ban đầu của Ares
                elif char == '+':
                    start = (i, j)  # Ares trên công tắc
                    switches.append((i, j))
                elif char == '$':
                    # Lưu vị trí và trọng lượng của mỗi viên đá
                    stones.append(((i, j), stone_weights[stone_index]))  
                    stone_index += 1
                elif char == '*':
                    stones.append(((i, j), stone_weights[stone_index]))  # Đá đặt trên công tắc
                    switches.append((i, j))
                    stone_index += 1
                elif char == '.':
                    switches.append((i, j))  # Vị trí công tắc không có đá
            grid.append(row)
    
    # Trả về đối tượng Maze với grid, stones, switches, và vị trí bắt đầu của Ares
    return Maze(grid, stones, switches, start)

def write_output(file_name, algorithm_name, path, nodes, elapsed_time, total_weight, memory_used):
    with open(file_name, 'w') as f:
        f.write(f"{algorithm_name}\n")
        f.write(f"Steps: {len(path)}, Weight: {total_weight}, Nodes: {nodes}, Time (ms): {elapsed_time*1000:.2f}, Memory (MB): {memory_used:.2f}\n")
        f.write(''.join(path) + '\n')


def main():
    maze = read_input('input-01.txt')
    path, nodes, elapsed_time, total_weight, memory_used = bfs(maze)
    if path:
        write_output('output-01.txt', 'BFS', path, nodes, elapsed_time, total_weight, memory_used)
        run_gui(maze, path, total_weight)
        
if __name__ == '__main__':
    main()
