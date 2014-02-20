def column(grid, col_num):
    return [row[col_num] for row in grid]


def transpose(grid):
    return [column(grid, i) for i in range(len(grid[0]))]


def draw(screen, data, x, y):
    for dy, row in enumerate(data, y):
        for dx, px in enumerate(row, x):
            if dy < len(screen) and dx < len(screen[dy]):
                screen[dy][dx] = px


def add_border(text, space=(1, 1)):
    sp_x, sp_y = space
    lines = text.splitlines()
    maxlen = max(len(ln) for ln in lines)
    center = [ln.center(maxlen + sp_x * 2) for ln in lines]
    width = len(center[0])
    top = [' ' + ('_' * width) + ' ']
    mid = ['|' + (' ' * width) + '|'] * sp_y
    bot = ['|' + ('_' * width) + '|']
    return top + mid + ['|{0}|'.format(ln) for ln in center] + mid[:-1] + bot
