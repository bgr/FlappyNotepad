import win32api
import win32gui
import win32con
import time
import subprocess
from util import transpose, draw
import art


PIPE_HEIGHT = 50
PIPE_SPACING = 35
PIPE_GAP = 11
SCREEN_WIDTH = 80
SCREEN_HEIGHT = PIPE_HEIGHT + 10
START_SPACE = 47
GRAVITY_ACCEL = -160
JUMP_ACCEL = 50
MAX_JUMP_VEL = 70
NUM_PIPES = 200


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
win_height = SCREEN_HEIGHT * 14 + 40
win_x = (monitor_width - win_width) / 2
win_y = (monitor_height - win_height) / 2
win32gui.SetWindowPos(notepad, None, win_x, win_y, win_width, win_height, 0)

# notepad's text area is the first child of the window
text_area = win32gui.FindWindowEx(notepad, None, None, None)


# level data is generated transposed, then transposed again for rendering

empty = ' ' * PIPE_HEIGHT


def pipe_and_space():
    return transpose(art.pipes(PIPE_GAP, PIPE_HEIGHT)) + [empty] * PIPE_SPACING


level = [empty] * START_SPACE + [el for _ in range(NUM_PIPES)
                                 for el in pipe_and_space()]
level = transpose(transpose(level) + art.ground(len(level)))
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
    if bird_pos_y_int >= PIPE_HEIGHT - 2 or bird_pos_y_int <= 0:
        print 'Game Over! (out of bounds)'
        game_over = True
        bird_pos_y_int = min(PIPE_HEIGHT - 2, max(0, bird_pos_y_int))


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
        0,
        (cur_screen_pos - START_SPACE) / (art.PIPE_WIDTH + PIPE_SPACING) + 1
    )
    if cur_segment != score:
        score = cur_segment
        print score
    score_text = art.score(score)
    draw(transposed, score_text, (SCREEN_WIDTH - len(score_text[0])) / 2, 2)

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
