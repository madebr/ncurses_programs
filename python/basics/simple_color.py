#!/usr/bin/env python

import curses
import sys


def main():
    # Start curses mode
    stdscr = curses.initscr()
    if not curses.has_colors():
        curses.endwin()
        sys.stderr.write("Your terminal does not support color\n")
        return 1
    
    # Start color
    curses.start_color()

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.attron(curses.color_pair(1))
    print_in_middle(stdscr, curses.LINES // 2, 0, 0, "Voilà !!! In color ...")

    stdscr.getch()
    curses.endwin()


def print_in_middle(win, starty, startx, width, text):
    y, x = win.getyx()
    if startx != 0:
        x = startx
    if starty != 0:
        y = starty
    if width == 0:
        width = 80

    x = startx + (width - len(text)) // 2
    win.addstr(y, x, text)
    win.refresh()


try:
    main()
finally:
    curses.endwin()
