import os
from algorithm.dfs import solve_maze

def run_all_mazes(input_folder="input", initial_depth=10, max_increment=5, max_limit=1000):
    # Lặp qua tất cả các tệp trong thư mục input
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):  # Chỉ xử lý các tệp có đuôi .txt
            input_path = os.path.join(input_folder, filename)
            print(f"Đang xử lý: {input_path}")
            solve_maze(input_path, initial_depth=initial_depth, max_increment=max_increment, max_limit=max_limit)

if __name__ == "__main__":
    # Chạy giải pháp cho tất cả các tệp input
    run_all_mazes()
