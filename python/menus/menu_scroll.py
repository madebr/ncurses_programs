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
    "Choice 8",
    "Choice 9",
    "Choice 10",
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
    curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)

    # Create items
    my_items = tuple(curses.menu.new_item(choice, choice) for choice in CHOICES)
    
    # Create menu
    my_menu = curses.menu.new_menu(my_items)

    # Create the window to be associated with the menu
    my_menu_win = stdscr.derwin(10, 40, 4, 4)  #curses.newwin(10, 40, 4, 4)
    my_menu_win.keypad(True)
     
    # Set main window and sub window
    my_menu.set_win(my_menu_win)
    my_menu.set_sub(my_menu_win.derwin(6, 38, 3, 1))
    my_menu.set_format(5, 1)
            
    # Set menu mark to the string " * "
    my_menu.set_mark(" * ")

    # Print a border around the main window and print a title
    my_menu_win.box()
    print_in_middle(my_menu_win, 1, 0, 40, "My Menu", curses.color_pair(1))
    my_menu_win.addch(2, 0, curses.ACS_LTEE)
    my_menu_win.hline(2, 1, curses.ACS_HLINE, 38)
    my_menu_win.addch(2, 39, curses.ACS_RTEE)
        
    # Post the menu
    my_menu.post()
    my_menu_win.refresh()
    
    stdscr.attron(curses.color_pair(2))
    stdscr.addstr(curses.LINES - 2, 0, "Use PageUp and PageDown to scoll down or up a page of items");
    stdscr.addstr(curses.LINES - 1, 0, "Arrow Keys to navigate (F1 to Exit)")
    stdscr.attroff(curses.color_pair(2))
    stdscr.refresh()

    while True:
        c = my_menu_win.getch()
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
        elif c == curses. KEY_NPAGE:
            try:
                my_menu.driver(curses.menu.REQ_SCR_DPAGE)
            except curses.menu.error:
                pass
        elif c == curses. KEY_PPAGE:
            try:
                my_menu.driver(curses.menu.REQ_SCR_UPAGE)
            except curses.menu.error:
                pass
        my_menu_win.refresh()

    # Unpost and free all the memory taken up
    my_menu.unpost()
    curses.endwin()


def print_in_middle(win, starty, startx, width, text, color):
    x = startx + (width - len(text)) // 2
    win.attron(color)
    win.addstr(starty, x, text)
    win.attroff(color)
    win.refresh()

try:
    main()
finally:
    curses.endwin()
