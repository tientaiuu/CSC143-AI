import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import os
from PIL import Image, ImageTk  # type: ignore 

# Function to read the maze from a file
def read_maze_from_file(filename):
    with open(filename, 'r') as file:
        weights = list(map(int, file.readline().strip().split()))
        maze = [list(line.strip()) for line in file.readlines()]
    return weights, maze

# Find positions for the player, stones, and targets in the maze
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

# Read the path information from a file
def read_path_from_file(filename, algorithm):
    if not os.path.exists(filename):
        return [], 0, 0

    with open(filename, "r") as file:
        lines = file.readlines()
        start_index = -1
        for i, line in enumerate(lines):
            if line.strip().startswith(algorithm):
                start_index = i
                break

        if start_index != -1:
            try:
                info_line = lines[start_index + 1].strip()
                directions = lines[start_index + 2].strip()
                info_parts = info_line.split(", ")
                steps = int(info_parts[0].split(": ")[1])
                weight = int(info_parts[1].split(": ")[1])
                return directions, steps, weight
            except IndexError:
                return [], 0, 0
        else:
            return [], 0, 0

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Solver")
        self.root.geometry("1000x600")
        self.root.resizable(False, False)

        # Initialize attributes
        self.maze = None
        self.path = []
        self.weights = None
        self.steps = 0
        self.weight = 0
        self.current_step = 0
        self.delay = 200
        self.cell_size = 50
        self.is_paused = False
        self.is_manual_control = False

        # Create fonts
        self.title_font = tkFont.Font(family="Helvetica", size=14, weight="bold")
        self.label_font = tkFont.Font(family="Helvetica", size=12)
        self.output_font = tkFont.Font(family="Courier New", size=12)

        # Load images
        self.load_images()

        # List of input and output files
        self.input_files = sorted([f for f in os.listdir("input") if f.endswith(".txt")])

        # Create GUI widgets
        self.create_widgets()
        self.root.bind("<KeyPress>", self.handle_keypress)

    def load_images(self):
        # Load original images and resize for the maze
        self.wall_img_original = Image.open("assets/wall.png")
        self.player_img_original = Image.open("assets/player.png")
        self.stone_img_original = Image.open("assets/rock.png")
        self.hole_img_original = Image.open("assets/hole.png")
        self.resize_images(self.cell_size)

    def resize_images(self, cell_size):
        # Resize images based on the cell size
        self.wall_img = ImageTk.PhotoImage(self.wall_img_original.resize((cell_size, cell_size)))
        self.player_img = ImageTk.PhotoImage(self.player_img_original.resize((cell_size, cell_size)))
        self.stone_img = ImageTk.PhotoImage(self.stone_img_original.resize((cell_size, cell_size)))
        self.hole_img = ImageTk.PhotoImage(self.hole_img_original.resize((cell_size, cell_size)))

    def create_widgets(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas frame for maze display
        canvas_frame = tk.Frame(main_frame)
        canvas_frame.grid(row=0, column=0, sticky="nsew")
        self.canvas = tk.Canvas(canvas_frame, bg='white', width=600, height=600)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Control frame
        control_frame = tk.Frame(main_frame, padx=10, pady=10)
        control_frame.grid(row=0, column=1, sticky="nsew")

        # Map selector combobox
        tk.Label(control_frame, text="Select Map:", font=self.label_font).pack(pady=5)
        self.map_selector = ttk.Combobox(control_frame, values=self.input_files)
        self.map_selector.pack(pady=5)
        self.map_selector.bind("<<ComboboxSelected>>", self.display_selected_map)

        # Algorithm selector combobox
        tk.Label(control_frame, text="Select Algorithm:", font=self.label_font).pack(pady=5)
        self.algo_selector = ttk.Combobox(control_frame, values=["DFS", "BFS", "UCS", "A*"])
        self.algo_selector.pack(pady=5)

        # Control buttons
        button_frame = tk.Frame(control_frame)
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Start", command=self.start_animation)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.pause_button = tk.Button(button_frame, text="Pause", command=self.toggle_pause)
        self.pause_button.grid(row=0, column=1, padx=5, pady=5)

        self.restart_button = tk.Button(button_frame, text="Restart", command=self.restart_game)
        self.restart_button.grid(row=1, column=0, padx=5, pady=5)

        self.quit_button = tk.Button(button_frame, text="Quit", command=self.root.quit)
        self.quit_button.grid(row=1, column=1, padx=5, pady=5)

        # Manual control button
        self.manual_control_button = tk.Button(control_frame, text="Manual Control", command=self.enable_manual_control)
        self.manual_control_button.pack(pady=5)

        # Output text area
        self.output_text = tk.Text(control_frame, width=30, height=10, state=tk.DISABLED, font=self.output_font, wrap=tk.WORD)
        self.output_text.pack(pady=5)

    def display_output(self):
        # Display only the current step count and weight
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Steps: {self.current_step}\n")
        self.output_text.insert(tk.END, f"Weight: {self.weight}\n")
        self.output_text.config(state=tk.DISABLED)

    def load_maze(self, input_file, output_file, algorithm):
        self.weights, self.maze = read_maze_from_file(f"input/{input_file}")
        result = read_path_from_file(f"output/{output_file}", algorithm)
        if result and result[0]:  # Ensure valid path is returned
            self.path, self.steps, self.weight = result
        else:
            self.path = []

    def display_selected_map(self, event=None):
        input_file = self.map_selector.get()
        algo = self.algo_selector.get()

        if not input_file:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Error: No map selected. Please select a map file.\n")
            self.output_text.config(state=tk.DISABLED)
            return

        output_file = f"output-{input_file.split('-')[1]}"
        self.weights, self.maze = read_maze_from_file(f"input/{input_file}")
        
        if algo:
            self.load_maze(input_file, output_file, algo)
        else:
            self.path = []
        
        self.display_output()
        self.draw_maze()

    def start_animation(self):
        if not self.path:
            algo = self.algo_selector.get()
            input_file = self.map_selector.get()
            if algo and input_file:
                output_file = f"output-{input_file.split('-')[1]}"
                self.load_maze(input_file, output_file, algo)
                if not self.path:
                    self.path = []
                    print("Warning: No valid path found in output.")
        
        self.is_paused = False
        self.is_manual_control = False
        self.current_step = 0
        self.weight = 0  # Reset weight to zero at the start of animation
        self.display_output()
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
        self.display_selected_map(None)

    def draw_maze(self):
        self.canvas.delete("all")
        if not self.maze:
            return

        rows, cols = len(self.maze), len(self.maze[0])
        self.cell_size = min(600 // cols, 600 // rows)
        self.resize_images(self.cell_size)
        self.canvas.config(width=cols * self.cell_size, height=rows * self.cell_size)

        for i in range(rows + 1):
            y = i * self.cell_size
            self.canvas.create_line(0, y, cols * self.cell_size, y, fill="black", width=2)

        for j in range(cols + 1):
            x = j * self.cell_size
            self.canvas.create_line(x, 0, x, rows * self.cell_size, fill="black", width=2)

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
        self.stone_text = []

        for idx, stone in enumerate(stones):
            stone_rect = self.canvas.create_image(stone[1] * self.cell_size, stone[0] * self.cell_size, anchor="nw", image=self.stone_img)
            self.stone_rects.append(stone_rect)

            x_center = stone[1] * self.cell_size + self.cell_size // 2
            y_center = stone[0] * self.cell_size + self.cell_size // 2
            stone_weight = str(self.weights[idx])
            text_id = self.canvas.create_text(x_center, y_center, text=stone_weight, font=self.label_font, fill="white")
            self.stone_text.append(text_id)

        self.ares = ares
        self.stones = stones
        self.current_step = 0

    def move_character(self, step_index):
        if self.path is None or not self.path:
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert(tk.END, "Warning: Path is not valid or initialized.\n")
            self.output_text.config(state=tk.DISABLED)
            return

        if self.is_paused or self.is_manual_control or step_index >= len(self.path):
            return

        direction = self.path[step_index]
        dx, dy = 0, 0
        if direction.lower() == 'u': dx, dy = -1, 0
        elif direction.lower() == 'd': dx, dy = 1, 0
        elif direction.lower() == 'l': dx, dy = 0, -1
        elif direction.lower() == 'r': dx, dy = 0, 1

        new_ares = (self.ares[0] + dx, self.ares[1] + dy)

        # Check if pushing a stone and update weight
        if new_ares in self.stones:
            stone_index = self.stones.index(new_ares)
            new_stone_pos = (new_ares[0] + dx, new_ares[1] + dy)
            if self.is_valid_move(new_stone_pos) and new_stone_pos not in self.stones:
                self.stones[stone_index] = new_stone_pos
                self.canvas.coords(self.stone_rects[stone_index], new_stone_pos[1] * self.cell_size, new_stone_pos[0] * self.cell_size)
                self.canvas.coords(self.stone_text[stone_index], new_stone_pos[1] * self.cell_size + self.cell_size // 2, new_stone_pos[0] * self.cell_size + self.cell_size // 2)
                
                # Update weight with the weight of the pushed stone
                self.weight += self.weights[stone_index]
            else:
                return

        # Move player
        self.ares = new_ares
        self.canvas.coords(self.ares_rect, self.ares[1] * self.cell_size, self.ares[0] * self.cell_size)

        # Update step count and display output
        self.current_step = step_index + 1
        self.display_output()

        # Move to the next step with a delay
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
                self.canvas.coords(self.stone_text[stone_index], new_stone_pos[1] * self.cell_size + self.cell_size // 2, new_stone_pos[0] * self.cell_size + self.cell_size // 2)
                
                # Update weight when a stone is pushed manually
                self.weight += self.weights[stone_index]

        self.ares = new_ares
        self.canvas.coords(self.ares_rect, self.ares[1] * self.cell_size, self.ares[0] * self.cell_size)
        self.display_output()

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
