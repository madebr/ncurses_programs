#!/usr/bin/env python

import curses.panel

NLINES = 10
NCOLS = 40


class PanelData(object):
    def __init__(self, hide):
        """
        :param hide: True if panel is hidden
        """
        self.hide = hide


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

    NB = 3

    my_wins = init_wins(NB)

    # Attach a panel to each window           Order is bottom up
    my_panels = [
        curses.panel.new_panel(my_wins[0]),   # Push 0, order: stdscr-0
        curses.panel.new_panel(my_wins[1]),   # Push 1, order: stdscr-0-1
        curses.panel.new_panel(my_wins[2]),   # Push 2, order: stdscr-0-1-2
    ]
    my_panels.extend([curses.panel.new_panel(my_wins[i]) for i in range(3, len(my_wins))])

    # Initialize panel datas saying that nothing is hidden
    panel_datas = [PanelData(False) for _ in range(NB)]

    for panel, panel_data in zip(my_panels, panel_datas):
        panel.set_userptr(panel_data)

    # Update the stacking order. 2nd panel will be on top
    curses.panel.update_panels()

    # Show it on the screen
    stdscr.attron(curses.color_pair(4))
    stdscr.addstr(curses.LINES - 3, 0, "Show or Hide a window with 'a'(first window)  'b'(Second Window)  'c'(Third Window)")
    stdscr.addstr(curses.LINES - 2, 0, "F1 to Exit")

    stdscr.attroff(curses.color_pair(4))
    curses.doupdate()

    while True:
        ch = stdscr.getch()
        if ch == curses.KEY_F1:
            break
        elif ch == ord("a"):
            temp = my_panels[0].userptr()
            if temp.hide:
                my_panels[0].show()
            else:
                my_panels[0].hide()
            temp.hide = not temp.hide
        elif ch == ord("b"):
            temp = my_panels[1].userptr()
            if temp.hide:
                my_panels[1].show()
            else:
                my_panels[1].hide()
            temp.hide = not temp.hide
        elif ch == ord("c"):
            temp = my_panels[2].userptr()
            if temp.hide:
                my_panels[2].show()
            else:
                my_panels[2].hide()
            temp.hide = not temp.hide
        curses.panel.update_panels()
        curses.doupdate()
    curses.endwin()


def init_wins(nb):
    """
    Put all the windows
    :param nb: number of windows
    :return: List with `nb` windows
    """
    y = 2
    x = 10
    result = []
    for i in range(nb):
        win = curses.newwin(NLINES, NCOLS, y, x)
        win_show(win, "Window Number {}".format(i + 1), 1 + i % 3)
        y += 3
        x += 7
        result.append(win)
    return result


def win_show(win, label, label_color):
    """
    Show the window with a border and a label
    :param win: window to show
    :param label: window label
    :param label_color: window label color
    """
    height, width = win.getmaxyx()

    win.box()
    win.addch(2, 0, curses.ACS_LTEE)
    win.hline(2, 1, curses.ACS_HLINE, width - 2)
    win.addch(2, width - 1, curses.ACS_RTEE)

    print_in_middle(win, 1, 0, width, label, curses.color_pair(label_color))


def print_in_middle(win, starty, startx, width, text, color):
    y = starty
    x = startx + (width - len(text)) // 2
    win.attron(color)
    win.addstr(y, x, text)
    win.attroff(color)
    win.refresh()


try:
    main()
finally:
    curses.endwin()
