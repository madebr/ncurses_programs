#!/usr/bin/env python

# We use addstr() instead of printw()

import curses

try:
    # Start curses mode
    stdscr = curses.initscr()
    # Print Hello World
    stdscr.addstr("Hello World !!!")
    # Print it on to the real screen
    stdscr.refresh()
    # Wait for user input
    stdscr.getch()
    # End curses mode
finally:
    curses.endwin()
