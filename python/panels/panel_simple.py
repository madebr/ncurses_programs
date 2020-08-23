#!/usr/bin/env python

import curses.panel


try:
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    
    lines = 10
    cols = 40
    y = 2
    x = 4

    # Create windows for the panels
    my_wins = [
        curses.newwin(lines, cols, y, x),
        curses.newwin(lines, cols, y + 1, x + 5),
        curses.newwin(lines, cols, y + 2, x + 10),
    ]

    # Create borders around the windows so that you can see the effect of panels
    for win in my_wins:
        win.box()

    # Attach a panel to each window
    # Order is bottom up

    my_panels = [
        curses.panel.new_panel(my_wins[0]),  # Push 0, order: stdscr-0
        curses.panel.new_panel(my_wins[1]),  # Push 1, order: stdscr-0-1
        curses.panel.new_panel(my_wins[2]),  # Push 2, order: stdscr-0-1-2
    ]

    # Update the stacking order. 2nd panel will be on top
    curses.panel.update_panels()

    # Show it on the screen
    # stdscr.refresh()
    curses.doupdate()

    stdscr.getch()
finally:
    curses.endwin()
