import asyncio
import time
import curses
import random


class EventLoopCommand():

    def __await__(self):
        return (yield self)


class Sleep(EventLoopCommand):

    def __init__(self, seconds):
        self.seconds = seconds


async def blink(canvas, row, column, symbol):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        curses.curs_set(False)
        await asyncio.sleep(0)
        await Sleep(2)
        canvas.refresh()

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)
        await Sleep(0.3)
        canvas.refresh()

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)
        await Sleep(0.5)
        canvas.refresh()

        canvas.addstr(row, column, symbol)
        await asyncio.sleep(0)
        await Sleep(0.3)
        canvas.refresh()


def draw(canvas):
    symbol = '+*.:'
    x, y = window.getmaxyx()
    coroutines = [
        blink(canvas, row=random.randint(0, x - 1), column=random.randint(0, y - 1), symbol=random.choice(symbol)) for _
        in range(200)]

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
            if len(coroutines) == 0:
                break
        time.sleep(0.5)


if __name__ == '__main__':
    curses.update_lines_cols()
    window = curses.initscr()
    curses.wrapper(draw)
    curses.curs_set(False)
