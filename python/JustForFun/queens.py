#!/usr/bin/env python

import curses
import sys

QUEEN_CHAR  = "*"


def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: {} <number of queens (chess board order)>\n".format(sys.argv[0]))
        sys.exit(1)

    try:
        num_queens = int(sys.argv[1])
    except ValueError:
        sys.stderr("Invalid number\n")
        sys.exit(1)
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.keypad(True)
    nqueens(stdscr, num_queens)
    curses.endwin()


def nqueens(win, num):
    num_solutions = 0

    position = [0] * (num + 1)

    position[1] = 0
    current = 1     # current queen is being checked
                    # position[current] is the column
    while current > 0:
        position[current] += 1
        while position[current] <= num and place(current, position) == 0:
            position[current] += 1
        if position[current] <= num:
            if current == num:
                num_solutions += 1
                printwin(win, position, num, num_solutions)
            else:
                current += 1
                position[current] = 0
        else:
            current -= 1    #  backtrack
    print("Total Number of Solutions : {}".format(num_solutions))
    return position


def place(current, position):
    if current == 1:
        return 1
    for i in range(1, current):
        if position[i] == position[current]:
            return(0)
        elif abs(position[i] - position[current]) == abs(i - current):
            return 0
    return 1

def printwin(win, positions, num_queens, num_solutions):
    y = 2
    x = 2
    w = 4
    h = 2

    win.addstr(0, 0, "Solution No: {}".format(num_solutions))
    board(win, y, x, num_queens, num_queens, w, h)
    for count in range(1, num_queens + 1):
        tempy = y + (count - 1) * h + h // 2
        tempx = x + (positions[count] - 1) * w + w // 2
        win.addch(tempy, tempx, QUEEN_CHAR)
    win.refresh()
    win.addstr(curses.LINES - 2, 0, "Press Any Key to See next solution (F1 to Exit)")
    if win.getch() == curses.KEY_F1:
        curses.endwin()
        sys.exit(0)
    win.clear()


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


try:
    main()
finally:
    curses.endwin()
