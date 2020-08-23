#!/usr/bin/env python

import curses.menu

CHOICES = [
    "Choice 1",
    "Choice 2",
    "Choice 3",
    "Choice 4",
    "Choice 5",
    "Choice 6",
    "Choice 7",
    "Exit",
]

def main():
    # Initialize curses
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)

    # Create items
    my_items = tuple(curses.menu.new_item(choice, choice) for choice in CHOICES)

    # Create menu
    my_menu = curses.menu.new_menu(my_items)

    # Make the menu multi valued
    my_menu.opts_off(curses.menu.O_ONEVALUE)

    stdscr.addstr(curses.LINES - 3, 0, "Use <SPACE> to select or unselect an item.")
    stdscr.addstr(curses.LINES - 2, 0, "<ENTER> to see presently selected items(F1 to Exit)")

    my_menu.post()
    stdscr.refresh()

    while True:
        c = stdscr.getch()
        if c == curses.KEY_F1:
            break
        elif c == curses. KEY_DOWN:
            try:
                my_menu.driver(curses.menu.REQ_DOWN_ITEM)
            except curses.menu.error:
                pass
        elif c == curses. KEY_UP:
            try:
                my_menu.driver(curses.menu.REQ_UP_ITEM)
            except curses.menu.error:
                pass
        elif c == ord(" "):
            try:
                my_menu.driver(curses.menu.REQ_TOGGLE_ITEM)
            except curses.menu.error:
                pass
        elif c == ord("\n"):
            items = my_menu.items()
            names = []
            for item in items:
                if item.value():
                    names.append(item.name().decode())
            stdscr.move(20, 0)
            stdscr.clrtoeol()
            stdscr.addstr(20, 0, " ".join(names))
            stdscr.refresh()
        stdscr.refresh()

try:
    main()
finally:
    curses.endwin()

