import tkinter as tk
import time

def read_maze_from_file(filename):
    with open(filename, 'r') as file:
        weights = list(map(int, file.readline().strip().split()))  # Đọc khối lượng từ dòng đầu tiên
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
        directions = file.readlines()[-1].strip()  # Đọc dòng cuối cùng
    return list(directions)

def draw_maze(maze, path, weights):
    root = tk.Tk()
    root.title("Maze Solver")

    cell_size = 40
    rows, cols = len(maze), len(maze[0])
    canvas = tk.Canvas(root, width=cols * cell_size, height=rows * cell_size, bg='white')
    canvas.pack()

    # Xác định tốc độ di chuyển (ms) dựa trên độ dài của đường đi
    if len(path) > 100:
        delay = 100  # Nếu đường đi dài, tăng tốc độ
    elif len(path) > 50:
        delay = 200  # Đường đi trung bình
    else:
        delay = 500  # Đường đi ngắn, tốc độ chậm

    # Vẽ mê cung ban đầu với tường, đích, và các viên đá
    ares, stones, targets = find_positions(maze)

    for i, row in enumerate(maze):
        for j, col in enumerate(row):
            x1, y1 = j * cell_size, i * cell_size
            x2, y2 = x1 + cell_size, y1 + cell_size
            if col == '#':
                canvas.create_rectangle(x1, y1, x2, y2, fill='orange')  # Tường
            elif col == '.':
                canvas.create_rectangle(x1, y1, x2, y2, fill='blue')  # Đích

    # Vẽ nhân vật và đá
    ares_rect = canvas.create_rectangle(ares[1] * cell_size, ares[0] * cell_size,
                                        (ares[1] + 1) * cell_size, (ares[0] + 1) * cell_size,
                                        fill='green')  # Nhân vật màu xanh lá
    stone_rects = []
    stone_labels = []

    # Vẽ đá với nhãn khối lượng trên mỗi viên đá
    for idx, stone in enumerate(stones):
        stone_rect = canvas.create_rectangle(stone[1] * cell_size, stone[0] * cell_size,
                                             (stone[1] + 1) * cell_size, (stone[0] + 1) * cell_size,
                                             fill='gray')  # Đá màu xám
        stone_label = canvas.create_text(stone[1] * cell_size + cell_size // 2,
                                         stone[0] * cell_size + cell_size // 2,
                                         text=str(weights[idx]), font=("Arial", 10, "bold"), fill="white")
        stone_rects.append(stone_rect)
        stone_labels.append(stone_label)

    def move_character(step_index):
        nonlocal ares, stones
        if step_index < len(path):
            direction = path[step_index]
            dx, dy = 0, 0
            if direction.lower() == 'u': dx, dy = -1, 0
            elif direction.lower() == 'd': dx, dy = 1, 0
            elif direction.lower() == 'l': dx, dy = 0, -1
            elif direction.lower() == 'r': dx, dy = 0, 1

            new_ares = (ares[0] + dx, ares[1] + dy)

            # Kiểm tra xem nhân vật có đẩy đá không
            if direction.isupper():  # Đẩy đá
                for idx, stone in enumerate(stones):
                    if stone == new_ares:
                        new_stone_pos = (stone[0] + dx, stone[1] + dy)
                        stones[idx] = new_stone_pos
                        # Cập nhật vị trí của đá và nhãn khối lượng trên canvas
                        canvas.coords(stone_rects[idx], new_stone_pos[1] * cell_size, new_stone_pos[0] * cell_size,
                                      (new_stone_pos[1] + 1) * cell_size, (new_stone_pos[0] + 1) * cell_size)
                        canvas.coords(stone_labels[idx], new_stone_pos[1] * cell_size + cell_size // 2,
                                      new_stone_pos[0] * cell_size + cell_size // 2)

            # Cập nhật vị trí nhân vật
            ares = new_ares
            canvas.coords(ares_rect, ares[1] * cell_size, ares[0] * cell_size,
                          (ares[1] + 1) * cell_size, (ares[0] + 1) * cell_size)

            # Đệ quy để tiếp tục di chuyển với độ trễ đã xác định
            root.after(delay, move_character, step_index + 1)

    # Bắt đầu di chuyển
    move_character(0)
    root.mainloop()

if __name__ == "__main__":
    # Đọc mê cung và đường đi từ file
    weights, maze = read_maze_from_file("input/input-05.txt")
    path = read_path_from_file("output/output-05.txt")

    # Vẽ mê cung và hiển thị đường đi
    draw_maze(maze, path, weights)
