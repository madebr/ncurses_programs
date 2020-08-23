#!/usr/bin/env python

# We use addstr() instead of printw()
# Print python comments in bold, instead of C-style comments

import curses
import re
import sys


if len(sys.argv) < 2:
    sys.stderr.write("Usage: {} PYTHON_SOURCE\n".format(sys.argv[0]))
    sys.exit(1)

try:
    stdscr = curses.initscr()
    stdscr.keypad(True)
    row, col = stdscr.getmaxyx()


    def print_text(text):
        """
        Output the text, and pause if it is the last line on the page
        """
        stdscr.addstr(text)
        # get the current curser position
        y, x = stdscr.getyx()
        # are we are at the end of the screen
        if y == row - 1:
            # tell the user to press a key
            stdscr.addstr("<-Press Any Key->")
            stdscr.refresh()
            stdscr.getch()
            # clear the screen
            stdscr.clear()
            # start at the beginning of the screen
            stdscr.move(0, 0)


    # Read the input line per line
    for m in re.finditer(r"([^#]*)(#+[^\n]*\n)?", open(sys.argv[1], "r").read(), flags=re.M):
        for line in m.group(1).splitlines(True):
            print_text(line)
        if m.group(2):
            stdscr.attron(curses.A_BOLD)
            for line in m.group(2).splitlines(True):
                print_text(line)
            stdscr.attroff(curses.A_BOLD)

    stdscr.refresh()
    stdscr.getch()
finally:
    curses.endwin()
