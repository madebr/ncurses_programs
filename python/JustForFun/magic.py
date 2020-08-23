#!/usr/bin/env python

import curses
import sys

STARTX = 9
STARTY = 3
WIDTH  = 6
HEIGHT = 4

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <magic square order>\n".format(sys.argv[0]))
        sys.exit(1)
    try:
        n = int(sys.argv[1])
        if n % 2 == 0:
            raise ValueError
    except:
        sys.stderr.write("Sorry !!! I don't know how to create magic square of even order\n")
        sys.stderr.wriet("The order should be an odd number\n")
        sys.exit(1)

    a = magic(n)
    
    stdscr = curses.initscr()
    curses.curs_set(0)
    curses.noecho()
    magic_board(stdscr, a, n)
    stdscr.getch()
    curses.endwin()


def magic(n):
    a = [[-1 for _ in range (n)] for _ in range(n)]
    
    row = 0
    col = n / 2

    k = 1
    a[row][col] = k
    
    while k != n * n:
        k += 1
        if row == 0 and col != n - 1:
            row = n - 1
            col += 1
            a[row][col] = k
        elif row != 0 and col != n - 1:
            if a[row - 1][col + 1] == -1:
                row -= 1
                col += 1
                a[row][col] = k
            else:
                row += 1
                a[row][col] = k
        elif row != 0 and col == n - 1:
            row -= 1
            col = 0
            a[row][col] = k
        elif row == 0 and col == n - 1:
            row += 1
            a[row][col] = k
    return a


def board(win, starty, startx, lines, cols, tile_width, tile_height):
    endy = starty + lines * tile_height
    endx = startx + cols  * tile_width

    for j in range(starty, endy + 1, tile_height):
        for i in range(startx, endx + 1):
            win.addch(j, i, curses.ACS_HLINE)

    for i in range(startx, endx + 1, tile_width):
        for j in range(starty, endy + 1):
            win.addch(j, i, curses.ACS_VLINE)
    win.addch(starty, startx, curses.ACS_ULCORNER)
    win.addch(starty, endx, curses.ACS_URCORNER)
    win.addch(endy, startx, curses.ACS_LLCORNER)
    win.addch(endy, endx, curses.ACS_LRCORNER)
    for j in range(starty + tile_height, endy - tile_height + 1, tile_height):
        win.addch(j, startx, curses.ACS_LTEE)
        win.addch(j, endx, curses.ACS_RTEE)
        for i in range(startx + tile_width, endx - tile_width + 1, tile_width):
            win.addch(j, i, curses.ACS_PLUS)
    for i in range(startx + tile_width, endx - tile_width + 1, tile_width):
        win.addch(starty, i, curses.ACS_TTEE)
        win.addch(endy, i, curses.ACS_BTEE)
    win.refresh()


def magic_board(win, a, n):
    starty = (curses.LINES - n * HEIGHT) // 2
    startx = (curses.COLS - n * WIDTH) // 2
    board(win, starty, startx, n, n, WIDTH, HEIGHT)
    deltay = HEIGHT // 2
    deltax = WIDTH // 2
    for i in range(n):
        for j in range(n):
            win.addstr(starty + j * HEIGHT + deltay, startx + i * WIDTH + deltax, str(a[i][j]))
            

try:
    main()
finally:
    curses.endwin()
    