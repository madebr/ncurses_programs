#!/usr/bin/env python

import curses

WIDTH = 30
HEIGHT = 10

startx = 0
starty = 0

CHOICES = [
    "Choice 1",
    "Choice 2",
    "Choice 3",
    "Choice 4",
    "Exit",
]


def main():
    # Initialize curses
    stdscr = curses.initscr()
    curses.curs_set(False)
    stdscr.clear()
    curses.noecho()
    # Line buffering disabled. pass on everything
    curses.cbreak()

    # Try to put the window in the middle of screen
    global startx, starty
    startx = (80 - WIDTH) // 2
    starty = (24 - HEIGHT) // 2

    stdscr.attron(curses.A_REVERSE)
    stdscr.addstr(23, 0, "Use arrow keys to go up and down, Press enter to select a choice")
    stdscr.refresh()
    stdscr.attroff(curses.A_REVERSE)

    # Print the menu for the first time
    menu_win = curses.newwin(HEIGHT, WIDTH, starty, startx)
    # Need to interpret escape sequences on menu_win
    menu_win.keypad(True)

    choice = None
    highlight = 0
    print_menu(menu_win, highlight)

    while True:
        c = menu_win.getch()
        if c == curses.KEY_UP:
            highlight -= 1
            if highlight < 0:
                highlight = len(CHOICES) - 1
        elif c == curses.KEY_DOWN:
            highlight += 1
            if highlight >= len(CHOICES):
                highlight = 0
        elif c == 10:
            choice = highlight
        else:
            stdscr.addstr(24, 0, "Character pressed is = {:3d}. Hopefully it can be printed as '{}'".format(c, chr(c)))
            # stdscr.addstr(24, 0, "Character pressed is = {:3d}. Hopefully it can be printed as '{}'".format(c, type(c)))
            stdscr.refresh()

        print_menu(menu_win, highlight)
        if choice is not None:
            break

    stdscr.addstr(23, 0, "You chose choice {} with choice string '{}'".format(choice, CHOICES[choice]))

    stdscr.clrtoeol()
    stdscr.getch()

    stdscr.refresh()
    curses.endwin()
    return 0


def print_menu(menu_win, highlight):
    x = 2
    y = 2
    menu_win.box()
    for choice_i, choice in enumerate(CHOICES):
        if highlight == choice_i:
            menu_win.attron(curses.A_REVERSE)
            menu_win.addstr(y, x, choice)
            menu_win.attroff(curses.A_REVERSE)
        else:
            menu_win.addstr(y, x, choice)
        y += 1
    menu_win.refresh()


try:
    main()
finally:
    curses.endwin()
