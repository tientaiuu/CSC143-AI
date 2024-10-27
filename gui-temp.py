import tkinter as tk
from tkinter import ttk
import os
import time

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

def read_path_from_file(filename):
    with open(filename, "r") as file:
        directions = file.readlines()[-1].strip()
    return list(directions)

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")

        # Biến lưu trạng thái
        self.maze = None
        self.path = None
        self.weights = None
        self.delay = 500
        self.cell_size = 40
        self.is_paused = False

        # Tạo danh sách các file input và output
        self.input_files = sorted([f for f in os.listdir("input") if f.endswith(".txt")])
        self.output_files = sorted([f for f in os.listdir("output") if f.endswith(".txt")])

        # Tạo giao diện
        self.create_widgets()

    def create_widgets(self):
        # Menu chọn bản đồ
        tk.Label(self.root, text="Select Map:").pack()
        self.map_selector = ttk.Combobox(self.root, values=self.input_files)
        self.map_selector.pack()
        self.map_selector.bind("<<ComboboxSelected>>", self.display_selected_map)  # Hiển thị bản đồ ngay khi chọn

        # Menu chọn thuật toán
        tk.Label(self.root, text="Select Algorithm:").pack()
        self.algo_selector = ttk.Combobox(self.root, values=["DFS", "BFS", "UCS", "A*"])
        self.algo_selector.pack()

        # Nút Start và Pause
        self.start_button = tk.Button(self.root, text="Start", command=self.start_animation)
        self.start_button.pack(pady=5)
        self.pause_button = tk.Button(self.root, text="Pause", command=self.toggle_pause)
        self.pause_button.pack(pady=5)

        # Canvas vẽ mê cung
        self.canvas = tk.Canvas(self.root, bg='white')
        self.canvas.pack()

    def load_maze(self, input_file, output_file):
        self.weights, self.maze = read_maze_from_file(f"input/{input_file}")
        self.path = read_path_from_file(f"output/{output_file}")

    def display_selected_map(self, event):
        # Đọc và hiển thị bản đồ ngay khi chọn
        input_file = self.map_selector.get()
        output_file = f"output-{input_file.split('-')[1]}"
        
        if input_file and output_file in self.output_files:
            self.load_maze(input_file, output_file)
            self.draw_maze()

    def start_animation(self):
        # Đặt lại các biến và bắt đầu hoạt ảnh
        self.is_paused = False
        self.pause_button.config(text="Pause")  # Đặt lại nhãn nút pause
        self.current_step = 0
        self.move_character(0)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_button.config(text="Continue" if self.is_paused else "Pause")
        if not self.is_paused:
            self.move_character(self.current_step)

    def draw_maze(self):
        self.canvas.delete("all")
        rows, cols = len(self.maze), len(self.maze[0])
        self.canvas.config(width=cols * self.cell_size, height=rows * self.cell_size)

        # Vẽ tường, đích và đá
        ares, stones, targets = find_positions(self.maze)

        for i, row in enumerate(self.maze):
            for j, col in enumerate(row):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                if col == '#':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='orange')
                elif col == '.':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='blue')

        # Vẽ nhân vật và đá
        self.ares_rect = self.canvas.create_rectangle(ares[1] * self.cell_size, ares[0] * self.cell_size,
                                                      (ares[1] + 1) * self.cell_size, (ares[0] + 1) * self.cell_size,
                                                      fill='green')
        self.stone_rects = []
        self.stone_labels = []
        for idx, stone in enumerate(stones):
            stone_rect = self.canvas.create_rectangle(stone[1] * self.cell_size, stone[0] * self.cell_size,
                                                      (stone[1] + 1) * self.cell_size, (stone[0] + 1) * self.cell_size,
                                                      fill='gray')
            stone_label = self.canvas.create_text(stone[1] * self.cell_size + self.cell_size // 2,
                                                  stone[0] * self.cell_size + self.cell_size // 2,
                                                  text=str(self.weights[idx]), font=("Arial", 10, "bold"), fill="white")
            self.stone_rects.append(stone_rect)
            self.stone_labels.append(stone_label)

        self.ares = ares
        self.stones = stones
        self.current_step = 0

    def move_character(self, step_index):
        if self.is_paused or step_index >= len(self.path):
            return

        direction = self.path[step_index]
        dx, dy = 0, 0
        if direction.lower() == 'u': dx, dy = -1, 0
        elif direction.lower() == 'd': dx, dy = 1, 0
        elif direction.lower() == 'l': dx, dy = 0, -1
        elif direction.lower() == 'r': dx, dy = 0, 1

        new_ares = (self.ares[0] + dx, self.ares[1] + dy)

        # Xử lý đẩy đá
        if direction.isupper():
            for idx, stone in enumerate(self.stones):
                if stone == new_ares:
                    new_stone_pos = (stone[0] + dx, stone[1] + dy)
                    self.stones[idx] = new_stone_pos
                    self.canvas.coords(self.stone_rects[idx], new_stone_pos[1] * self.cell_size,
                                       new_stone_pos[0] * self.cell_size,
                                       (new_stone_pos[1] + 1) * self.cell_size, (new_stone_pos[0] + 1) * self.cell_size)
                    self.canvas.coords(self.stone_labels[idx], new_stone_pos[1] * self.cell_size + self.cell_size // 2,
                                       new_stone_pos[0] * self.cell_size + self.cell_size // 2)

        # Cập nhật vị trí của nhân vật
        self.ares = new_ares
        self.canvas.coords(self.ares_rect, self.ares[1] * self.cell_size, self.ares[0] * self.cell_size,
                           (self.ares[1] + 1) * self.cell_size, (self.ares[0] + 1) * self.cell_size)

        # Ghi lại bước hiện tại và tiếp tục di chuyển
        self.current_step = step_index + 1
        self.root.after(self.delay, self.move_character, self.current_step)

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
