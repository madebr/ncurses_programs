#!/usr/bin/env python

# We use addstr() instead of printw()

import curses


try:
    # message to be appeared on the screen
    mesg = "Enter a string: "

    # start the curses mode
    stdscr = curses.initscr()
    # get the number of rows and columns
    row, col = stdscr.getmaxyx()
    # print the message at the center of the screen
    stdscr.addstr(row // 2, (col - len(mesg)) // 2, mesg)
    txt = stdscr.getstr().decode()
    stdscr.addstr(curses.LINES - 2, 0, "You Entered: {}".format(txt))
    stdscr.getch()
finally:
    curses.endwin()
