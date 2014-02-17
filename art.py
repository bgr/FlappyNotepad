logo = [
    ' ____ _ ____                  ____ _        _ ',
    '|  __| |__  |____ ___ __ __  | ,  |_|--- __| |',
    '|  __| |    |    |   |  |  | |   <| | |_|    |',
    '| |  | |  , |  | |  ||  |  | | ,  | | | | |  |',
    '|_|  |_|____|  __|  _|___  | |____|_|_| |____|',
    '            |_|  |_|   |___|                  ',
]

game_over = [
    ' ___ ____        ____    ___     ____     ',
    '|  _|__  |------|  , |  |   |- -|  , |--- ',
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
    ]
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


ground = [
    ',,,,',
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
