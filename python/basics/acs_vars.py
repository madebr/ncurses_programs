#!/usr/bin/env python

import curses


try:
    stdscr = curses.initscr()

    stdscr.addstr("Upper left corner           "); stdscr.addch(curses.ACS_ULCORNER); stdscr.addstr("\n")
    stdscr.addstr("Lower left corner           "); stdscr.addch(curses.ACS_LLCORNER); stdscr.addstr("\n")
    stdscr.addstr("Lower right corner          "); stdscr.addch(curses.ACS_LRCORNER); stdscr.addstr("\n")
    stdscr.addstr("Tee pointing right          "); stdscr.addch(curses.ACS_LTEE);     stdscr.addstr("\n")
    stdscr.addstr("Tee pointing left           "); stdscr.addch(curses.ACS_RTEE);     stdscr.addstr("\n")
    stdscr.addstr("Tee pointing up             "); stdscr.addch(curses.ACS_BTEE);     stdscr.addstr("\n")
    stdscr.addstr("Tee pointing down           "); stdscr.addch(curses.ACS_TTEE);     stdscr.addstr("\n")
    stdscr.addstr("Horizontal line             "); stdscr.addch(curses.ACS_HLINE);    stdscr.addstr("\n")
    stdscr.addstr("Vertical line               "); stdscr.addch(curses.ACS_VLINE);    stdscr.addstr("\n")
    stdscr.addstr("Large Plus or cross over    "); stdscr.addch(curses.ACS_PLUS);     stdscr.addstr("\n")
    stdscr.addstr("Scan Line 1                 "); stdscr.addch(curses.ACS_S1);       stdscr.addstr("\n")
    stdscr.addstr("Scan Line 3                 "); stdscr.addch(curses.ACS_S3);       stdscr.addstr("\n")
    stdscr.addstr("Scan Line 7                 "); stdscr.addch(curses.ACS_S7);       stdscr.addstr("\n")
    stdscr.addstr("Scan Line 9                 "); stdscr.addch(curses.ACS_S9);       stdscr.addstr("\n")
    stdscr.addstr("Diamond                     "); stdscr.addch(curses.ACS_DIAMOND);  stdscr.addstr("\n")
    stdscr.addstr("Checker board (stipple)     "); stdscr.addch(curses.ACS_CKBOARD);  stdscr.addstr("\n")
    stdscr.addstr("Degree Symbol               "); stdscr.addch(curses.ACS_DEGREE);   stdscr.addstr("\n")
    stdscr.addstr("Plus/Minus Symbol           "); stdscr.addch(curses.ACS_PLMINUS);  stdscr.addstr("\n")
    stdscr.addstr("Bullet                      "); stdscr.addch(curses.ACS_BULLET);   stdscr.addstr("\n")
    stdscr.addstr("Arrow Pointing Left         "); stdscr.addch(curses.ACS_LARROW);   stdscr.addstr("\n")
    stdscr.addstr("Arrow Pointing Right        "); stdscr.addch(curses.ACS_RARROW);   stdscr.addstr("\n")
    stdscr.addstr("Arrow Pointing Down         "); stdscr.addch(curses.ACS_DARROW);   stdscr.addstr("\n")
    stdscr.addstr("Arrow Pointing Up           "); stdscr.addch(curses.ACS_UARROW);   stdscr.addstr("\n")
    stdscr.addstr("Board of squares            "); stdscr.addch(curses.ACS_BOARD);    stdscr.addstr("\n")
    stdscr.addstr("Lantern Symbol              "); stdscr.addch(curses.ACS_LANTERN);  stdscr.addstr("\n")
    stdscr.addstr("Solid Square Block          "); stdscr.addch(curses.ACS_BLOCK);    stdscr.addstr("\n")
    stdscr.addstr("Less/Equal sign             "); stdscr.addch(curses.ACS_LEQUAL);   stdscr.addstr("\n")
    stdscr.addstr("Greater/Equal sign          "); stdscr.addch(curses.ACS_GEQUAL);   stdscr.addstr("\n")
    stdscr.addstr("Pi                          "); stdscr.addch(curses.ACS_PI);       stdscr.addstr("\n")
    stdscr.addstr("Not equal                   "); stdscr.addch(curses.ACS_NEQUAL);   stdscr.addstr("\n")
    stdscr.addstr("UK pound sign               "); stdscr.addch(curses.ACS_STERLING); stdscr.addstr("\n")

    stdscr.getch()
finally:
    curses.endwin()
