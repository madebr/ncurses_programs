#!/usr/bin/env python

import curses.panel

NLINES = 10
NCOLS = 40


def init_wins(nb):
    """ 
    Create all the windows
    :param nb: Number of windows to create
    :return: list with the windows
    """
    y = 2
    x = 10
    result = []
    for i in range(nb):
        win = curses.newwin(NLINES, NCOLS, y, x)
        result.append(win)
        label = "Window Number {}".format(i)
        win_show(win, label, i + 1)
        y += 3
        x += 7
    return result


def win_show(win, label, label_color):
    height, width = win.getmaxyx()

    win.box()
    win.addch(2, 0, curses.ACS_LTEE)
    win.hline(2, 1, curses.ACS_HLINE, width - 2)
    win.addch(2, width - 1, curses.ACS_RTEE)
    
    print_in_middle(win, 1, 0, width, label, curses.color_pair(label_color))


def print_in_middle(win, starty, startx, width, label, color):
    y, x = win.getyx()
    if startx != 0:
        x = startx
    if starty != 0:
        y = starty
    if width == 0:
        width = 80
        
    x = startx + (width - len(label)) // 2
    win.attron(color)
    win.addstr(y, x, label)
    win.attroff(color)
    win.refresh()


def main():
    # Initialize curses
    stdscr = curses.initscr()
    curses.start_color()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
     
    # Initialize all the colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)

    my_wins = init_wins(3)

    # Attach a panel to each window. Order is bottom up.
    my_panels = [
        curses.panel.new_panel(my_wins[0]),  # Push 0, order: stdscr-0
        curses.panel.new_panel(my_wins[1]),  # Push 1, order: stdscr-0-1
        curses.panel.new_panel(my_wins[2]),  # Push 2, order: stdscr-0-1-2
    ]

    # Set up the user pointers to the next panel
    my_panels[0].set_userptr(my_panels[1])
    my_panels[1].set_userptr(my_panels[2])
    my_panels[2].set_userptr(my_panels[0])

    # Update the stacking order. 2nd panel will be on top
    curses.panel.update_panels()

    # Show it on the screen
    stdscr.attron(curses.color_pair(4))
    stdscr.addstr(curses.LINES - 2, 0, "Use tab to browse through the windows (F1 to Exit)")
    stdscr.attroff(curses.color_pair(4))
    curses.doupdate()

    top = my_panels[2]
    while True:
        ch = stdscr.getch()
        if ch == curses.KEY_F1:
            break
        elif ch == ord("\t"):
            top = top.userptr()
            top.top()
        curses.panel.update_panels()
        curses.doupdate()
    curses.endwin()


try:
    main()
finally:
    curses.endwin()