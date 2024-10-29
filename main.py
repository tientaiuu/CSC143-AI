import os
from algorithm.dfs import solve_maze as solve_maze_dfs
from algorithm.bfs import solve_maze as solve_maze_bfs
from algorithm.ucs import solve_maze as solve_maze_ucs
from algorithm.a_star import solve_maze as solve_maze_a_star  # Import A*

def run_all_mazes(input_folder="input", initial_depth=10, max_increment=5, max_limit=1000):
    # Lặp qua tất cả các tệp trong thư mục input
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):  # Chỉ xử lý các tệp có đuôi .txt
            input_path = os.path.join(input_folder, filename)
            
            # print(f"Đang xử lý với DFS: {input_path}")
            # solve_maze_dfs(input_path, initial_depth=initial_depth, max_increment=max_increment, max_limit=max_limit)
            
            print(f"Đang xử lý với BFS: {input_path}")
            solve_maze_bfs(input_path)
            
            # print(f"Đang xử lý với UCS: {input_path}")
            # solve_maze_ucs(input_path)
            
            print(f"Đang xử lý với A*: {input_path}")
            solve_maze_a_star(input_path)

if __name__ == "__main__":
    # Chạy giải pháp cho tất cả các tệp input với cả DFS, BFS, UCS, và A*
    run_all_mazes()
