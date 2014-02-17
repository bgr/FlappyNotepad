import win32api
import win32gui
import win32con
import time
import subprocess
import random
import art
from util import transpose, draw, add_border


PIPE_HEIGHT = 50    # lines of text
PIPE_WIDTH = 4      # characters
PIPE_SPACING = 33   # characters
GAP_PERCENT = 0.22  # percentage of pipe height
SCREEN_WIDTH = 80   # characters
START_SPACE = 42    # characters
GRAVITY_ACCEL = -66
JUMP_ACCEL = 32
MAX_JUMP_VEL = 40
NUM_PIPES = 9999


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
#if len(game_window) > 1:
    #raise Exception("Multiple Notepads seem to be running")

notepad = game_window[0]


def set_text(hwnd, text):
    win32api.SendMessage(hwnd, win32con.WM_SETTEXT, 0, text)

# set window title, bring it to front
set_text(notepad, "Flappy - Notepad")
win32gui.ShowWindow(notepad, win32con.SW_SHOWNORMAL)
# resize and center
monitor_width = win32api.GetSystemMetrics(0)
monitor_height = win32api.GetSystemMetrics(1)
win_width = SCREEN_WIDTH * 8 + 30
win_height = PIPE_HEIGHT * 14 + 40
win_x = (monitor_width - win_width) / 2
win_y = (monitor_height - win_height) / 2
win32gui.SetWindowPos(notepad, None, win_x, win_y, win_width, win_height, 0)

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


level = [empty] * START_SPACE + [el for _ in range(NUM_PIPES)
                                 for el in pipe_and_space()]
cur_screen_pos = 0
can_jump = True
bird_pos_x = 4
bird_pos_y = round(PIPE_HEIGHT / 2)
bird_vel = 0
dt = 0.033
score = 0
game_over = False
bird_anim_frame = 0


while not game_over:  # game loop
    # jumping, only apply when key is pressed, then ignore until released
    shift_pressed = win32api.GetKeyState(win32con.VK_SHIFT) < 0  # -127 or -128
    if shift_pressed and can_jump:
        can_jump = False
        bird_vel += JUMP_ACCEL
    elif not shift_pressed:
        can_jump = True

    # update bird vertical velocity and position
    bird_vel = min(MAX_JUMP_VEL, bird_vel + GRAVITY_ACCEL * dt)
    bird_pos_y -= bird_vel * dt

    bird_pos_y_int = int(round(bird_pos_y))

    # check if bird hit ground or ceiling
    if bird_pos_y_int >= PIPE_HEIGHT or bird_pos_y_int <= 0:
        print 'Game Over! (out of bounds)'
        game_over = True
        bird_pos_y_int = min(PIPE_HEIGHT - 1, max(0, bird_pos_y_int))


    # take part of the level to display
    screen_slice = level[cur_screen_pos:cur_screen_pos + SCREEN_WIDTH]
    transposed = transpose(screen_slice)

    collider = transposed[bird_pos_y_int][bird_pos_x]

    # check if bird hit something
    if collider != ' ':
        print 'Game Over! (hit pipe)'
        game_over = True

    # draw bird
    if cur_screen_pos % 5 == 0:
        bird_anim_frame = (bird_anim_frame + 1) % 2
    draw(transposed, art.bird[bird_anim_frame], bird_pos_x, bird_pos_y_int)

    # display score
    cur_segment = max(
        0, (cur_screen_pos - START_SPACE) / (PIPE_WIDTH + PIPE_SPACING) + 1)
    if cur_segment != score:
        score = cur_segment
        print score
    score_text = add_border('Score: {}'.format(str(score).zfill(4)))
    draw(transposed, score_text,
         SCREEN_WIDTH - len(score_text[0]) - 5, 2, False)

    # render to notepad
    data = '\r\n'.join(''.join(row) for row in transposed)
    set_text(text_area, data)

    # scroll level
    cur_screen_pos += 1


    if process.poll() == 0:
        print 'Notepad was closed'
        break
    elif cur_screen_pos + SCREEN_WIDTH >= len(level):
        print 'Reached end of level'
        break
    time.sleep(dt)
