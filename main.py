import asyncio
import time
import curses
import random
from load_img import load_img
from itertools import cycle

SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


async def blink(canvas, row, column, symbol):
    for _ in range(0, random.randint(1, 5)):
        await asyncio.sleep(0)
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        curses.curs_set(False)
        for _ in range(0, 2):
            await asyncio.sleep(0)
            canvas.refresh()

        canvas.addstr(row, column, symbol)
        for _ in range(0, 1):
            await asyncio.sleep(0)
            canvas.refresh()

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for _ in range(0, 2):
            await asyncio.sleep(0)
            canvas.refresh()

        canvas.addstr(row, column, symbol)
        for _ in range(0, 1):
            await asyncio.sleep(0)
            canvas.refresh()


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


def read_controls(canvas):
    """Read keys pressed and returns tuple witl controls state."""

    rows_direction = columns_direction = 0
    space_pressed = False
    window.nodelay(True)

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed


def draw_frame(canvas, text, start_row=5, start_column=35, negative=False):
    """Draw multiline text fragment on canvas, erase text instead of drawing if negative=True is specified."""
    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue
        if row >= rows_number:
            break
        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue
            if column >= columns_number:
                break
            if symbol == ' ':
                continue
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


async def animate_spaceship(canvas, images):
    for item in cycle(images):
        draw_frame(canvas=canvas, text=item,
                   negative=False)
        await asyncio.sleep(0)
        canvas.refresh()
        draw_frame(canvas=canvas, text=item,
                   negative=True)


def draw(canvas):
    img_1 = load_img('rocket_frame_1.txt')
    img_2 = load_img('rocket_frame_2.txt')
    images = [img_1, img_2]

    symbol = '+*.:'
    x, y = window.getmaxyx()

    coroutines = [
        blink(canvas, row=random.randint(0, x - 1), column=random.randint(0, y - 1), symbol=random.choice(symbol)) for
        _
        in range(50)]

    coroutines.append(animate_spaceship(canvas=canvas, images=images))

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
                break
        time.sleep(0.2)


if __name__ == '__main__':
    curses.update_lines_cols()
    window = curses.initscr()
    window.nodelay(True)
    curses.wrapper(draw)
    curses.curs_set(False)
