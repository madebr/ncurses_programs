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
            cur_item = my_menu.current_item()
            stdscr.move(curses.LINES - 2, 0)
            stdscr.clrtoeol()
            stdscr.addstr(curses.LINES - 2, 0, "You have chosen item {} with name {} and description {}".format(
                cur_item.index() + 1,
                cur_item.name().decode(),
                cur_item.description().decode(),
            ))
        stdscr.refresh()
        my_menu.pos_cursor()
    
    my_menu.unpost()
    curses.endwin()
    
try:
    main()
finally:
    curses.endwin()
