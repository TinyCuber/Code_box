import tkinter as tk
from tkinter import messagebox
import random
import time
from datetime import datetime


# Define the Minesweeper game class
class Minesweeper:
    # Initialization method of the class, receiving a Tkinter root window object
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.difficulty_frame = tk.Frame(self.root)
        self.difficulty_frame.pack(pady=20)

        self.difficulties = {
            "Easy": (9, 9, 10),
            "Middle": (16, 16, 40),
            "Hard": (30, 16, 99)
        }

        for difficulty, (width, height, mines) in self.difficulties.items():
            tk.Button(self.difficulty_frame, text=difficulty, command=lambda w=width, h=height, m=mines: self.start_game(w, h, m)).pack(side=tk.LEFT, padx=10)

       
        tk.Button(self.difficulty_frame, text="Cusstomize", command=self.show_custom_dialog).pack(side=tk.LEFT, padx=10)

        
        self.current_width = None
        self.current_height = None
        self.current_mines = None
        self.current_mode = None

        
        self.history_records = []

    # Method to show a custom dialog box
    def show_custom_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Customize")

        tk.Label(dialog, text="width:").grid(row=0, column=0)
        width_entry = tk.Entry(dialog)
        width_entry.grid(row=0, column=1)

        tk.Label(dialog, text="height:").grid(row=1, column=0)
        height_entry = tk.Entry(dialog)
        height_entry.grid(row=1, column=1)

        tk.Label(dialog, text="The numbers of mines:").grid(row=2, column=0)
        mines_entry = tk.Entry(dialog)
        mines_entry.grid(row=2, column=1)

        def start_custom_game():
            try:
                width = int(width_entry.get())
                height = int(height_entry.get())
                mines = int(mines_entry.get())
                
                if 1 <= width <= 30 and 1 <= height <= 24 and 1 <= mines <= 667 and mines < width * height:
                    dialog.destroy()
                    self.start_game(width, height, mines, mode="Customize（width{}height{}mine{}）".format(width, height, mines))
                else:
                    messagebox.showerror("Input error", "Please enter a valid width（1 - 30）、height（1 - 24）and the number of mines（1 - 667 and less the the total number of squares）.")
            except ValueError:
                messagebox.showerror("Tnput error", "Please enter a valid integer.")

        tk.Button(dialog, text="Start", command=start_custom_game).grid(row=3, column=0, columnspan=2)

    # Method to start the game, receiving the width, height, number of mines, and game mode of the game area
    def start_game(self, width, height, mines, mode=None):
        self.current_width = width
        self.current_height = height
        self.current_mines = mines
        self.current_mode = mode if mode else self.get_mode_name(width, height, mines)

        self.width = width
        self.height = height
        self.mines = mines
        self.first_click = True
        self.flagged = 0
        self.start_time = None
        self.elapsed_time = 0

        for widget in self.root.winfo_children():
            if widget != self.difficulty_frame:
                widget.destroy()

        
        self.status_frame = tk.Frame(self.root, highlightbackground="gray", highlightthickness=5)  # 添加灰色粗边框
        self.status_frame.pack(pady=10)

        self.mines_label = tk.Label(self.status_frame, text=f"mine: {self.mines}")
        self.mines_label.pack(side=tk.LEFT, padx=10)

        self.game_status_label = tk.Label(self.status_frame, text="😀", font=("Arial", 20))
        self.game_status_label.pack(side=tk.LEFT, padx=20)
        
        self.game_status_label.bind("<Button-1>", self.reset_game_from_emoji)

        tk.Button(self.status_frame, text="Check the history", command=self.show_history).pack(side=tk.RIGHT, padx=10)

        self.timer_label = tk.Label(self.status_frame, text="time: 0")
        self.timer_label.pack(side=tk.LEFT, padx=10)

        
        self.game_frame = tk.Frame(self.root, highlightbackground="gray", highlightthickness=5)
        self.game_frame.pack()

        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.buttons = [[None for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.mark_status = [[0 for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                self.buttons[y][x] = tk.Button(self.game_frame, width=2, height=1, font=("Arial", 12))
                self.buttons[y][x].grid(row=y, column=x)
                self.buttons[y][x].bind("<Button-1>", lambda event, row=y, col=x: self.left_click(row, col))
                self.buttons[y][x].bind("<Button-3>", lambda event, row=y, col=x: self.right_click(row, col))

    # Method to get the game mode name based on width, height, and number of mines
    def get_mode_name(self, width, height, mines):
        for difficulty, (w, h, m) in self.difficulties.items():
            if w == width and h == height and m == mines:
                return difficulty
        return ""

    # Method to place mines, receiving the coordinates of a safe area
    def place_mines(self, safe_x, safe_y):
        safe_area = []
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx, ny = safe_x + dx, safe_y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    safe_area.append((nx, ny))

        mines_placed = 0
        while mines_placed < self.mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x, y) not in safe_area and self.board[y][x] != -1:
                self.board[y][x] = -1
                mines_placed += 1
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and self.board[ny][nx] != -1:
                            self.board[ny][nx] += 1

    # Method to handle the left mouse click event, receiving the row and column coordinates of the click
    def left_click(self, row, col):
        if self.first_click:
            self.start_time = time.time()
            self.place_mines(col, row)
            self.first_click = False
            self.update_timer()
            self.reveal_cell(row, col)
        elif self.mark_status[row][col] != 0:
            return
        elif self.board[row][col] == -1:
            self.game_over()
        else:
            self.reveal_cell(row, col)

        if self.check_win():
            self.win_game()

    # Method to handle the right mouse click event, receiving the row and column coordinates of the click
    def right_click(self, row, col):
        if self.revealed[row][col]:
            return
        current_status = self.mark_status[row][col]
        if current_status == 0:
            self.mark_status[row][col] = 1
            self.buttons[row][col].config(text="🚩")
            self.flagged += 1
        elif current_status == 1:
            self.mark_status[row][col] = 2
            self.buttons[row][col].config(text="?")
            self.flagged -= 1
        else:
            self.mark_status[row][col] = 0
            self.buttons[row][col].config(text="")

        self.mines_label.config(text=f"mine: {self.mines - self.flagged}")

    # Method to reveal the content of a cell, receiving the row and column coordinates of the cell
    def reveal_cell(self, row, col):
        if self.revealed[row][col] or self.mark_status[row][col] != 0:
            return
        self.revealed[row][col] = True
        if self.board[row][col] == 0:
            self.buttons[row][col].config(text="", bg="lightgray")
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = col + dx, row + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        self.reveal_cell(ny, nx)
        else:
            color_mapping = {
                1: "blue",
                2: "green",
                3: "red",
                4: "purple",
                5: "maroon",
                6: "turquoise",
                7: "black",
                8: "gray"
            }
            num = self.board[row][col]
            color = color_mapping.get(num, "black")
            self.buttons[row][col].config(text=str(num), bg="lightgray", fg=color)

    # Method to check if the player has won the game
    def check_win(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != -1 and not self.revealed[y][x]:
                    return False
        return True

    # Method to handle the game over situation
    def game_over(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == -1:
                    if self.mark_status[y][x] == 1:
                        self.buttons[y][x].config(text="🚩", bg="green")
                    else:
                        self.buttons[y][x].config(text="💣", bg="red")
                elif self.mark_status[y][x] == 1:
                    self.buttons[y][x].config(text="❌", bg="yellow")
        self.game_status_label.config(text="😵")
        end_time = time.time()
        elapsed_time = int(end_time - self.start_time) if self.start_time else 0
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history_records.append((timestamp, self.current_mode, elapsed_time, "lose"))
        messagebox.showinfo("Game over", "You stepped on a mine!")

    # Method to handle the situation when the player wins the game
    def win_game(self):
        self.elapsed_time = int(time.time() - self.start_time)
        self.game_status_label.config(text="😎")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history_records.append((timestamp, self.current_mode, self.elapsed_time, "win"))
        messagebox.showinfo("Victory!", f"Congratulations, you won! Time: {self.elapsed_time} s")

    # Method to update the game timer
    def update_timer(self):
        if not self.first_click:
            self.elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"time: {self.elapsed_time}")
            self.root.after(1000, self.update_timer)

    # Method to reset the game via an emoji, receiving an event object
    def reset_game_from_emoji(self, event):
        if self.current_width and self.current_height and self.current_mines:
            self.start_game(self.current_width, self.current_height, self.current_mines, mode=self.current_mode)

    # Method to reset the game
    def reset_game(self):
        self.reset_game_from_emoji(None)

    # Method to show the game history
    def show_history(self):
        history_window = tk.Toplevel(self.root, highlightbackground="gray", highlightthickness=5)  # 添加灰色粗边框
        history_window.title("History")
        history_window.geometry("600x400")

        
        canvas = tk.Canvas(history_window)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        
        scrollbar = tk.Scrollbar(history_window, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        
        canvas.configure(yscrollcommand=scrollbar.set)

        
        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor=tk.NW)

        def populate_history():
            
            for widget in frame.winfo_children():
                widget.destroy()

            
            tk.Label(frame, text="Choose", width=10).grid(row=0, column=0)
            tk.Label(frame, text="Number", width=10).grid(row=0, column=1)
            tk.Label(frame, text="Model", width=20).grid(row=0, column=2)
            tk.Label(frame, text="Time", width=20).grid(row=0, column=3)
            tk.Label(frame, text="Result", width=10).grid(row=0, column=4)

            
            check_vars = []
            for i, (timestamp, mode, elapsed_time, result) in enumerate(self.history_records, start=1):
                var = tk.IntVar()
                check_vars.append(var)
                tk.Checkbutton(frame, variable=var).grid(row=i, column=0)
                tk.Label(frame, text=str(i), width=10).grid(row=i, column=1)
                tk.Label(frame, text=mode, width=20).grid(row=i, column=2)
                tk.Label(frame, text="{} 秒".format(elapsed_time), width=20).grid(row=i, column=3)
                tk.Label(frame, text=result, width=10).grid(row=i, column=4)

            def delete_selected():
                indices_to_delete = [i for i, var in enumerate(check_vars) if var.get() == 1]
                if not indices_to_delete:
                    messagebox.showinfo("Tip", "Please select the record you want to delete.")
                    return
                confirm = messagebox.askyesno("Confirm and delete", "Are you sure you want to delete the selected history?")
                if confirm:
                    indices_to_delete.sort(reverse=True)
                    for index in indices_to_delete:
                        del self.history_records[index]
                    populate_history()

            def delete_all():
                confirm = messagebox.askyesno("Confirm and delete", "Are you sure you want to delete all the history?")
                if confirm:
                    self.history_records = []
                    populate_history()

            
            tk.Button(frame, text="Delete the selected record", command=delete_selected).grid(row=len(self.history_records) + 1, column=2)
            
            tk.Button(frame, text="Delete all", command=delete_all).grid(row=len(self.history_records) + 1, column=3)

            # 配置 Canvas 的滚动区域
            frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

        populate_history()

        # 绑定鼠标滚轮事件
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)


# Main program entry point
if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()