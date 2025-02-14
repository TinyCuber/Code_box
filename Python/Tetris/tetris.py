import tkinter as tk
from tkinter import messagebox
import random

DEFAULT_FPS = 300
DEFAULT_ROWS = 20
DEFAULT_COLS = 12
cell_size = 30

SHAPES = {
    "O": [(-1, -1), (0, -1), (-1, 0), (0, 0)],
    "S": [(-1, 0), (0, 0), (0, -1), (1, -1)],
    "T": [(-1, 0), (0, 0), (0, -1), (1, 0)],
    "I": [(0, 1), (0, 0), (0, -1), (0, -2)],
    "L": [(-1, 0), (0, 0), (-1, -1), (-1, -2)],
    "J": [(-1, 0), (0, 0), (0, -1), (0, -2)],
    "Z": [(-1, -1), (0, -1), (0, 0), (1, 0)]
}

SHAPESCOLOR = {
    "O": "blue",
    "S": "red",
    "T": "yellow",
    "I": "green",
    "L": "purple",
    "J": "orange",
    "Z": "Cyan"
}


def draw_cell_by_cr(canvas, c, r, color="#CCCCCC"):
    x0 = c * cell_size
    y0 = r * cell_size
    x1 = c * cell_size + cell_size
    y1 = r * cell_size + cell_size
    canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="white", width=2)


def draw_board(canvas, block_list):
    for ri in range(len(block_list)):
        for ci in range(len(block_list[0])):
            cell_type = block_list[ri][ci]
            if cell_type:
                draw_cell_by_cr(canvas, ci, ri, SHAPESCOLOR[cell_type])
            else:
                draw_cell_by_cr(canvas, ci, ri)


def draw_cells(canvas, c, r, cell_list, color="#CCCCCC"):
    for cell in cell_list:
        cell_c, cell_r = cell
        ci = cell_c + c
        ri = cell_r + r
        if 0 <= ci < len(block_list[0]) and 0 <= ri < len(block_list):
            draw_cell_by_cr(canvas, ci, ri, color)


def draw_block_move(canvas, block, direction=[0, 0]):
    shape_type = block['kind']
    c, r = block['cr']
    cell_list = block['cell_list']

    draw_cells(canvas, c, r, cell_list)

    dc, dr = direction
    new_c, new_r = c + dc, r + dr
    block['cr'] = [new_c, new_r]
    draw_cells(canvas, new_c, new_r, cell_list, SHAPESCOLOR[shape_type])


