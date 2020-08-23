#!/usr/bin/env python

# We use addstr() instead of printw()

import curses


try:
    # Start curses mode
    stdscr = curses.initscr()
    # Line buffering disabled
    curses.raw()
    # We get F1, F2 etc..
    stdscr.keypad(True)
    # Don't echo() while we do getch
    curses.noecho()

    stdscr.addstr("Type any character to see it in bold\n")

    # If raw() hadn't been called, we had to press enter before it gets to the program
    ch = stdscr.getch()
    # Without keypad enabled, curses.KEY_F1 will never be returned
    if ch == curses.KEY_F1:
        # Without noecho() some ugly escape characters might have been printed on screens
        stdscr.addstr("F1 Key pressed")
    else:
        stdscr.addstr("The pressed key is ")
        stdscr.attron(curses.A_BOLD)
        stdscr.addstr(chr(ch))
        stdscr.attroff(curses.A_BOLD)

    # Print it on to the real screen
    stdscr.refresh()
    # End curses mode
    stdscr.getch()
finally:
    curses.endwin()
