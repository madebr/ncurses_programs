#!/usr/bin/env python

import curses.menu

CHOICES = [
    "Choice 1",
    "Choice 2",
    "Choice 3",
    "Choice 4",
    "Exit",
]


def main():
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)

    my_items = tuple(curses.menu.new_item(choice, choice) for choice in CHOICES)

    my_menu = curses.menu.new_menu(my_items)
    stdscr.addstr(curses.LINES - 2, 0, "F1 to Exit")
    my_menu.post()
    stdscr.refresh()

    while True:
        c = stdscr.getch()
        if c == curses.KEY_F1:
            break
        elif c == curses.KEY_DOWN:
            try:
                my_menu.driver(curses.menu.REQ_DOWN_ITEM)
            except curses.menu.error:
                pass
        elif c == curses.KEY_UP:
            try:
                my_menu.driver(curses.menu.REQ_UP_ITEM)
            except curses.menu.error:
                pass

    del my_items
    del my_menu

    curses.endwin()


try:
    main()
finally:
    curses.endwin()
