#!/usr/bin/env python

import curses
import dataclasses
import sys
from typing import List


POSX = 10
POSY = 5
DISC_CHAR = "*"
PEG_CHAR = "#"
TIME_OUT = 300

@dataclasses.dataclass
class Peg(object):
    nb: int             # Number of discs at present
    bottomx: int        # Bottom x coordinate
    bottomy: int        # Bottom y coordinate
    sizes: List[int]    # The disc sizes list


WELCOME_STRING = "Enter the number of discs you want to be solved: "


def main():
    stdscr = curses.initscr()    # Start curses mode
    curses.cbreak()              # Line buffering disabled. Pass on everything
    stdscr.keypad(True)
    curses.curs_set(False)

    print_in_middle(stdscr, 0, curses.LINES // 2, curses.COLS, WELCOME_STRING)
    try:
        n_discs = int(stdscr.getstr().decode())
    except ValueError:
        n_discs = 3

    stdscr.timeout(TIME_OUT)
    curses.noecho()

    pegs = init_pegs(n_discs)

    assert len(pegs[0].sizes) == n_discs, n_discs
    assert pegs[0].nb == n_discs, n_discs
    assert len(pegs[1].sizes) == n_discs, n_discs
    assert pegs[1].nb == 0, pegs[1].nb
    assert len(pegs[2].sizes) == n_discs, n_discs
    assert pegs[2].nb == 0, pegs[2].nb

    show_pegs(stdscr, pegs)
    solve_hanoi(stdscr, pegs, n_discs, 0, 1, 2)

    curses.endwin()             # End curses mode
    return 0

def solve_hanoi(win, pegs, n_discs, src, aux, dst):
    if n_discs == 0:
        return
    solve_hanoi(win, pegs, n_discs - 1, src, dst, aux)
    move_disc(pegs, src, dst)
    show_pegs(win, pegs)
    check_usr_response(win)
    solve_hanoi(win, pegs, n_discs - 1, aux, src, dst)

def check_usr_response(win):
    ch = win.getch()   # Waits for TIME_OUT milliseconds
    if ch == curses.KEY_F1:
        curses.endwin()
        sys.exit(0)

def move_disc(pegs, src, dst):
    index_src = len(pegs[src].sizes) - pegs[src].nb
    temp = pegs[src].sizes[index_src]
    pegs[src].sizes[index_src] = 0
    pegs[src].nb -= 1

    index_dst = len(pegs[dst].sizes) - pegs[dst].nb - 1
    pegs[dst].sizes[index_dst] = temp
    pegs[dst].nb += 1


def init_pegs(n_discs):
    dx = (3 + 2 * n_discs - 1) // 2
    return [
        Peg(
            n_discs,
            POSX + dx,
            POSY + 2 + n_discs,
            [3 + 2 * i for i in range(n_discs)],
        ),
        Peg(
            0,
            POSX + 3 * dx,
            POSY + 2 + n_discs,
            [0] * n_discs,
        ),
        Peg(
            0,
            POSX  + 5 * dx,
            POSY + 2 + n_discs,
            [0] * n_discs,
        ),
    ]


def show_pegs(win, pegs):
    win.clear()
    win.attron(curses.A_REVERSE)
    win.addstr(24, 0, "Press F1 to Exit")
    win.attroff(curses.A_REVERSE)
    for peg in pegs:
        win.addch(peg.bottomy - len(peg.sizes) - 1, peg.bottomx, PEG_CHAR)
        for i in range(len(peg.sizes) - peg.nb):
            win.addch(peg.bottomy - len(peg.sizes) + i, peg.bottomx, PEG_CHAR)
        for i in range(peg.nb):
            size = peg.sizes[-peg.nb + i]
            win.hline(peg.bottomy - peg.nb + i, peg.bottomx - size // 2, DISC_CHAR, size)
    win.refresh()


def print_in_middle(win, startx, starty, width, text):
    """

    :param win:
    :param startx: 0 means at present x
    :param starty: 0 means at present y
    :param width:
    :param text:
    :return:
    """
    y, x = win.getyx()
    if startx == 0:
        startx = x
    if starty == 0:
        starty = y
    if width == 0:
        width, height = win.getmaxyx()
    y = starty
    x = startx + (width - startx - len(text)) // 2
    win.addstr(y, x, text)
    win.refresh()

try:
    main()
finally:
    curses.endwin()
