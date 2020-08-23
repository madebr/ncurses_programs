#!/usr/bin/env python

import curses
import os

#  Start curses mode
stdscr = curses.initscr()
# Print Hello World
stdscr.addstr("Hello World !!!\n")
# Print it on to the real screen
stdscr.refresh()
# Save the tty modes
curses.def_prog_mode()
# End curses mode temporarily
curses.endwin()
# Do whatever you like in cooked mode
os.system("/bin/sh")
# Return to the previous tty mode stored by def_prog_mode()
stdscr.refresh()
# Back to curses use the full capabilities of curses
stdscr.addstr("Another String\n")
stdscr.getch()
# End curses mode
curses.endwin()
