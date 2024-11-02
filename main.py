# main.py
import os
from algorithm.dfs import solve_maze as solve_maze_dfs
from algorithm.bfs import solve_maze as solve_maze_bfs
from algorithm.a_star import solve_maze as solve_maze_a_star
from algorithm.ucs import solve_maze as solve_maze_ucs

def clear_output_folder(output_folder="output"):
    # Kiểm tra thư mục đầu ra tồn tại, nếu có thì xóa các file bên trong
    if os.path.exists(output_folder):
        for filename in os.listdir(output_folder):
            file_path = os.path.join(output_folder, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
    else:
        os.makedirs(output_folder)  # Tạo thư mục nếu chưa tồn tại

def run_all_mazes(input_folder="input", output_folder="output", initial_depth=10, max_increment=5, max_limit=1000):
    # Xóa nội dung thư mục đầu ra trước khi bắt đầu
    clear_output_folder(output_folder)
    
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            print(f"Xử lí file input: {input_path}")
            
            print(f"Đang xử lý với BFS: {input_path}")
            solve_maze_bfs(input_path)
            
            print(f"Đang xử lý với DFS: {input_path}")
            solve_maze_dfs(input_path, initial_depth=initial_depth, max_increment=max_increment, max_limit=max_limit)
            
            print(f"Đang xử lí với UCS: {input_path}")
            solve_maze_ucs(input_path)
            
            print(f"Đang xử lí với A*: {input_path}")
            solve_maze_a_star(input_path)
            
if __name__ == "__main__":
    run_all_mazes()