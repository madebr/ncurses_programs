#!/usr/bin/env python

import curses.panel

NLINES = 10
NCOLS = 40


class PanelData(object):
    def __init__(self, x, y, w, h, label, label_color, next):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.label = label
        self.label_color = label_color
        self.next = next
        

def main():
    # Initialize curses
    stdscr = curses.initscr()
    curses.start_color()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)

    NB = 3

    my_wins = init_wins(NB)

    # Initialize all the colors
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)

    # Attach a panel to each window           Order is bottom up
    my_panels = [
        curses.panel.new_panel(my_wins[0]),   # Push 0, order: stdscr-0
        curses.panel.new_panel(my_wins[1]),   # Push 1, order: stdscr-0-1
        curses.panel.new_panel(my_wins[2]),   # Push 2, order: stdscr-0-1-2
    ]
    my_panels.extend([curses.panel.new_panel(my_wins[i]) for i in range(3, len(my_wins))])

    set_user_ptrs(my_panels)
    # Update the stacking order. 2nd panel will be on top
    curses.panel.update_panels()

    # Show it on the screen
    stdscr.attron(curses.color_pair(4))
    stdscr.addstr(curses.LINES - 3, 0, "Use 'm' for moving, 'r' for resizing")
    stdscr.addstr(curses.LINES - 2, 0, "Use tab to browse through the windows (F1 to Exit)")
    stdscr.attroff(curses.color_pair(4))
    curses.doupdate()

    stack_top = my_panels[-1]
    top = stack_top.userptr()
    newx = top.x
    newy = top.y
    neww = top.w
    newh = top.h
    move = False
    size = False

    while True:
        ch = stdscr.getch()
        if ch == curses.KEY_F1:
            break
        elif ch == ord("\t"):   # Tab
            top.next.top()
            stack_top = top.next
            top = stack_top.userptr()
            newx = top.x
            newy = top.y
            neww = top.w
            newh = top.h
        elif ch == ord('r'):    # Re-Size
            size = True
            stdscr.attron(curses.color_pair(4))
            stdscr.move(curses.LINES - 4, 0)
            stdscr.clrtoeol()
            stdscr.addstr(curses.LINES - 4, 0, "Entered Resizing: Use Arrow Keys to resize and press <ENTER> to end resizing")
            stdscr.refresh()
            stdscr.attroff(curses.color_pair(4))
        elif ch == ord("m"):    # Move
            stdscr.attron(curses.color_pair(4))
            stdscr.move(curses.LINES - 4, 0)
            stdscr.clrtoeol()
            stdscr.addstr(curses.LINES - 4, 0, "Entered Moving: Use Arrow Keys to Move and press <ENTER> to end moving")
            stdscr.refresh()
            stdscr.attroff(curses.color_pair(4))
            move = True
        elif ch == curses.KEY_LEFT:
            if size:
                newx -= 1
                neww += 1
            if move:
                newx -= 1
        elif ch == curses.KEY_RIGHT:
            if size:
                newx += 1
                neww -= 1
            if move:
                newx += 1
        elif ch == curses.KEY_UP:
            if size:
                newy -= 1
                newh += 1
            if move:
                newy -= 1
        elif ch == curses.KEY_DOWN:
            if size:
                newy += 1
                newh -= 1
            if move:
                newy += 1
        elif ch == ord("\n"):       # Enter
            stdscr.move(curses.LINES - 4, 0)
            stdscr.clrtoeol()
            stdscr.refresh()
            if size:
                old_win = stack_top.window()
                temp_win = curses.newwin(newh, neww, newy, newx)
                stack_top.replace(temp_win)
                win_show(temp_win, top.label, top.label_color)
                del old_win
                size = False
            if move:
                stack_top.move(newy, newx)
                move = False

        stdscr.attron(curses.color_pair(4))
        stdscr.addstr(curses.LINES - 3, 0, "Use 'm' for moving, 'r' for resizing")
        stdscr.addstr(curses.LINES - 2, 0, "Use tab to browse through the windows (F1 to Exit)")
        stdscr.attroff(curses.color_pair(4))
        curses.panel.update_panels()
        curses.doupdate()

    curses.endwin()
    return 0


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


def set_user_ptrs(panels):
    # Set the PANEL_DATA structures for individual panels
    for panel_i, panel in enumerate(panels):
        win = panel.window()
        y, x = win.getbegyx()
        h, w = win.getmaxyx()
        label = "Window Number {}".format(panel_i + 1)
        label_color = 1 + panel_i  % 3
        panel_next = panels[(panel_i + 1) % len(panels)]
        panel.set_userptr(PanelData(x, y, w, h, label, label_color, panel_next))


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
