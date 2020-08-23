#!/usr/bin/env python

import curses
import sys


def main():
    # Start curses mode         
    stdscr = curses.initscr()
    # Line buffering disabled, Pass on evertything to me
    curses.cbreak()
    # I need that nifty F1
    stdscr.keypad(True)        

    height = 3
    width = 10
    # Calculating for a center placement of the window
    starty = (curses.LINES - height) // 2
    startx = (curses.COLS - width) // 2
    stdscr.addstr("Press F1 to exit")
    stdscr.refresh()
    my_win = MyWindows(height, width, starty, startx)

    while True:
        ch = stdscr.getch()
        if ch == curses.KEY_F1:
            break
        elif ch == curses.KEY_LEFT:
            del my_win
            startx -= 1
            my_win = MyWindows(height, width, starty, startx)
        elif ch == curses.KEY_RIGHT:
            del my_win
            startx += 1
            my_win = MyWindows(height, width, starty, startx)
        elif ch == curses.KEY_UP:
            del my_win
            starty -= 1
            my_win = MyWindows(height, width, starty, startx)
        elif ch == curses.KEY_DOWN:
            del my_win
            starty += 1
            my_win = MyWindows(height, width, starty, startx)

    # End curses mode
    curses.endwin()
    return 0


class MyWindows(object):
    def __init__(self, height, width, starty, startx):
        self.local_win = curses.newwin(height, width, starty, startx)
        # Default box for the vertial and horizontal lines
        self.local_win.box()
        # Show that box
        self.local_win.refresh()

    def __del__(self):
        # # This won't produce the desired result of erasing the window.
        # # It will leave it's four corners and so an ugly remnant of window.
        # local_win.box(" ", " ")

        self.local_win.border(" ", " ", " ", " ", " ", " ", " ", " ")
        # The parameters t  aken are
        # 1. win: the window on which to operate
        # 2. ls: character to be used for the left side of the window
        # 3. rs: character to be used for the right side of the window
        # 4. ts: character to be used for the top side of the window
        # 5. bs: character to be used for the bottom side of the window
        # 6. tl: character to be used for the top left corner of the window
        # 7. tr: character to be used for the top right corner of the window
        # 8. bl: character to be used for the bottom left corner of the window
        # 9. br: character to be used for the bottom right corner of the window
        #
        self.local_win.refresh()
        del self.local_win


try:
    main()
finally:
    curses.endwin()
