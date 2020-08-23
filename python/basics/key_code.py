#!/usr/bin/env python

import curses


try:
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)

    ch = stdscr.getch()
finally:
    curses.endwin()

print("The key pressed is {}".format(ch))
