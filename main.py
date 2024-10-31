# main.py
import os
from algorithm.dfs import solve_maze as solve_maze_dfs
from algorithm.bfs import solve_maze as solve_maze_bfs
from algorithm.a_star import solve_maze as solve_maze_a_star
from algorithm.ucs import solve_maze as solve_maze_ucs

def run_all_mazes(input_folder="input", initial_depth=10, max_increment=5, max_limit=1000):
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            
            print(f"Đang xử lý với DFS: {input_path}")
            solve_maze_dfs(input_path, initial_depth=initial_depth, max_increment=max_increment, max_limit=max_limit)
            
            print(f"Đang xử lý với BFS: {input_path}")
            solve_maze_bfs(input_path)
            
            print(f"Processing with A*: {input_path}")
            solve_maze_a_star(input_path)
            
            print(f"Processing with UCS: {input_path}")
            solve_maze_ucs(input_path)


if __name__ == "__main__":
    run_all_mazes()
