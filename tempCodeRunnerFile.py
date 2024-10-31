    def display_selected_map(self, event=None):
        input_file = self.map_selector.get()
        algo = self.algo_selector.get()  # Lấy thuật toán được chọn
        output_file = f"{algo.lower()}-{input_file.split('-')[1]}"
        
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

        # Hiển thị thông tin output chính xác từ file output cho thuật toán đã chọn
        self.display_output(self.steps, self.weight, self.expanded_nodes, self.exec_time, self.memory)

        self.move_character(0)
