#!/usr/bin/env python

import curses


try:
    # Start curses mode
    stdscr = curses.initscr()
    # Start color functionality
    curses.start_color()

    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    stdscr.addstr("A Big string which I didn't care to type fully ")
    # First two parameters specify the position at which to start
    # Third parameter number of characters to update. -1 means till end of line
    # Fourth parameter is the normal attribute you wanted to give to the character
    # Fifth is the color index. It is the index given during init_pair()
    # use 0 if you didn't want color
    # stdscr.chgat(0, 0, -1, curses.A_BLINK| curses.A_COLOR)
    # stdscr.chgat(0, 0, -1, curses.A_BLINK | curses.A_COLOR)
    stdscr.chgat(0, 0, -1, curses.A_BLINK | curses.A_COLOR)

    # stdscr.refresh()
    stdscr.getch()
    #  End curses mode
finally:
    curses.endwin()
