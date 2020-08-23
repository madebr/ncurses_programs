#!/usr/bin/env python

import curses

STARTX = 0
STARTY = 0
ENDX = 79
ENDY = 24

CELL_CHAR = "#"
TIME_OUT = 300


class State(object):
    def __init__(self):
        self.oldstate = False
        self.newstate = False

def main():
    stdscr = curses.initscr()
    curses.cbreak()
    stdscr.timeout(TIME_OUT)
    stdscr.keypad(True)

    ENDX = curses.COLS - 1
    ENDY = curses.LINES - 1


    workarea = [[State() for _ in range(curses.LINES)] for _ in range(curses.COLS)]

    if True:
        # For inverted U
        workarea[39][15].newstate = True
        workarea[40][15].newstate = True
        workarea[41][15].newstate = True
        workarea[39][16].newstate = True
        workarea[39][17].newstate = True
        workarea[41][16].newstate = True
        workarea[41][17].newstate = True
    if False:
        # For block
        workarea[37][13].newstate = True
        workarea[37][14].newstate = True
        workarea[38][13].newstate = True
        workarea[38][14].newstate = True
        
    update_state(workarea, STARTX, STARTY, ENDX, ENDY)

    display(stdscr, workarea, STARTX, STARTY, ENDX, ENDY)
    while stdscr.getch() != curses.KEY_F1:
        for i in range(STARTX, ENDX + 1):
            for j in range(STARTY, ENDY + 1):
                calc(workarea, i, j)
        update_state(workarea, STARTX, STARTY, ENDX, ENDY)
        display(stdscr,  workarea, STARTX, STARTY, ENDX, ENDY)
    
    curses.endwin()

def display(win, area, startx, starty, endx, endy):
    win.clear()
    for i in range(startx, endx + 1):
        for j in range(starty, endy + 1):
            if area[i][j].newstate:
                win.addch(j, i, CELL_CHAR)
    win.refresh()

def calc(area, i, j):
    neighbours = 0 \
        + area[(i - 1 + curses.COLS) % curses.COLS][j].oldstate                                     \
        + area[(i - 1 + curses.COLS) % curses.COLS][(j - 1 + curses.LINES) % curses.LINES].oldstate \
        + area[(i - 1 + curses.COLS) % curses.COLS][(j + 1) % curses.LINES].oldstate                \
        + area[(i + 1) % curses.COLS][j].oldstate                                                   \
        + area[(i + 1) % curses.COLS][(j - 1 + curses.LINES) % curses.LINES].oldstate               \
        + area[(i + 1) % curses.COLS][(j + 1) % curses.LINES].oldstate                              \
        + area[i][(j - 1 + curses.LINES) % curses.LINES].oldstate                                   \
        + area[i][(j + 1) % curses.LINES].oldstate
                                
    newstate = False
    if area[i][j].oldstate and (neighbours == 2 or neighbours == 3):
         newstate = True
    else:
        if not area[i][j].oldstate and neighbours == 3:
             newstate = True
    area[i][j].newstate = newstate


def update_state(area, startx, starty, endx, endy):
    for i in range(startx, endx + 1):
        for j in range(starty, endy + 1):
            area[i][j].oldstate = area[i][j].newstate

try:
    main()
finally:
    curses.endwin()