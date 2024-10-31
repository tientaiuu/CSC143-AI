import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
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

def read_path_from_file(filename, algorithm):
    with open(filename, "r") as file:
        lines = file.readlines()
        start_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith(algorithm):
                start_index = i
                break

        if start_index != -1:  # Found the algorithm section
            try:  # Use a try-except block for robust error handling
                info_line = lines[start_index + 1].strip()
                directions = lines[start_index + 2].strip()
                info_parts = info_line.split(", ")
                steps = int(info_parts[0].split(": ")[1])
                weight = int(info_parts[1].split(": ")[1])
                nodes = int(info_parts[2].split(": ")[1])
                exec_time = float(info_parts[3].split(": ")[1])
                memory = float(info_parts[4].split(": ")[1])
                return directions, steps, weight, nodes, exec_time, memory
            except IndexError:  # Handle cases where file format is incorrect
                print(f"Error: Invalid output file format for algorithm {algorithm}")
                return [], 0, 0, 0, 0.0, 0.0  # Return default values if parsing fails
        else:
            print(f"Error: Algorithm {algorithm} not found in output file.")
            return [], 0, 0, 0, 0.0, 0.0 # Return defaults if algorithm isn't foun

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
        self.delay = 200
        self.cell_size = 50
        self.is_paused = False
        self.is_manual_control = False

        # font chữ
        self.title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=12)
        self.output_font = tkFont.Font(family="Courier New", size=12)  # Monospaced for output

        # Tải ảnh
        self.load_images()

        # Tạo danh sách các file input và output
        self.input_files = sorted([f for f in os.listdir("input") if f.endswith(".txt")])
        self.output_files = sorted([f for f in os.listdir("output") if f.endswith(".txt")])

        # Tạo giao diện
        self.create_widgets()
        self.root.bind("<KeyPress>", self.handle_keypress)
        
    def load_images(self):
        # Đảm bảo tất cả hình ảnh có kích thước chính xác với ô (cell_size)
        self.wall_img_original = Image.open("assets/wall.png")
        self.player_img_original = Image.open("assets/player.png")
        self.stone_img_original = Image.open("assets/rock.png")
        self.hole_img_original = Image.open("assets/hole.png")

        # Khởi tạo các ảnh theo cell_size mặc định, sẽ được điều chỉnh trong draw_maze nếu cần
        self.cell_size = 50  # Giá trị mặc định, sẽ được điều chỉnh dựa trên kích thước mê cung
        self.resize_images(self.cell_size)
        
    def resize_images(self, cell_size):
        # Điều chỉnh tất cả hình ảnh theo kích thước ô
        self.wall_img = ImageTk.PhotoImage(self.wall_img_original.resize((cell_size, cell_size)))
        self.player_img = ImageTk.PhotoImage(self.player_img_original.resize((cell_size, cell_size)))
        self.stone_img = ImageTk.PhotoImage(self.stone_img_original.resize((cell_size, cell_size)))
        self.hole_img = ImageTk.PhotoImage(self.hole_img_original.resize((cell_size, cell_size)))

    def create_widgets(self):
        # Tạo khung chính
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Tạo khung vẽ mê cung
        canvas_frame = tk.Frame(main_frame)
        canvas_frame.grid(row=0, column=0, sticky="nsew")
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)

        # Tạo canvas vẽ mê cung
        self.canvas = tk.Canvas(canvas_frame, bg='white', width=600, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Tạo khung điều khiển
        control_frame = tk.Frame(main_frame, padx=10, pady=10)
        control_frame.grid(row=0, column=1, sticky="nsew")
        control_frame.grid_rowconfigure(0, weight=1)
        control_frame.grid_columnconfigure(0, weight=1)
 
        # Label và Combobox chọn thuật toán
        tk.Label(control_frame, text="Select Algorithm:", font=self.label_font).pack(pady=5)
        self.algo_selector = ttk.Combobox(control_frame, values=["DFS", "BFS", "UCS", "A*"])
        self.algo_selector.pack(pady=5)

        # Label và Combobox chọn mê cung
        tk.Label(control_frame, text="Select Map:", font=self.label_font).pack(pady=5)
        self.map_selector = ttk.Combobox(control_frame, values=self.input_files)
        self.map_selector.pack(pady=5)
        self.map_selector.bind("<<ComboboxSelected>>", self.display_selected_map)

        # Tạo khung chứa các nút điều khiển
        button_frame = tk.Frame(control_frame)
        button_frame.pack(pady=10)

        # Nút "Start"
        self.img = Image.open("assets/play_button.png").resize((100, 100))
        self.photo = ImageTk.PhotoImage(self.img)
        self.start_button = tk.Button(
            button_frame,
            image=self.photo,
            command=self.start_animation,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            padx=0,
            pady=0
        )
        self.start_button.image = self.photo
        self.start_button.grid(row=0, column=0, padx=10, pady=5)

        # Nút "Pause"
        self.pause_img = Image.open("assets/button_pause.png").resize((70, 70))
        self.pause_photo = ImageTk.PhotoImage(self.pause_img)
        self.pause_button = tk.Button(
            button_frame,
            image=self.pause_photo,
            command=self.toggle_pause,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            padx=0,
            pady=0
        )
        self.pause_button.image = self.pause_photo
        self.pause_button.grid(row=0, column=1, padx=10, pady=5)

        # Nút "Restart"
        self.restart_img = Image.open("assets/button_restart.png").resize((70, 70))
        self.restart_photo = ImageTk.PhotoImage(self.restart_img)
        self.restart_button = tk.Button(
            button_frame,
            image=self.restart_photo,
            command=self.restart_game,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            padx=0,
            pady=0
        )
        self.restart_button.image = self.restart_photo
        self.restart_button.grid(row=1, column=0, padx=10, pady=5)

        # Nút "Quit"
        self.quit_img = Image.open("assets/button_quit.png").resize((70, 70))
        self.quit_photo = ImageTk.PhotoImage(self.quit_img)
        self.quit_button = tk.Button(
            button_frame,
            image=self.quit_photo,
            command=self.root.quit,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            padx=0,
            pady=0
        )
        self.quit_button.image = self.quit_photo
        self.quit_button.grid(row=1, column=1, padx=10, pady=5)

        # Nút "Manual Control"
        self.manual_control_button = tk.Button(control_frame, text="Manual Control", font=self.label_font, command=self.enable_manual_control)
        self.manual_control_button.pack(pady=5)

        # Text area hiển thị thông tin
        self.output_text = tk.Text(control_frame, width=30, height=10, state=tk.DISABLED, font=self.output_font, wrap=tk.WORD)
        self.output_text.pack(pady=5)

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

    def load_maze(self, input_file, output_file, algorithm):  # Add algorithm argument
        self.weights, self.maze = read_maze_from_file(f"input/{input_file}")
        self.path, self.steps, self.weight, self.expanded_nodes, self.exec_time, self.memory = read_path_from_file(f"output/{output_file}", algorithm)  # Pass algorithm

    def display_selected_map(self, event=None):
        input_file = self.map_selector.get()
        algo = self.algo_selector.get()

        #Clear only if necessary (e.g., switching maps/algorithms)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)  # Disable editing after clearing


        if not input_file:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "Please select a map file.\n")
            self.output_text.config(state=tk.DISABLED)
        elif not algo:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "Please select an algorithm.\n")
            self.output_text.config(state=tk.DISABLED)
        #  Load and display only if BOTH algorithm and map are selected
        elif input_file and algo and os.path.exists(f"output/output-{input_file.split('-')[1]}"):
            output_file = f"output-{input_file.split('-')[1]}"
            self.load_maze(input_file, output_file, algo)  # Load data
            self.draw_maze() # Clear the canvas completely before drawing anything new
            self.display_output(self.steps, self.weight, self.expanded_nodes, self.exec_time, self.memory) # Display relevant data 
        else:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, f"Output not available for {algo} on {input_file}.\n")
            self.output_text.config(state=tk.DISABLED) 

    def start_animation(self):
        self.is_paused = False
        self.is_manual_control = False
        self.pause_button.config(text="Pause")
        self.manual_control_button.config(text="Manual Control")
        self.current_step = 0

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

        # Tính toán kích thước của từng ô sao cho vừa khít với khung canvas
        self.cell_size = min(600 // cols, 600 // rows)
        self.resize_images(self.cell_size)  # Điều chỉnh kích thước ảnh theo cell_size mới
        self.canvas.config(width=cols * self.cell_size, height=rows * self.cell_size)

        # Vẽ đường viền của lưới
        for i in range(rows + 1):
            y = i * self.cell_size
            self.canvas.create_line(0, y, cols * self.cell_size, y, fill="black", width=2)  # Đường ngang

        for j in range(cols + 1):
            x = j * self.cell_size
            self.canvas.create_line(x, 0, x, rows * self.cell_size, fill="black", width=2)  # Đường dọc

        # Định vị trí của người chơi (Ares), đá, và các mục tiêu
        ares, stones, targets = find_positions(self.maze)

        # Vẽ các phần tử của mê cung
        for i, row in enumerate(self.maze):
            for j, col in enumerate(row):
                x1, y1 = j * self.cell_size, i * self.cell_size
                if col == '#':
                    self.canvas.create_image(x1, y1, anchor="nw", image=self.wall_img)  # Vẽ tường
                elif col == '.':
                    self.canvas.create_image(x1, y1, anchor="nw", image=self.hole_img)  # Vẽ mục tiêu

        # Vẽ người chơi (Ares) và các viên đá
        self.ares_rect = self.canvas.create_image(ares[1] * self.cell_size, ares[0] * self.cell_size, anchor="nw", image=self.player_img)
        self.stone_rects = []
        self.stone_text = []

        for idx, stone in enumerate(stones):
            # Vẽ viên đá
            stone_rect = self.canvas.create_image(stone[1] * self.cell_size, stone[0] * self.cell_size, anchor="nw", image=self.stone_img)
            self.stone_rects.append(stone_rect)

            # Hiển thị trọng lượng của viên đá
            x_center = stone[1] * self.cell_size + self.cell_size // 2
            y_center = stone[0] * self.cell_size + self.cell_size // 2
            stone_weight = str(self.weights[idx])
            text_id = self.canvas.create_text(x_center, y_center, text=stone_weight, font=self.label_font, fill="white")
            self.stone_text.append(text_id)

        # Cập nhật trạng thái
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

                # Move the stone image
                self.canvas.coords(self.stone_rects[stone_index], new_stone_pos[1] * self.cell_size, new_stone_pos[0] * self.cell_size)
                # Move the stone weight text
                self.canvas.coords(self.stone_text[stone_index], new_stone_pos[1] * self.cell_size + self.cell_size // 2, new_stone_pos[0] * self.cell_size + self.cell_size // 2)
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

                 # Move the stone image
                self.canvas.coords(self.stone_rects[stone_index], new_stone_pos[1] * self.cell_size, new_stone_pos[0] * self.cell_size)
                # Move the stone weight text
                self.canvas.coords(self.stone_text[stone_index], new_stone_pos[1] * self.cell_size + self.cell_size // 2, new_stone_pos[0] * self.cell_size + self.cell_size // 2)
            else:
                return

        self.ares = new_ares
        self.canvas.coords(self.ares_rect, self.ares[1] * self.cell_size, self.ares[0] * self.cell_size)

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()