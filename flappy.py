import win32api
import win32gui
import win32con
import time
import subprocess
import random


PIPE_HEIGHT = 50   # lines of text
PIPE_WIDTH = 4     # characters
PIPE_SPACING = 33  # characters
GAP_PERCENT = 0.3  # percentage of pipe height
SCROLL_SPEED = 4   # character per second
SCREEN_WIDTH = 80  # characters
GRAVITY_ACCEL = -62
JUMP_ACCEL = 32
MAX_JUMP_VEL = 40


process = subprocess.Popen('Notepad.exe')

# wait for it to open
time.sleep(1)

# find its window handle
windows = {}
enum = lambda hwnd, _: windows.update({ hwnd: win32gui.GetWindowText(hwnd)})
win32gui.EnumWindows(enum, None)

game_window = [hwnd for hwnd, title in windows.items()
               if title == 'Untitled - Notepad']

if not game_window:
    raise Exception("Notepad must be running")
if len(game_window) > 1:
    raise Exception("Multiple Notepads seem to be running")

notepad = game_window[0]


def set_text(hwnd, text):
    win32api.SendMessage(hwnd, win32con.WM_SETTEXT, 0, text)

# set window title and bring it to front
set_text(notepad, "Flappy Notepad".center(200))
win32gui.ShowWindow(notepad, win32con.SW_SHOWNORMAL)

# notepad's text area is the first child of the window
text_area = win32gui.FindWindowEx(notepad, None, None, None)

text = 'Hello Flappy World!'
set_text(text_area, text)


# level data is generated transposed, then transposed again for rendering

def pipe(gap_perc, pipe_width, pipe_height):
    top_perc = random.random() * (1 - gap_perc)
    bot_perc = (1 - top_perc - gap_perc)
    top = int(round(top_perc * pipe_height))
    gap = int(round(gap_perc * pipe_height))
    bot = int(round(bot_perc * pipe_height))
    column = ('X' * top) + (' ' * gap) + ('X' * bot)
    assert len(column) == pipe_height, (len(column), pipe_height)
    return [column] * pipe_width


empty = ' ' * PIPE_HEIGHT


def pipe_and_space():
    return pipe(GAP_PERCENT, PIPE_WIDTH, PIPE_HEIGHT) + [empty] * PIPE_SPACING


def column(grid, col_num):
    return [row[col_num] for row in grid]


def transpose(grid):
    return [column(grid, i) for i in range(len(grid[0]))]



level = [empty] * 42 + [el for _ in range(9999) for el in pipe_and_space()]
cur_screen_pos = 0
can_jump = True
bird_pos_x = 4
bird_pos_y = round(PIPE_HEIGHT / 2)
bird_vel = 0
dt = 0.033

while True:  # game loop
    shift_pressed = win32api.GetKeyState(win32con.VK_SHIFT) < 0  # -127 or -128
    if shift_pressed and can_jump:
        print 'Jump!'
        can_jump = False
        bird_vel += JUMP_ACCEL
    elif not shift_pressed:
        can_jump = True

    bird_vel = min(MAX_JUMP_VEL, bird_vel + GRAVITY_ACCEL * dt)
    bird_pos_y -= bird_vel * dt

    screen_slice = level[cur_screen_pos:cur_screen_pos + SCREEN_WIDTH]
    transposed = transpose(screen_slice)

    bird_pos_y_int = int(round(bird_pos_y))
    collider = transposed[bird_pos_y_int][bird_pos_x]

    if collider != ' ' or bird_pos_y_int >= PIPE_HEIGHT:
        print 'Game Over!'
        break

    transposed[bird_pos_y_int][bird_pos_x] = 'O'
    data = '\r\n'.join(''.join(row) for row in transposed)
    set_text(text_area, data)
    cur_screen_pos += 1


    if process.poll() == 0:
        print 'Notepad was closed'
        break
    elif cur_screen_pos + SCREEN_WIDTH >= len(level):
        print 'Reached end of level'
        break
    time.sleep(dt)
