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
    stdscr.addstr(23, 0, "Click on Exit to quit (Works best in a virtual console)")
    stdscr.refresh()
    stdscr.attroff(curses.A_REVERSE)

    # Print the menu for the first time
    menu_win = curses.newwin(HEIGHT, WIDTH, starty, startx)
    # Need to interpret escape sequences on menu_win
    menu_win.keypad(True)

    choice = 0
    print_menu(menu_win, choice)

    # Get all the mouse events
    curses.mousemask(curses.ALL_MOUSE_EVENTS)

    while True:
        c = menu_win.getch()
        if c == curses.KEY_MOUSE:
            (event_id, event_x, event_y, event_z, event_bstate) = curses.getmouse()
            # When the user clicks left mouse button
            if event_bstate & (curses.BUTTON1_DOUBLE_CLICKED | curses.BUTTON1_RELEASED | curses.BUTTON1_CLICKED | curses.BUTTON1_TRIPLE_CLICKED):
                new_choice = report_choice(event_x, event_y)
                choice = choice if new_choice is None else new_choice
                if choice == -1:
                    # Exit chosen
                    break
                if choice:
                    stdscr.addstr(22, 1, "Choice made is : {} String Chosen is \"{:10}\"".format(choice, CHOICES[choice - 1]))
                    stdscr.refresh()
            print_menu(menu_win, choice)
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


def report_choice(mouse_x, mouse_y):
    """
    Report the choice according to mouse position
    :param mouse_x: mouse x position
    :param mouse_y: mouse y position
    :return: Return:
            - None if nothing selected
            - index in CHOICES list if selected
            - -1 if exit selected
    """
    i = startx + 2
    j = starty + 2

    result = None
    
    for choice_i, choice in enumerate(CHOICES):
        if mouse_y == j + choice_i and i <= mouse_x <= i + len(choice):
            result = choice_i
            break

    if result == len(CHOICES) - 1:
        return -1

    return result


try:
    main()
finally:
    curses.endwin()
