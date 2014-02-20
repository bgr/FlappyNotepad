import win32api
import win32gui
import win32con
import time
import subprocess
import random
from util import transpose, draw
import art


PIPE_HEIGHT = 49
PIPE_SPACING = 35
PIPE_GAP = 13
SCREEN_WIDTH = 80
SCREEN_HEIGHT = PIPE_HEIGHT + 4
START_SPACE = 47
LEAD_IN = 135
GRAVITY_ACCEL = -155
JUMP_ACCEL = 50
MAX_JUMP_VEL = 50
NUM_PIPES = 200
BIRD_X_POS = 4
DT = 0.033


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


def pipe_and_space(top_height=None):
    return transpose(art.pipes(PIPE_GAP, PIPE_HEIGHT, top_height)) \
        + [empty] * PIPE_SPACING


level = cur_screen_pos = bird_pos_x = bird_pos_y = bird_vel =\
    score = game_over = bird_anim_frame = None

first_run = True



was_released = True


def keycheck():
    global key_pressed, was_released
    # only register keypress the first time shift key is pressed, then ignore
    # until it's released
    shift_down = win32api.GetKeyState(win32con.VK_SHIFT) < 0  # -127 or -128
    if shift_down and was_released:
        was_released = False
        return True
    elif not shift_down:
        was_released = True
    return False



def reset():
    global level, cur_screen_pos, bird_pos_x, bird_pos_y, bird_vel,\
        score, game_over, bird_anim_frame, show_readme

    cur_screen_pos = 0
    bird_pos_x = BIRD_X_POS
    bird_pos_y = round(PIPE_HEIGHT / 2)
    bird_vel = 0
    score = 0
    game_over = False
    bird_anim_frame = 0

    # make first pipe have a gap in the middle
    middle = (PIPE_HEIGHT - PIPE_GAP) / 2
    first_pipe_top = random.randint(middle - 3, middle + 3)

    level = ([empty] * START_SPACE +
             pipe_and_space(first_pipe_top) +
             [el for _ in range(NUM_PIPES) for el in pipe_and_space()])
    level = transpose(transpose(level) + art.ground(len(level)))

    if first_run:
        # have to add empty space to the bottom of readme
        fillup = len(level[0]) - len(art.readme)

        whitespace = [' ' * len(art.readme[0])]
        readme = art.readme + whitespace * fillup

        whitespace = [' ' * len(art.logo[0])]
        logo = (whitespace * 20 +
                art.logo +
                whitespace * (SCREEN_HEIGHT - 20 - len(art.logo)))

        level = (transpose(readme) +
                 [' ' * SCREEN_HEIGHT] * 5 +
                 transpose(logo) +
                 level)
        bird_pos_x += SCREEN_WIDTH + len(logo[0]) + 7


reset()


# show first frame and wait for keypress
screen_slice = level[cur_screen_pos:cur_screen_pos + SCREEN_WIDTH]
screen = transpose(screen_slice)
data = '\r\n'.join(''.join(row) for row in screen)
set_text(text_area, data)
while not keycheck():
    print 'waiting'
    pass


while True:  # game loop
    key_pressed = keycheck()

    if key_pressed:
        if game_over:
            first_run = False
            reset()
        else:
            bird_vel += JUMP_ACCEL

    # update bird vertical velocity and position
    bird_vel = min(MAX_JUMP_VEL, bird_vel + GRAVITY_ACCEL * DT)
    bird_pos_y -= bird_vel * DT

    if (first_run and cur_screen_pos < LEAD_IN
            and bird_pos_y > PIPE_HEIGHT / 2 + 2):
        bird_vel += JUMP_ACCEL

    bird_pos_x = max(BIRD_X_POS, bird_pos_x - 1)
    bird_pos_y_int = int(round(bird_pos_y))


    # check if bird hit ground or ceiling
    if bird_pos_y_int >= PIPE_HEIGHT - 2 or bird_pos_y_int < 0:
        print 'Game Over! (out of bounds)'
        game_over = True
        bird_pos_y_int = min(PIPE_HEIGHT - 2, max(0, bird_pos_y_int))
        bird_vel = 0


    # take part of the level to display
    screen_slice = level[cur_screen_pos:cur_screen_pos + SCREEN_WIDTH]
    screen = transpose(screen_slice)

    # check if bird hit something
    if not first_run or cur_screen_pos > LEAD_IN:
        for y in range(bird_pos_y_int, bird_pos_y_int + 1):
            for x in range(bird_pos_x, bird_pos_x + 5):
                if screen[y][x] != ' ':
                    print 'Game Over! (hit pipe)'
                    game_over = True

    # draw bird
    if game_over:
        bird_anim_frame = 2
    elif cur_screen_pos % 5 == 0:
        bird_anim_frame = (bird_anim_frame + 1) % 2
    draw(screen, art.bird[bird_anim_frame], bird_pos_x, bird_pos_y_int)

    # display score
    cur_segment = max(
        0,
        (cur_screen_pos - LEAD_IN) / (art.PIPE_WIDTH + PIPE_SPACING) + 1
    )
    if cur_segment != score:
        score = cur_segment
    score_text = art.score(score)
    if not first_run or cur_screen_pos > LEAD_IN:
        draw(screen, score_text, (SCREEN_WIDTH - len(score_text[0])) / 2, 2)

    if game_over:
        draw(screen, art.game_over,
             (SCREEN_WIDTH - len(art.game_over[0])) / 2, 20)

    # render to notepad
    data = '\r\n'.join(''.join(row) for row in screen)
    set_text(text_area, data)

    # scroll level
    if not game_over:
        cur_screen_pos += 1


    if process.poll() == 0:
        print 'Notepad was closed'
        break
    elif cur_screen_pos + SCREEN_WIDTH >= len(level):
        print 'Reached end of level'
        break
    time.sleep(DT)
