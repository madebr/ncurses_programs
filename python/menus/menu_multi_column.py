#!/usr/bin/env python

import curses.menu

CHOICES = [
    "Choice 1", "Choice 2", "Choice 3", "Choice 4", "Choice 5",
    "Choice 6", "Choice 7", "Choice 8", "Choice 9", "Choice 10",
    "Choice 11", "Choice 12", "Choice 13", "Choice 14", "Choice 15",
    "Choice 16", "Choice 17", "Choice 18", "Choice 19", "Choice 20",
    "Exit",
]

def main():
    stdscr = curses.initscr()
    curses.start_color()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    # Create items
    my_items = tuple(curses.menu.new_item(choice, choice) for choice in CHOICES)

    # Create menu
    my_menu = curses.menu.new_menu(my_items)

    # Set menu option not to show the description
    my_menu.opts_off(curses.menu.O_SHOWDESC)

    # Create the window to be associated with the menu
    my_menu_win = curses.newwin(10, 70, 4, 4)
    my_menu_win.keypad(True)
     
    # Set main window and sub window
    my_menu.set_win(my_menu_win)
    my_menu.set_sub(my_menu_win.derwin(6, 68, 3, 1))
    my_menu.set_format(5, 3)
    my_menu.set_mark(" * ")

    # Print a border around the main window and print a title
    my_menu_win.box(0, 0)
    
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(curses.LINES - 3, 0, "Use PageUp and PageDown to scroll")
    stdscr.addstr(curses.LINES - 2, 0, "Use Arrow Keys to navigate (F1 to Exit)")
    stdscr.attroff(curses.color_pair(2))
    stdscr.refresh()

    # Post the menu
    my_menu.post()
    my_menu_win.refresh()
    
    while True:
        c = my_menu_win.getch()
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
        elif c == curses.KEY_LEFT:
            try:
                my_menu.driver(curses.menu.REQ_LEFT_ITEM)
            except curses.menu.error:
                pass
        elif c == curses.KEY_RIGHT:
            try:
                my_menu.driver(curses.menu.REQ_RIGHT_ITEM)
            except curses.menu.error:
                pass
        elif c == curses.KEY_NPAGE:
            try:
                my_menu.driver(curses.menu.REQ_SCR_DPAGE)
            except curses.menu.error:
                pass
        elif c == curses.KEY_PPAGE:
            try:
                my_menu.driver(curses.menu.REQ_SCR_UPAGE)
            except curses.menu.error:
                pass
        my_menu_win.refresh()

    # Unpost and free all the memory taken up
    my_menu.unpost()
    curses.endwin()

try:
    main()
finally:
    curses.endwin()
