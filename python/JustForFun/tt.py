#!/usr/bin/env python

import curses
import datetime
import random

HSIZE = 60
LENGTH = 75
WIDTH = 10
STARTX = 1
STARTY = 5
STATUSX = 1
STATUSY = 25

GROUPS = [
    "`123456",
    "7890-=",
    "~!@#$%^",
    "&*()_+",
    "<>?",
    ",./\\",
    "asdfg",
    "jkl;'",
    "qwer",
    "uiop",
    "tyur",
    "zxcv",
    "bnm",
]

def main():
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)
    curses.intrflush(False)
    
    ch = curses.KEY_F1
    while True:
        if ch == curses.KEY_F1:
            choice = print_menu(stdscr)
            choice -= 1
            if choice == len(GROUPS):
                print_byebye(stdscr)
                curses.endwin()
                return
        
        stdscr.clear()
        string = "Typing window"
        print_in_middle(stdscr, STARTX, STARTY - 2, LENGTH, string)
        stdscr.attron(curses.A_REVERSE)
        stdscr.addstr(STATUSY, STATUSX, "Press F1 to Main Menu")
        stdscr.refresh()
        stdscr.attroff(curses.A_REVERSE)

        test_array = create_test_string(choice)
        typing_win = curses.newwin(WIDTH, LENGTH, STARTY, STARTX)
        typing_win.keypad(True)
        curses.intrflush(False)
        typing_win.box()
    
        x = 1
        y = 1
        typing_win.addstr(y, x, test_array)
        typing_win.refresh()
        y += 1
    
        mistakes = 0
        i = 0
        start_t = datetime.datetime.now()
        typing_win.move(y, x)
        typing_win.refresh()
        ch = 0
        while ch != curses.KEY_F1 and i != HSIZE + 1:
            ch = typing_win.getch()
            typing_win.addch(y, x, ch)
            typing_win.refresh()
            x += 1
            try:
                correct = ch == test_array[i]
            except IndexError:
                correct = False
            if correct:
                i += 1
            else:
                mistakes += 1
                i += 1
        end_t = datetime.datetime.now()
        words = i // 5
        print_time(stdscr, start_t, end_t, words, mistakes)
        

def print_menu(win):
    choice = 0
    while True:
        win.clear()
        win.addstr("\n\n")
        print_in_middle(win, 1, 1, 0, "* * *   Welcome to typing practice (Version 1.0) * * * ")
        win.addstr("\n\n\n")
        for i in range(len(GROUPS)):
            win.addstr("\t{:3d}: \tPractice {}\n".format(i + 1, GROUPS[i]))
        win.addstr("\t{:3d}: \tExit\n".format(len(GROUPS)+1))
    
        win.addstr("\n\n\tChoice: ")
        win.refresh()
        curses.echo()
        try:
            choice = int(win.getstr().decode())
        except ValueError:
            pass
        curses.noecho()
    
        if 1 <= choice <= len(GROUPS) + 1:
            break
        else:
            win.attron(curses.A_REVERSE)
            win.addstr(STATUSY, STATUSX, "Wrong choice\tPress any key to continue")
            win.attroff(curses.A_REVERSE)
            win.getch()
    return choice


def create_test_string(choice):
    return " ".join("".join(random.choices(GROUPS[choice], k=4)) for _ in range(HSIZE // 5))


def print_byebye(win):
    win.addstr("\n")
    print_in_middle(win, 0, 0, 0, "Thank you for using my typing tutor\n")
    print_in_middle(win, 0, 0, 0, "Bye Bye ! ! !\n")
    win.refresh()

def print_time(win, start, end, words, mistakes):
    diff = end - start
    wpm = 60 * words / diff.total_seconds()

    win.attron(curses.A_REVERSE)
    win.addstr(STATUSY, STATUSX, "Mistakes made : {} time taken: {} WPM : {:.2f}    Press any Key to continue".format(
        mistakes, diff, wpm))
    win.attroff(curses.A_REVERSE)
    
    win.refresh()
    win.getch()

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
