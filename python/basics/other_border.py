#!/usr/bin/env python

import curses


class Border(object):
    def __init__(self):
        self.ls = '|'
        self.rs = '|'
        self.ts = '-'
        self.bs = '-'
        self.tl = '+'
        self.tr = '+'
        self.bl = '+'
        self.br = '+'


class Window(object):
    def __init__(self):
        self.width = 10
        self.height = 3
        self.startx = (curses.COLS - self.height) // 2
        self.starty = (curses.LINES - self.height) // 2
        self.border = Border()

    def create_box(self, window, flag):
        x = self.startx
        y = self.starty
        w = self.width
        h = self.height

        if flag:
            window.addch(y + 0, x + 0, self.border.tl)
            window.addch(y + 0, x + w, self.border.tr)
            window.addch(y + h, x + 0, self.border.bl)
            window.addch(y + h, x + w, self.border.br)
            window.hline(y + 0, x + 1, self.border.ts, w - 1)
            window.hline(y + h, x + 1, self.border.bs, w - 1)
            window.vline(y + 1, x + 0, self.border.ls, h - 1)
            window.vline(y + 1, x + w, self.border.rs, h - 1)
        else:
            pass
            # for j in range(y, y + h + 1):
            #     for i in range(x, x + w + 1):
            #         window.addch(j, i, ' ')

    def __repr__(self):
        return "<{}: {} {} {} {}>".format(type(self).__name__, self.startx, self.starty, self.width, self.height)


def main():
    # Start curses mode
    stdscr = curses.initscr()
    # Start the color functionality
    curses.start_color()
    # Line buffering disabled, Pass on verything to me
    curses.cbreak()
    # I need that nifty F1
    stdscr.keypad(True)
    curses.noecho()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)

    # Initialize the window parameters
    win = Window()
    stdscr.insstr(25, 0, repr(win))
    stdscr.refresh()

    stdscr.attron(curses.color_pair(1))
    stdscr.addstr(0, 0, "Press F1 to exit")
    stdscr.refresh()
    stdscr.attroff(curses.color_pair(1))

    win.create_box(stdscr, True)
    while True:
        ch = stdscr.getch()
        if ch == curses.KEY_F1:
            break
        if ch == curses.KEY_LEFT:
            win.create_box(stdscr, False)
            win.startx -= 1
            win.create_box(stdscr, True)
        elif ch == curses.KEY_RIGHT:
            win.create_box(stdscr, False)
            win.startx += 1
            win.create_box(stdscr, True)
        elif ch == curses.KEY_UP:
            win.create_box(stdscr, False)
            win.starty -= 1
            win.create_box(stdscr, True)
        elif ch == curses.KEY_DOWN:
            win.create_box(stdscr, False)
            win.starty += 1
            win.create_box(stdscr, True)
    # End curses mode
    curses.endwin()


try:
    main()
finally:
    curses.endwin()
