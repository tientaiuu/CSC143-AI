import tkinter as tk
from tkinter import ttk
import os
from PIL import Image, ImageTk  # Sử dụng thư viện Pillow để tải ảnh

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
        lines = file.readlines()
        # Đảm bảo định dạng đầu ra có đúng các dòng thông tin
        if len(lines) >= 2:
            info_line = lines[-2].strip()
            directions = lines[-1].strip()
            # Phân tích dữ liệu từ dòng thông tin (info_line)
            info_parts = info_line.split(", ")
            steps = int(info_parts[0].split(": ")[1])
            weight = int(info_parts[1].split(": ")[1])
            expanded_nodes = int(info_parts[2].split(": ")[1])
            exec_time = float(info_parts[3].split(": ")[1])
            memory = float(info_parts[4].split(": ")[1])
            return directions, steps, weight, expanded_nodes, exec_time, memory
    return [], 0, 0, 0, 0.0, 0.0

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")
        self.root.geometry("1000x600")  # Tăng kích thước cố định của GUI
        self.root.resizable(False, False)

        # Biến lưu trạng thái
        self.maze = None
        self.path = None
        self.weights = None
        self.delay = 500
        self.cell_size = 40
        self.is_paused = False
        self.is_manual_control = False

        # Tải ảnh
        self.load_images()

        # Tạo danh sách các file input và output
        self.input_files = sorted([f for f in os.listdir("input") if f.endswith(".txt")])
        self.output_files = sorted([f for f in os.listdir("output") if f.endswith(".txt")])

        # Tạo giao diện
        self.create_widgets()
        self.root.bind("<KeyPress>", self.handle_keypress)

    def load_images(self):
        # Đảm bảo ảnh có kích thước vừa với cell_size
        self.player_img = ImageTk.PhotoImage(Image.open("assets/player.png").resize((self.cell_size, self.cell_size)))
        self.stone_img = ImageTk.PhotoImage(Image.open("assets/rock.png").resize((self.cell_size, self.cell_size)))
        self.hole_img = ImageTk.PhotoImage(Image.open("assets/hole.png").resize((self.cell_size, self.cell_size)))
        self.wall_img = ImageTk.PhotoImage(Image.open("assets/wall.png").resize((self.cell_size, self.cell_size)))

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas vẽ mê cung với kích thước cố định
        self.canvas = tk.Canvas(main_frame, bg='white', width=600, height=600)  # Kích thước cố định của canvas
        self.canvas.grid(row=0, column=0, rowspan=10, sticky="nsew", padx=20, pady=20)

        # Tạo khung chứa các nút điều khiển và thông tin
        control_frame = tk.Frame(main_frame, padx=10, pady=10)
        control_frame.grid(row=0, column=1, sticky="n")

        tk.Label(control_frame, text="Select Map:").pack()
        self.map_selector = ttk.Combobox(control_frame, values=self.input_files)
        self.map_selector.pack()
        self.map_selector.bind("<<ComboboxSelected>>", self.display_selected_map)

        tk.Label(control_frame, text="Select Algorithm:").pack()
        self.algo_selector = ttk.Combobox(control_frame, values=["DFS", "BFS", "UCS", "A*"])
        self.algo_selector.pack()

        self.start_button = tk.Button(control_frame, text="Start", command=self.start_animation)
        self.start_button.pack(pady=5)
        self.pause_button = tk.Button(control_frame, text="Pause", command=self.toggle_pause)
        self.pause_button.pack(pady=5)
        self.manual_control_button = tk.Button(control_frame, text="Manual Control", command=self.enable_manual_control)
        self.manual_control_button.pack(pady=5)
        self.restart_button = tk.Button(control_frame, text="Restart", command=self.restart_game)
        self.restart_button.pack(pady=5)
        self.quit_button = tk.Button(control_frame, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=5)

        self.output_text = tk.Text(control_frame, width=40, height=10, state=tk.DISABLED)
        self.output_text.pack(pady=5)

        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

    def display_output(self, steps, weight, expanded_nodes, exec_time, memory):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Algorithm: {self.algo_selector.get()}\n")
        self.output_text.insert(tk.END, f"Steps: {steps}\n")
        self.output_text.insert(tk.END, f"Weight: {weight}\n")
        self.output_text.insert(tk.END, f"Nodes Expanded: {expanded_nodes}\n")
        self.output_text.insert(tk.END, f"Execution Time (ms): {exec_time:.2f}\n")
        self.output_text.insert(tk.END, f"Memory (MB): {memory:.2f}\n")
        self.output_text.config(state=tk.DISABLED)

    def load_maze(self, input_file, output_file):
        self.weights, self.maze = read_maze_from_file(f"input/{input_file}")
        self.path, self.steps, self.weight, self.expanded_nodes, self.exec_time, self.memory = read_path_from_file(f"output/{output_file}")

    def display_selected_map(self, event):
        input_file = self.map_selector.get()
        output_file = f"output-{input_file.split('-')[1]}"
        
        if input_file and output_file in self.output_files:
            self.load_maze(input_file, output_file)
            self.draw_maze()

    def start_animation(self):
        self.is_paused = False
        self.is_manual_control = False
        self.pause_button.config(text="Pause")
        self.manual_control_button.config(text="Manual Control")
        self.current_step = 0

        path_length = len(self.path) if self.path else 1
        self.delay = max(100, 5000 // path_length)

        # Hiển thị thông tin output chính xác từ file output
        self.display_output(self.steps, self.weight, self.expanded_nodes, self.exec_time, self.memory)

        self.move_character(0)

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_button.config(text="Continue" if self.is_paused else "Pause")
        if not self.is_paused:
            self.move_character(self.current_step)

    def enable_manual_control(self):
        self.is_manual_control = not self.is_manual_control
        self.manual_control_button.config(text="Exit Manual Control" if self.is_manual_control else "Manual Control")
        if self.is_manual_control:
            self.canvas.focus_set()

    def restart_game(self):
        # Hàm để khởi động lại trò chơi
        self.display_selected_map(None)  # Hiển thị lại bản đồ

    def draw_maze(self):
        self.canvas.delete("all")
        rows, cols = len(self.maze), len(self.maze[0])
        self.canvas.config(width=cols * self.cell_size, height=rows * self.cell_size)

        ares, stones, targets = find_positions(self.maze)

        for i, row in enumerate(self.maze):
            for j, col in enumerate(row):
                x1, y1 = j * self.cell_size, i * self.cell_size
                if col == '#':
                    self.canvas.create_image(x1, y1, anchor="nw", image=self.wall_img)
                elif col == '.':
                    self.canvas.create_image(x1, y1, anchor="nw", image=self.hole_img)

        self.ares_rect = self.canvas.create_image(ares[1] * self.cell_size, ares[0] * self.cell_size, anchor="nw", image=self.player_img)
        self.stone_rects = []
        for idx, stone in enumerate(stones):
            stone_rect = self.canvas.create_image(stone[1] * self.cell_size, stone[0] * self.cell_size, anchor="nw", image=self.stone_img)
            self.stone_rects.append(stone_rect)

        self.ares = ares
        self.stones = stones
        self.current_step = 0

    def move_character(self, step_index):
        if self.is_paused or self.is_manual_control or step_index >= len(self.path):
            return

        direction = self.path[step_index]
        dx, dy = 0, 0
        if direction.lower() == 'u': dx, dy = -1, 0
        elif direction.lower() == 'd': dx, dy = 1, 0
        elif direction.lower() == 'l': dx, dy = 0, -1
        elif direction.lower() == 'r': dx, dy = 0, 1

        new_ares = (self.ares[0] + dx, self.ares[1] + dy)

        if new_ares in self.stones:
            stone_index = self.stones.index(new_ares)
            new_stone_pos = (new_ares[0] + dx, new_ares[1] + dy)
            if self.is_valid_move(new_stone_pos) and new_stone_pos not in self.stones:
                self.stones[stone_index] = new_stone_pos
                self.canvas.coords(self.stone_rects[stone_index], new_stone_pos[1] * self.cell_size, new_stone_pos[0] * self.cell_size)
            else:
                return

        self.ares = new_ares
        self.canvas.coords(self.ares_rect, self.ares[1] * self.cell_size, self.ares[0] * self.cell_size)
        self.current_step = step_index + 1
        self.root.after(self.delay, self.move_character, self.current_step)

    def handle_keypress(self, event):
        if not self.is_manual_control:
            return

        direction = event.keysym.lower()
        dx, dy = 0, 0
        if direction == 'up': dx, dy = -1, 0
        elif direction == 'down': dx, dy = 1, 0
        elif direction == 'left': dx, dy = 0, -1
        elif direction == 'right': dx, dy = 0, 1

        new_ares = (self.ares[0] + dx, self.ares[1] + dy)

        if self.is_valid_move(new_ares):
            self.move_character_manual(new_ares, dx, dy)

    def is_valid_move(self, pos):
        x, y = pos
        return 0 <= x < len(self.maze) and 0 <= y < len(self.maze[0]) and self.maze[x][y] != '#'

    def move_character_manual(self, new_ares, dx, dy):
        if new_ares in self.stones:
            stone_index = self.stones.index(new_ares)
            new_stone_pos = (new_ares[0] + dx, new_ares[1] + dy)
            if self.is_valid_move(new_stone_pos) and new_stone_pos not in self.stones:
                self.stones[stone_index] = new_stone_pos
                self.canvas.coords(self.stone_rects[stone_index], new_stone_pos[1] * self.cell_size, new_stone_pos[0] * self.cell_size)
            else:
                return

        self.ares = new_ares
        self.canvas.coords(self.ares_rect, self.ares[1] * self.cell_size, self.ares[0] * self.cell_size)

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
