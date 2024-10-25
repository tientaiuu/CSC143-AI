import tkinter as tk
from maze import Maze

class MazeApp:
    def __init__(self, root, maze, solution_path, total_weight):
        self.root = root
        self.maze = maze
        self.solution_path = solution_path
        self.total_weight = total_weight
        self.grid_size = 30
        self.canvas = tk.Canvas(root, width=self.maze.cols * self.grid_size, height=self.maze.rows * self.grid_size)
        self.canvas.pack()

        # Thông tin thống kê
        self.steps = 0
        self.weight_pushed = 0
        self.current_index = 0
        self.ares_position = self.maze.start
        
        # Thông tin thống kê trên GUI
        self.info_label = tk.Label(root, text=f"Steps: {self.steps}  Weight Pushed: {self.weight_pushed}")
        self.info_label.pack()

        # Bắt đầu vẽ mê cung và chạy animation
        self.draw_maze()
        self.animate()

    def draw_maze(self):
        self.canvas.delete("all")
        for i in range(self.maze.rows):
            for j in range(self.maze.cols):
                color = 'black'
                if self.maze.grid[i][j] == '#':
                    color = 'white'
                elif self.maze.grid[i][j] == '$':
                    color = 'grey'
                elif self.maze.grid[i][j] == '.':
                    color = 'yellow'
                elif (i, j) == self.ares_position:
                    color = 'blue'
                elif self.maze.grid[i][j] == '*':
                    color = 'orange'
                elif self.maze.grid[i][j] == '+':
                    color = 'cyan'
                self.canvas.create_rectangle(j * self.grid_size, i * self.grid_size,
                                             (j + 1) * self.grid_size, (i + 1) * self.grid_size,
                                             fill=color, outline='black')

    def move(self, direction):
        x, y = self.ares_position
        dx, dy = 0, 0

        # Xác định hướng di chuyển
        if direction == 'u':
            dx, dy = -1, 0
        elif direction == 'd':
            dx, dy = 1, 0
        elif direction == 'l':
            dx, dy = 0, -1
        elif direction == 'r':
            dx, dy = 0, 1

        new_x, new_y = x + dx, y + dy

        # Kiểm tra xem Ares có thể di chuyển không
        if self.maze.is_valid(new_x, new_y):
            self.ares_position = (new_x, new_y)
            self.steps += 1  # Tăng số bước di chuyển

    def push(self, direction):
        x, y = self.ares_position
        dx, dy = 0, 0

        # Xác định hướng đẩy đá
        if direction == 'U':
            dx, dy = -1, 0
        elif direction == 'D':
            dx, dy = 1, 0
        elif direction == 'L':
            dx, dy = 0, -1
        elif direction == 'R':
            dx, dy = 0, 1

        stone_x, stone_y = x + dx, y + dy
        new_stone_x, new_stone_y = stone_x + dx, stone_y + dy

        # Kiểm tra nếu đá có thể được đẩy và di chuyển Ares
        if self.maze.is_stone(stone_x, stone_y) and self.maze.is_valid(new_stone_x, new_stone_y):
            # Di chuyển viên đá
            self.maze.grid[stone_x][stone_y] = ' '  # Xóa đá ở vị trí cũ
            self.maze.grid[new_stone_x][new_stone_y] = '$'  # Đặt đá ở vị trí mới
            self.ares_position = (stone_x, stone_y)  # Cập nhật vị trí của Ares
            self.steps += 1  # Tăng số bước
            self.weight_pushed += self.maze.get_stone_weight(stone_x, stone_y)  # Cập nhật trọng lượng đã đẩy

    def update_info_label(self):
        # Cập nhật thông tin thống kê
        self.info_label.config(text=f"Steps: {self.steps}  Weight Pushed: {self.weight_pushed}")

    def animate(self):
        if self.current_index < len(self.solution_path):
            move = self.solution_path[self.current_index]
            if move in 'udlr':  # Di chuyển Ares
                self.move(move)
            elif move in 'UDLR':  # Đẩy đá
                self.push(move)

            # Vẽ lại mê cung với vị trí mới
            self.draw_maze()
            self.update_info_label()
            self.current_index += 1
            self.root.after(300, self.animate)  # Cập nhật mỗi 300ms
        else:
            print("Completed")

# Hàm khởi chạy GUI từ main
def run_gui(maze, solution_path, total_weight):
    root = tk.Tk()
    app = MazeApp(root, maze, solution_path, total_weight)
    root.mainloop()
