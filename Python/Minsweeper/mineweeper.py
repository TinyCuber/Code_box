import tkinter as tk
from tkinter import messagebox
import random
import time

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Mineseeper")
        self.difficulty_frame = tk.Frame(self.root)
        self.difficulty_frame.pack(pady=20)

        self.difficulties = {
            "easy": (9, 9, 10),
            "middle": (16, 16, 40),
            "hard": (30, 16, 99)
        }

        for difficulty, (width, height, mines) in self.difficulties.items():
            tk.Button(self.difficulty_frame, text=difficulty, command=lambda w=width, h=height, m=mines: self.start_game(w, h, m)).pack(side=tk.LEFT, padx=10)

    def start_game(self, width, height, mines):
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

        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack()

        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(pady=10)

        self.mines_label = tk.Label(self.status_frame, text=f"mine: {self.mines}")
        self.mines_label.pack(side=tk.LEFT, padx=10)

        self.timer_label = tk.Label(self.status_frame, text="time: 0")
        self.timer_label.pack(side=tk.LEFT, padx=10)

        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.buttons = [[None for _ in range(width)] for _ in range(height)]
        self.revealed = [[False for _ in range(width)] for _ in range(height)]
        self.flagged_cells = [[False for _ in range(width)] for _ in range(height)]

        for y in range(height):
            for x in range(width):
                self.buttons[y][x] = tk.Button(self.game_frame, width=2, height=1, font=("Arial", 12))
                self.buttons[y][x].grid(row=y, column=x)
                self.buttons[y][x].bind("<Button-1>", lambda event, row=y, col=x: self.left_click(row, col))
                self.buttons[y][x].bind("<Button-3>", lambda event, row=y, col=x: self.right_click(row, col))

    def place_mines(self, safe_x, safe_y):
        mines_placed = 0
        while mines_placed < self.mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if (x != safe_x or y != safe_y) and self.board[y][x] != -1:
                self.board[y][x] = -1
                mines_placed += 1
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and self.board[ny][nx] != -1:
                            self.board[ny][nx] += 1

    def left_click(self, row, col):
        if self.first_click:
            self.start_time = time.time()
            self.place_mines(col, row)
            self.first_click = False
            self.update_timer()

        if self.flagged_cells[row][col]:
            return

        if self.board[row][col] == -1:
            self.game_over()
        else:
            self.reveal_cell(row, col)
            if self.check_win():
                self.win_game()

    def right_click(self, row, col):
        if not self.revealed[row][col]:
            if self.flagged_cells[row][col]:
                self.flagged_cells[row][col] = False
                self.flagged -= 1
                self.buttons[row][col].config(text="")
            else:
                self.flagged_cells[row][col] = True
                self.flagged += 1
                self.buttons[row][col].config(text="⚑")
            self.mines_label.config(text=f"mine: {self.mines - self.flagged}")

    def reveal_cell(self, row, col):
        if self.revealed[row][col] or self.flagged_cells[row][col]:
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
            self.buttons[row][col].config(text=str(self.board[row][col]), bg="lightgray")

    def check_win(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != -1 and not self.revealed[y][x]:
                    return False
        return True

    def game_over(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == -1:
                    self.buttons[y][x].config(text="*", bg="red")
        messagebox.showinfo("game over", "you stepped the mine！")
        self.reset_game()

    def win_game(self):
        self.elapsed_time = int(time.time() - self.start_time)
        messagebox.showinfo("game over", f"congratulations,you win！time: {self.elapsed_time} s")
        self.reset_game()

    def update_timer(self):
        if not self.first_click:
            self.elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"time: {self.elapsed_time}")
            self.root.after(1000, self.update_timer)

    def reset_game(self):
        for widget in self.root.winfo_children():
            if widget != self.difficulty_frame:
                widget.destroy()
        self.__init__(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()