class Maze:
    def __init__(self, grid, stones, switches, start):
        """
        Khởi tạo mê cung.
        - param grid: Ma trận mô tả mê cung.
        - param stones: Danh sách tọa độ các viên đá.
        - param switches: Danh sách tọa độ các công tắc.
        - param start: Vị trí bắt đầu của Ares.
        """
        self.grid = grid
        self.stones = stones  # Các viên đá chưa đặt lên công tắc
        self.switches = switches
        self.start = start
        self.rows = len(grid)
        self.cols = len(grid[0])

    def is_valid(self, x, y):
        # Kiểm tra xem một vị trí (x, y) có hợp lệ trong mê cung không.
        return 0 <= x < self.rows and 0 <= y < self.cols and self.grid[x][y] != '#'

    def is_stone(self, x, y):        
        # Kiểm tra xem vị trí có phải là viên đá không (bao gồm cả viên đá trên công tắc).
        return self.grid[x][y] == '$' or self.grid[x][y] == '*'

    def is_switch(self, x, y):
        # Kiểm tra xem vị trí có phải là công tắc không (bao gồm cả công tắc có Ares hoặc đá trên đó).
        return self.grid[x][y] == '.' or self.grid[x][y] == '*' or self.grid[x][y] == '+'

    def is_free(self, x, y):
        # Kiểm tra xem vị trí có phải là ô trống không (bao gồm cả công tắc không có vật).
        return self.grid[x][y] == ' ' or self.is_switch(x, y)

    def is_ares(self, x, y):     
        # Kiểm tra xem vị trí có phải là vị trí của Ares không.
        return self.grid[x][y] == '@' or self.grid[x][y] == '+'
    
    def get_stone_weight(self, x, y):
        # Trả về trọng lượng của viên đá ở vị trí (x, y). Nếu không có viên đá, trả về 0.
        for (sx, sy), weight in self.stones:
            if (sx, sy) == (x, y):
                return weight
        return 0  # Không có viên đá ở vị trí (x, y)