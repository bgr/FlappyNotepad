logo = [
    ' ____ _ ____                  _  _     _  ____      ____    _ ',
    '|  __l l__  l____ ___ __ __  | \| l___| l|  , l____|__  l__| l',
    '|  __l |    |    l   l  l  l |    |   |  l    |    l    |    |',
    '| |  | |  , |  | |  ||  |  | |    | | | |_  __|  | |  , | |  |',
    '|_|  |_|____|  __|  _|___  | |_|\_|___|___l___|  __|____|____|',
    '            |_|  |_|   |___|                  |_|             ',
    '                                                              ',
    '                      TAP THAT SHIFT                          ',
]

game_over = [
    ' ___ ____        ____    ___     ____     ',
    '|  _l__  l------|  , l  |   l- -|  , l--- ',
    '| | |    | ,  , |    |  | | | | |    | |_|',
    '| | |  , | |  | |  __|  | | | ` |  __| |  ',
    '|___|____|_|__|_|____|  |___|\_/|____|_|  ',
]

bird = [
    [
        '/( ,)',
        '^_===',
    ],
    [
        '/( ,)',
        'V_===',
    ],
    [
        '/( x)',
        '<_==<',
    ],
]


digits = [
    [
        ' ___ ',
        '|   |',
        '| | |',
        '|___|',
    ],
    [
        '  _ ',
        ' | |',
        ' | |',
        ' |_|',
    ],
    [
        ' ___ ',
        '|_  |',
        '|  _|',
        '|___|',
    ],
    [
        ' ___ ',
        '|_  |',
        '|_  |',
        '|___|',
    ],
    [
        ' ___ ',
        '| | |',
        '|_  |',
        '  |_|',
    ],
    [
        ' ___ ',
        '|  _|',
        '|_  |',
        '|___|',
    ],
    [
        ' ___ ',
        '|  _|',
        '| . |',
        '|___|',
    ],
    [
        ' ___ ',
        '|_  |',
        '  | |',
        '  |_|',
    ],
    [
        ' ___ ',
        '| . |',
        '| . |',
        '|___|',
    ],
    [
        ' ___ ',
        '| . |',
        '|_  |',
        '|___|',
    ]
]


ground_segment = [
    '----',
    '    ',
    '//  ',
    '====',
]

pipe_top = [
    ' |. ===%1%#| ',
    '[. =====%1%#]',
    '|. =====%1%#|',
    ' ``````````` ',
]

pipe_bottom = [
    ' ___________ ',
    '|. =====%1%#|',
    '[. =====%1%#]',
    ' |. ===%1%#| ',
]



# extend pipes
pipe_top = [pipe_top[0]] * 80 + pipe_top[1:]
pipe_bottom = pipe_bottom[:-1] + [pipe_bottom[-1]] * 80
PIPE_WIDTH = len(pipe_top[0])

import random


def pipe_top_slice(height):
    assert height >= 0
    if height == 0:
        return [' ' * PIPE_WIDTH]  # spaces instead of last line of pipe
    l = len(pipe_top)
    return pipe_top[l - height - 1:]


def pipe_bottom_slice(height):
    assert height >= 0
    if height == 0:
        return [' ' * PIPE_WIDTH]
    return pipe_bottom[:height + 1]


def pipes(gap_width, column_height, top_height=None):
    max_top_height = column_height - gap_width - 1
    if top_height is None:
        top_height = random.randint(0, max_top_height)
    assert top_height <= max_top_height
    top = pipe_top_slice(top_height)
    gap = [' ' * PIPE_WIDTH] * (gap_width - 1)  # pipe end lines count as gap
    bot = pipe_bottom_slice(column_height - len(top) - len(gap) - 1)
    column = top + gap + bot
    assert len(column) == column_height, (len(column), column_height)
    return column


from util import transpose


def score(num):
    digs = [transpose(digits[int(d)]) for d in str(num)]
    return transpose([col for dig in digs for col in dig])


def ground(length):
    one = transpose(ground_segment)
    many = one * (length / len(one) + 1)
    assert len(many) >= length
    return transpose(many[:length])


readme = \
"""Flappy Notepad - Readme
=======================

               YOU MUST DO THIS TO PLAY:

1. disable Format > Word Wrap
2. set font back to default (Format > Font, Lucida Console - Regular - 10)


when you're done with that, press "Shift" on your keyboard



FAQ
===

Q: game flickers too much!
A: try disabling fancy Windows effects - open Run menu (press Win+R on keyboard)
   type in "net stop uxsms", then when you're done playing do "net start uxsms"

Q: how do I take a screenshot of the game?
A: press Ctrl-A, then Ctrl-C


Credits
=======

inspired by Flappy Bird
made during Flappy Jam (http://itch.io/jam/flappyjam)
code at https://github.com/bgr/FlappyNotepad
by bgr"""

readme = [ln.ljust(80) for ln in readme.splitlines()]
