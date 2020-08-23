#!/usr/bin/env python

# We use addstr() instead of printw()

import curses


try:
    # message to be appeared on the screen
    mesg = "Just a string"

    # start the curses mode
    stdscr = curses.initscr()
    # get number of rows and columns on the screen
    row, col = stdscr.getmaxyx()
    # print the message at the center of the screen
    stdscr.addstr(row // 2, (col - len(mesg)) // 2, mesg)
    stdscr.addstr(row - 2, 0, "This screen has {} rows and {} columns\n".format(row, col))
    stdscr.refresh()
    stdscr.getch()
finally:
    curses.endwin()
