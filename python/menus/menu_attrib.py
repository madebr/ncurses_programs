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
    curses.start_color()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

    # Initialize items
    my_items = tuple(curses.menu.new_item(choice, choice) for choice in CHOICES)
    my_items[3].opts_off(curses.menu.O_SELECTABLE)
    my_items[6].opts_off(curses.menu.O_SELECTABLE)

    # Create menu
    my_menu = curses.menu.new_menu(my_items)

    # Set fore ground and back ground of the menu
    my_menu.set_fore(curses.color_pair(1) | curses.A_REVERSE)
    my_menu.set_back(curses.color_pair(2))
    my_menu.set_grey(curses.color_pair(3))

    # Post the menu
    stdscr.addstr(curses.LINES - 3, 0, "Press <ENTER> to see the option selected")
    stdscr.addstr(curses.LINES - 2, 0, "Up and Down arrow keys to naviage (F1 to Exit)")
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
        elif c == ord("\n"):
            stdscr.move(20, 10)
            stdscr.clrtoeol()
            stdscr.addstr(20, 0, "Item selected is : {}".format(my_menu.current_item().name().decode()))
            my_menu.pos_cursor()

    my_menu.unpost()
    curses.endwin()


try:
    main()
finally:
    curses.endwin()
