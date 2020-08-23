#!/usr/bin/env python

import curses
import enum
import random
import sys

STARTX = 9
STARTY = 3
WIDTH  = 6
HEIGHT = 4

BLANK  = 0

class Blank(object):
    def __init__(self):
        self.x = 0
        self.y = 0

class Dir(enum.Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <shuffle board order>\n".format(sys.argv[0]))
        sys.exit(1)
    try:
        n = int(sys.argv[1])
    except ValueError:
        sys.stderr("Argument must be a number")
        sys.exit(1)

    board, blank = init_board(n)
    stdscr = curses.initscr()
    stdscr.keypad(True)
    curses.cbreak()
    shuffle_board(stdscr, board, n)
    while True:
        c = stdscr.getch()
        if c == curses.KEY_F1:
            break
        elif c == curses.KEY_LEFT:
            move_blank(Dir.RIGHT, board, n, blank)
        elif c == curses.KEY_RIGHT:
            move_blank(Dir.LEFT, board, n, blank)
        elif c == curses.KEY_UP:
            move_blank(Dir.DOWN, board, n, blank)
        elif c == curses.KEY_DOWN:
            move_blank(Dir.UP, board, n, blank)
        shuffle_board(stdscr, board, n)
        if check_win(board, n, blank):
            stdscr.addstr(24, 0, "You Win !!!\n")
            stdscr.refresh()
            break
    curses.endwin()

def move_blank(direction, board, n, blank):
    if direction == Dir.LEFT:
        if blank.x != 0:
            blank.x -= 1
            temp = board[blank.x][blank.y]
            board[blank.x + 1][blank.y] = temp
            board[blank.x][blank.y] = BLANK
    elif direction == Dir.RIGHT:
        if blank.x != n - 1:
            blank.x += 1
            temp = board[blank.x][blank.y]
            board[blank.x - 1][blank.y] = temp
            board[blank.x][blank.y] = BLANK
    elif direction == Dir.UP:
        if blank.y != 0:
            blank.y -= 1
            temp = board[blank.x][blank.y]
            board[blank.x][blank.y + 1] = temp
            board[blank.x][blank.y] = BLANK
    elif direction == Dir.DOWN:
        if blank.y != n - 1:
            blank.y += 1
            temp = board[blank.x][blank.y]
            board[blank.x][blank.y - 1] = temp
            board[blank.x][blank.y] = BLANK

def check_win(board, n, blank):
    board[blank.x][blank.y] = n * n
    for i in range(n):
        for j in range(n):
            if board[i][j] != j * n + i + 1:
                board[blank.x][blank.y] = BLANK
                return False
    board[blank.x][blank.y] = BLANK
    return True

def init_board(n):
    board = [[0 for _ in range(n)] for _ in range(n)]
    blank = Blank()
    temp_board = list(range(n*n))
    random.shuffle(temp_board)
    
    k = 0
    for i in range(n):
        for j in range(n):
            if temp_board[k] == 0:
                blank.x = i
                blank.y = j
            board[i][j] = temp_board[k]
            k += 1

    return board, blank


def print_board(win, starty, startx, lines, cols, tile_width, tile_height):
    endy = starty + lines * tile_height
    endx = startx + cols  * tile_width

    for j in range(starty, endy + 1, tile_height):
        for i in range(startx, endx + 1):
            win.addch(j, i, curses.ACS_HLINE)
    for i in range(startx, endx + 1, tile_width):
        for j in range(starty, endy + 1):
            win.addch(j, i, curses.ACS_VLINE)
    win.addch(starty, startx, curses.ACS_ULCORNER)
    win.addch(endy, startx, curses.ACS_LLCORNER)
    win.addch(starty, endx, curses.ACS_URCORNER)
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

def shuffle_board(win, board, n):
    starty = (curses.LINES - n * HEIGHT) // 2
    startx = (curses.COLS  - n * WIDTH) // 2
    win.clear()
    win.addstr(24, 0, "Press F1 to Exit")
    print_board(win, starty, startx, n, n, WIDTH, HEIGHT)
    deltay = HEIGHT // 2
    deltax = WIDTH  // 2
    for j in range(n):
        for i in range(n):
            if board[i][j] != BLANK:
                win.addstr(starty + j * HEIGHT + deltay, startx + i * WIDTH  + deltax, "{:-2d}".format(board[i][j]))
    win.refresh()

try:
    main()
finally:
    curses.endwin()
    