def generate_new_block():
    kind = random.choice(list(SHAPES.keys()))
    cr = [len(block_list[0]) // 2, 0]
    new_block = {
        "kind": kind,
        "cell_list": SHAPES[kind],
        "cr": cr,
    }
    return new_block


def check_move(block, direction=[0, 0]):
    cc, cr = block['cr']
    cell_list = block['cell_list']

    for cell in cell_list:
        cell_c, cell_r = cell
        c = cell_c + cc + direction[0]
        r = cell_r + cr + direction[1]

        if c < 0 or c >= len(block_list[0]) or r >= len(block_list):
            return False

        if r >= 0 and block_list[r][c]:
            return False

    return True


def save_to_block_list(block):
    shape_type = block['kind']
    cc, cr = block['cr']
    cell_list = block['cell_list']

    for cell in cell_list:
        cell_c, cell_r = cell
        c = cell_c + cc
        r = cell_r + cr

        block_list[r][c] = shape_type


def horizontal_move_block(event):
    direction = [0, 0]
    if event.keysym == 'Left':
        direction = [-1, 0]
    elif event.keysym == 'Right':
        direction = [1, 0]
    else:
        return

    global current_block
    if current_block is not None and check_move(current_block, direction):
        draw_block_move(canvas, current_block, direction)


def rotate_block(event):
    global current_block
    if current_block is None:
        return

    cell_list = current_block['cell_list']
    rotate_list = []
    for cell in cell_list:
        cell_c, cell_r = cell
        rotate_cell = [cell_r, -cell_c]
        rotate_list.append(rotate_cell)

    block_after_rotate = {
        'kind': current_block['kind'],
        'cell_list': rotate_list,
        'cr': current_block['cr']
    }

    if check_move(block_after_rotate):
        cc, cr = current_block['cr']
        draw_cells(canvas, cc, cr, current_block['cell_list'])
        draw_cells(canvas, cc, cr, rotate_list, SHAPESCOLOR[current_block['kind']])
        current_block = block_after_rotate


def land(event):
    global current_block
    if current_block is None:
        return

    cell_list = current_block['cell_list']
    cc, cr = current_block['cr']
    min_height = len(block_list)
    for cell in cell_list:
        cell_c, cell_r = cell
        c, r = cell_c + cc, cell_r + cr
        if block_list[r][c]:
            return

        h = 0
        for ri in range(r + 1, len(block_list)):
            if block_list[ri][c]:
                break
            else:
                h += 1

        if h < min_height:
            min_height = h

    down = [0, min_height]
    if check_move(current_block, down):
        draw_block_move(canvas, current_block, down)


score = 0


def check_row_complete(row):
    for cell in row:
        if cell == '':
            return False

    return True


def check_and_clear():
    has_complete_row = False
    for ri in range(len(block_list)):
        if check_row_complete(block_list[ri]):
            has_complete_row = True
            if ri > 0:
                for cur_ri in range(ri, 0, -1):
                    block_list[cur_ri] = block_list[cur_ri - 1][:]
                block_list[0] = ['' for j in range(len(block_list[0]))]
            else:
                block_list[ri] = ['' for j in range(len(block_list[0]))]
            global score
            score += 10

    if has_complete_row:
        draw_board(canvas, block_list)
        win.title("SCORES: %s" % score)


def game_loop():
    win.update()
    global current_block
    if current_block is None:
        new_block = generate_new_block()
        draw_block_move(canvas, new_block)
        current_block = new_block
        if not check_move(current_block):
            messagebox.showinfo("Game Over!", "Your Score is %s" % score)
            restart_button.config(state=tk.NORMAL)
            return
    else:
        if check_move(current_block, [0, 1]):
            draw_block_move(canvas, current_block, [0, 1])
        else:
            save_to_block_list(current_block)
            current_block = None

    check_and_clear()

    win.after(FPS, game_loop)


def start_game():
    global FPS, R, C, block_list
    try:
        FPS = int(entry_fps.get())
        if custom_mode:
            R = int(entry_rows.get())
            C = int(entry_cols.get())
        else:
            R = DEFAULT_ROWS
            C = DEFAULT_COLS

        setting_frame.pack_forget()
        restart_button.pack()
        restart_button.config(state=tk.DISABLED)


        canvas.config(width=C * cell_size, height=R * cell_size)

        block_list = []
        for i in range(R):
            i_row = ['' for j in range(C)]
            block_list.append(i_row)
        draw_board(canvas, block_list)

        canvas.focus_set()
        current_block = None
        game_loop()
    except ValueError:
        messagebox.showerror("Wrong", "Please enter a valid integer!")


def restart_game():
    global score, block_list, current_block
    score = 0
    restart_button.config(state=tk.DISABLED)
    restart_button.pack_forget()
    setting_frame.pack(side=tk.RIGHT, padx=20)


def toggle_custom_mode():
    global custom_mode
    custom_mode = not custom_mode
    if custom_mode:
        label_rows.pack()
        entry_rows.pack()
        label_cols.pack()
        entry_cols.pack()
    else:
        label_rows.pack_forget()
        entry_rows.pack_forget()
        label_cols.pack_forget()
        entry_cols.pack_forget()


# 创建主窗口
win = tk.Tk()
win.title("SCORES: %s" % score)

# 创建一个 Frame 来包裹 Canvas，并设置边框样式
canvas_frame = tk.Frame(win, bd=8, relief=tk.GROOVE, bg="#808080")
canvas_frame.pack(side=tk.LEFT, pady=20, padx=20)

canvas = tk.Canvas(canvas_frame, width=DEFAULT_COLS * cell_size, height=DEFAULT_ROWS * cell_size, bg="white", bd=0,
                   highlightthickness=0)
canvas.pack()

# 创建设置界面
setting_frame = tk.Frame(win)
setting_frame.pack(side=tk.RIGHT, padx=20)

# FPS 设置
label_fps = tk.Label(setting_frame, text="Please enter FPS（The smaller the value, the faster it falls）：")
label_fps.pack(pady=10)
entry_fps = tk.Entry(setting_frame)
entry_fps.insert(0, DEFAULT_FPS)
entry_fps.pack(pady=5)

# 自定义模式开关
custom_mode = False
toggle_button = tk.Button(setting_frame, text="Switch(classic or customized)", command=toggle_custom_mode)
toggle_button.pack(pady=20)

# 自定义行数和列数设置（初始隐藏）
label_rows = tk.Label(setting_frame, text="Please enter the height of the game interface（lines）：")
entry_rows = tk.Entry(setting_frame)
entry_rows.insert(0, DEFAULT_ROWS)
label_cols = tk.Label(setting_frame, text="Please enter the width of the game interface（columns）：")
entry_cols = tk.Entry(setting_frame)
entry_cols.insert(0, DEFAULT_COLS)

# 开始游戏按钮
start_button = tk.Button(setting_frame, text="Start", command=start_game)
start_button.pack(pady=20)

# 创建重新开始按钮，初始时隐藏
restart_button = tk.Button(win, text="Regame", command=restart_game, state=tk.DISABLED)

block_list = []
for i in range(DEFAULT_ROWS):
    i_row = ['' for j in range(DEFAULT_COLS)]
    block_list.append(i_row)

draw_board(canvas, block_list)

current_block = None

canvas.bind("<KeyPress-Left>", horizontal_move_block)
canvas.bind("<KeyPress-Right>", horizontal_move_block)
canvas.bind("<KeyPress-Up>", rotate_block)
canvas.bind("<KeyPress-Down>", land)

win.mainloop()