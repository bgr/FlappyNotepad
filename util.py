def column(grid, col_num):
    return [row[col_num] for row in grid]


def transpose(grid):
    return [column(grid, i) for i in range(len(grid[0]))]


def draw(screen, data, x, y, transparent=True):
    for dy, row in enumerate(data, y):
        for dx, px in enumerate(row, x):
            if not transparent or px  != ' ':
                screen[dy][dx] = px


def add_border(text, space=(1, 1)):
    sp_x, sp_y = space
    center = '{space}{text}{space}'.format(space=(' ' * sp_x), text=text)
    top = [' ' + ('_' * len(center)) + ' ']
    mid = ['|' + (' ' * len(center)) + '|'] * sp_y
    bot = [' ' + (chr(175) * len(center)) + ' ']
    return top + mid + ['|{0}|'.format(center)] + mid + bot
