#!/usr/bin/env python

import curses
import curses.ascii
import enum
import time
from typing import Dict, List, Optional


class Vec2(object):
    def __init__(self, x: int, y: int):
        self.x, self.y = x, y

    def copy_from(self, v: "Vec2") -> None:
        self.x, self.y = v.x, v.y

    def __eq__(self, v: "Vec2") -> bool:
        return self.x == v.x and self.y == v.y

    def __str__(self):
        return "({},{})".format(self.x, self.y)


class TetronimoShape(object):
    def __init__(self, data: List[List[bool]]):
        self.data = data

    @classmethod
    def from_string(cls, description: str):
        lines = []
        for linestr in description.splitlines():
            lines.append([c != " " for c in linestr])
        if len(set(len(line) for line in lines)) > 1:
            raise ValueError("Bad description")
        return cls(lines)


class Tetronimo(object):
    def __init__(self, name: str, code: str, color: str, shapes: List[TetronimoShape]):
        self.name = name
        self.code = code
        self.color = color
        self.shapes = shapes


TETRONIMOS = [
    Tetronimo("straight", "I", "cyan", [
        TetronimoShape.from_string(
            "    \n"
            "xxxx\n"
            "    \n"
            "    "
        ), TetronimoShape.from_string(
            "  x \n"
            "  x \n"
            "  x \n"
            "  x "
        ), TetronimoShape.from_string(
            "    \n"
            "    \n"
            "xxxx\n"
            "    "
        ), TetronimoShape.from_string(
            " x  \n"
            " x  \n"
            " x  \n"
            " x  "
        ),
    ]),
    Tetronimo("square", "T", "purple", [
        TetronimoShape.from_string(
            "xx\n"
            "xx"
        ),
    ]),
    Tetronimo("t", "T", "yellow", [
        TetronimoShape.from_string(
            " x \n"
            "xxx\n"
            "   "
        ), TetronimoShape.from_string(
            " x \n"
            " xx\n"
            " x "
        ), TetronimoShape.from_string(
            "   \n"
            "xxx\n"
            " x "
        ), TetronimoShape.from_string(
            " x \n"
            "xx \n"
            " x "
        ),
    ]),
    Tetronimo("l", "L", "orange", [
        TetronimoShape.from_string(
            "  x\n"
            "xxx\n"
            "   "
        ), TetronimoShape.from_string(
            " x \n"
            " x \n"
            " xx"
        ), TetronimoShape.from_string(
            "   \n"
            "xxx\n"
            "x  "
        ), TetronimoShape.from_string(
            "xx \n"
            " x \n"
            " x "
        ),
    ]),
    Tetronimo("j", "J", "blue", [
        TetronimoShape.from_string(
            "x  \n"
            "xxx\n"
            "   "
        ), TetronimoShape.from_string(
            " xx\n"
            " x \n"
            " x "
        ), TetronimoShape.from_string(
            "   \n"
            "xxx\n"
            "  x"
        ), TetronimoShape.from_string(
            " x \n"
            " x \n"
            "xx "
        ),
    ]),
    Tetronimo("s", "S", "green", [
        TetronimoShape.from_string(
            " xx\n"
            "xx \n"
            "   "
        ), TetronimoShape.from_string(
            " x \n"
            " xx\n"
            "  x"
        ), TetronimoShape.from_string(
            "   \n"
            " xx\n"
            "xx "
        ), TetronimoShape.from_string(
            "x  \n"
            "xx \n"
            " x "
        ),
    ]),
    Tetronimo("z", "Z", "red", [
        TetronimoShape.from_string(
            "xx \n"
            " xx\n"
            "   "
        ), TetronimoShape.from_string(
            "  x\n"
            " xx\n"
            " x "
        ), TetronimoShape.from_string(
            "   \n"
            "xx \n"
            " xx"
        ), TetronimoShape.from_string(
            " x \n"
            "xx \n"
            "x  "
        ),
    ]),
]


class Randomizer(object):
    def __init__(self, tetronimos: List[Tetronimo]):
        self.tetronimos = tetronimos
        self.bag = []

    def next(self) -> Tetronimo:
        if len(self.bag) == 0:
            self.bag = list(self.tetronimos)
        import random
        v = random.choice(self.bag)
        self.bag.remove(v)
        return v


class TetronimoState(object):
    def __init__(self, pos: Vec2, tetronimo: Tetronimo, next_tetronimo: Tetronimo, saved_tetronimo: Optional[Tetronimo], shape_index: int):
        self._pos = pos
        self.tetronimo = tetronimo
        self.next_tetronimo = next_tetronimo
        self.saved_tetronimo = saved_tetronimo
        self.shape_index = shape_index

    @property
    def pos(self) -> Vec2:
        return self._pos

    def copy_from(self, state: "TetronimoState") -> None:
        self._pos.copy_from(state._pos)
        self.tetronimo = state.tetronimo
        self.next_tetronimo = state.next_tetronimo
        self.saved_tetronimo = state.saved_tetronimo
        self.shape_index = state.shape_index

    def __eq__(self, state: "TetronimoState") -> bool:
        if self._pos != state._pos:
            return False
        if self.tetronimo != state.tetronimo:
            return False
        if self.next_tetronimo != state.next_tetronimo:
            return False
        if self.saved_tetronimo != state.saved_tetronimo:
            return False
        if self.shape_index != state.shape_index:
            return False
        return True


class Block(object):
    def __init__(self, color: str):
        self.color = color


class Field(object):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.data: List[List[Optional[Block]]] = [[None for _ in range(width)] for _ in range(height)]

    def fits(self, state: TetronimoState) -> bool:
        for rowi, row in enumerate(state.tetronimo.shapes[state.shape_index].data, state.pos.y):
            for coli, v in enumerate(row, state.pos.x):
                if v:
                    if 0 > rowi or rowi >= self.height:
                        return False
                    if 0 > coli or coli >= self.width:
                        return False
                    if self.data[rowi][coli] is not None:
                        return False
        return True

    def add(self, state: TetronimoState) -> int:
        for rowi, row in enumerate(state.tetronimo.shapes[state.shape_index].data, state.pos.y):
            for coli, v in enumerate(row, state.pos.x):
                if v:
                    self.data[rowi][coli] = Block(state.tetronimo.color)
        wr = -1
        nb = 0
        for rd in range(-1, -self.height-1, -1):
            if all(self.data[rd]):
                nb += 1
            else:
                if rd != wr:
                    self.data[wr][:] = self.data[rd][:]
                wr -= 1
        for ptr in range(wr, -self.height, -1):
            self.data[ptr][:] = [None] * self.width
        return nb

class CursesRenderer(object):
    def __init__(self, field: Field, parent: "curses.window", aspect: Vec2=None):
        self.aspect = aspect or Vec2(2, 1)
        self.field = field
        self.parent = parent
        win_size = Vec2(self.aspect.x * field.width + 2, self.aspect.y * field.height + 2)
        self.win = parent.derwin(win_size.y, win_size.x, 0, 0)

        width, height = 4, 4
        border = 1
        tetwin_size = Vec2(self.aspect.x * height + 2 * border, self.aspect.y * width + 2 * border)
        self.nextwin = parent.derwin(tetwin_size.y, tetwin_size.x, 0, win_size.x)
        self.swapwin = parent.derwin(tetwin_size.y, tetwin_size.x, tetwin_size.y, win_size.x)
        self.colors: Dict[str, int] = {}
        for ci, (cs, cc) in enumerate(self._curses_colors_map().items()):
            curses.init_pair(ci + 1, cc, curses.COLOR_BLACK)
            self.colors[cs] = ci + 1
        self.ch = curses.ACS_CKBOARD

    @staticmethod
    def _curses_colors_map() -> Dict[str, int]:
        return {
            "red": curses.COLOR_RED,
            "green": curses.COLOR_GREEN,
            "blue": curses.COLOR_BLUE,
            "yellow": curses.COLOR_YELLOW,
            "cyan": curses.COLOR_CYAN,
            "purple": curses.COLOR_MAGENTA,
            "orange": curses.COLOR_WHITE,
        }

    def render_init(self) -> None:
        self.win.box()
        self.win.refresh()
        self.nextwin.box()
        self.swapwin.box()
        self.nextwin.refresh()
        self.swapwin.refresh()

    def render_next(self, tetro: Tetronimo, clear: bool=False):
        self._render_tetronimo(self.nextwin, 0, 0, tetro, 0, clear)

    def render_swap(self, tetro: Tetronimo, clear: bool=False):
        self._render_tetronimo(self.swapwin, 0, 0, tetro, 0, clear)

    def render_tetronimo_shape(self, state: TetronimoState, clear: bool=False):
        self._render_tetronimo(self.win, state.pos.y, state.pos.x, state.tetronimo, state.shape_index, clear)

    def _render_tetronimo(self, win: "curses.window", y: int, x: int, tetro: Tetronimo, shape_index: int, clear: bool):
        color = 0 if clear else curses.color_pair(self.colors[tetro.color])
        win.attrset(color)
        ch = " " if clear else self.ch
        for rowi, row in enumerate(tetro.shapes[shape_index].data, y):
            for coli, v in enumerate(row, x):
                if v:
                    self._render_block(win, ch, rowi, coli)


    def _render_block(self, win, ch, row, col) -> None:
        ystart, xstart = self.aspect.y * row, self.aspect.x * col
        for y in range(ystart, ystart + self.aspect.y):
            for x in range(xstart, xstart + self.aspect.x):
                win.addch(1 + y, 1 + x, ch)

    def render_field(self) -> None:
        self.win.attrset(0)
        self.win.clear()
        self.win.box()
        for rowi, row in enumerate(self.field.data):
            for coli, block in enumerate(row):
                if block:
                    self.win.attrset(curses.color_pair(self.colors[block.color]))
                self._render_block(self.win, self.ch if block else " ", rowi, coli)


class PlayerAction(enum.IntFlag):
    NONE = 0
    LEFT = enum.auto()
    RIGHT = enum.auto()
    DOWN = enum.auto()
    DROP = enum.auto()
    CHANGE = enum.auto()
    SWAP = enum.auto()
    PAUSE = enum.auto()


class GameState(object):
    def __init__(self, field: Field, renderer: CursesRenderer):
        self.field = field
        self.renderer = renderer
        self.randomizer = Randomizer(TETRONIMOS)
        self.state = TetronimoState(Vec2(0, 0), self.randomizer.next(), self.randomizer.next(), None, 0)
        self._next_state = TetronimoState(Vec2(0, 0), self.state.tetronimo, self.state.next_tetronimo, self.state.saved_tetronimo, 0)
        self.drop_dt = 1.

        self.time = 0
        self.next_drop_time = self.time + self.drop_dt

    def init_loop(self):
        self.renderer.render_tetronimo_shape(self.state)
        self.renderer.win.refresh()
        self.renderer.render_next(self.state.next_tetronimo)
        self.renderer.nextwin.refresh()

    def _redraw_moved_tetronimos(self, remove: TetronimoState, draw: TetronimoState) -> None:
        self.renderer.render_tetronimo_shape(remove, True)
        self.renderer.render_tetronimo_shape(draw)
        self.renderer.win.refresh()

    def _small_step(self, action: PlayerAction, dt: float) -> bool:
        assert self.state == self._next_state
        assert self.state is not self._next_state
        if not self.field.fits(self.state):
            self.renderer.parent.attrset(curses.A_REVERSE)
            self.renderer.parent.addstr(curses.LINES - 1, 0, "GAME OVER. Press 'Q' to quit.")
            while True:
                ch = self.renderer.parent.getch()
                if ch == ord("q") or ch == ord("Q"):
                    break
            return False
        self.time = self.time + dt

        if action & PlayerAction.LEFT:
            self._next_state.pos.x -= 1
        if action & PlayerAction.RIGHT:
            self._next_state.pos.x += 1
        if action & PlayerAction.DOWN or self.time > self.next_drop_time:
            self._next_state.pos.y += 1
        if action & PlayerAction.CHANGE:
            self._next_state.shape_index = (self._next_state.shape_index + 1) % len(self._next_state.tetronimo.shapes)
        if action & PlayerAction.SWAP:
            if self._next_state.saved_tetronimo is None:
                self._next_state.saved_tetronimo = self._next_state.next_tetronimo
                self._next_state.next_tetronimo = None
            self._next_state.saved_tetronimo, self._next_state.tetronimo = self._next_state.tetronimo, self._next_state.saved_tetronimo
            self._next_state.shape_index = 0

        moved = False

        if self.state != self._next_state:
            if self.field.fits(self._next_state):
                self._redraw_moved_tetronimos(self.state, self._next_state)
                if self.time > self.next_drop_time:
                    self.next_drop_time += self.drop_dt

                if action & PlayerAction.SWAP:
                    if self.state.saved_tetronimo:
                        self.renderer.render_swap(self.state.saved_tetronimo, True)
                    self.renderer.render_swap(self._next_state.saved_tetronimo)
                    if self._next_state.next_tetronimo is None:
                        self._next_state.next_tetronimo = self.randomizer.next()
                    self.renderer.render_next(self.state.next_tetronimo, True)
                    self.renderer.render_next(self._next_state.next_tetronimo)
                    self.renderer.nextwin.refresh()
                    self.renderer.swapwin.refresh()

                self._commit_next_state()
                moved = True
            else:
                self._rollback_state()

        if action & PlayerAction.DROP:
            while self.field.fits(self._next_state):
                self._next_state.pos.y += 1
            self._next_state.pos.y -= 1
            self._freeze_next_state()
            self.next_drop_time = self.time + self.drop_dt

        if self.time > self.next_drop_time and not moved:
            self._next_state.pos.y += 1
            if self.field.fits(self._next_state):
                self._redraw_moved_tetronimos(self.state, self._next_state)
                self._commit_next_state()
                moved = True
                self.next_drop_time += self.drop_dt
            else:
                self._next_state.pos.y -= 1
                self._freeze_next_state()
        return True

    def _freeze_next_state(self):
        assert self.field.fits(self._next_state)
        nb = self.field.add(self._next_state)
        if nb:
            self.renderer.render_field()
        else:
            self.renderer.render_tetronimo_shape(self.state, True)
            self.renderer.render_tetronimo_shape(self._next_state)
        self.renderer.render_next(self.state.next_tetronimo, True)
        self._next_state.tetronimo = self._next_state.next_tetronimo
        self._next_state.shape_index = 0
        self._next_state.next_tetronimo = self.randomizer.next()
        self._next_state.pos.x, self._next_state.pos.y = 0, 0
        self.renderer.render_tetronimo_shape(self._next_state)
        self.renderer.render_next(self._next_state.next_tetronimo)
        self.renderer.win.refresh()
        self.renderer.nextwin.refresh()
        self._commit_next_state()

    def step(self, action: PlayerAction, dt: float) -> bool:
        handled_dt = 0.
        STEP_DT = 0.1
        next_handled_dt = STEP_DT
        while next_handled_dt < dt:
            res = self._small_step(action, STEP_DT)
            if not res:
                return res
            handled_dt = next_handled_dt
            next_handled_dt += STEP_DT
            action = 0
        return self._small_step(action, dt - handled_dt)

    def _commit_next_state(self) -> None:
        self.state, self._next_state = self._next_state, self.state
        self._next_state.copy_from(self.state)

    def _rollback_state(self) -> None:
        self._next_state.copy_from(self.state)


def main():
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    curses.start_color()
    curses.curs_set(False)
    stdscr.keypad(True)
    stdscr.timeout(1)
    field = Field(10, 20)
    renderer = CursesRenderer(field, stdscr)

    renderer.render_init()

    gamestate = GameState(field, renderer)

    gamestate.init_loop()

    walltime = time.time()

    while True:
        ch = stdscr.getch()

        new_walltime = time.time()
        dt = new_walltime - walltime
        walltime = new_walltime

        current_action = PlayerAction.NONE
        if ch == curses.ascii.ESC:
            break
        elif ch == curses.KEY_LEFT:
            current_action |= PlayerAction.LEFT
        elif ch == curses.KEY_RIGHT:
            current_action |= PlayerAction.RIGHT
        elif ch == curses.KEY_UP:
            current_action |= PlayerAction.CHANGE
        elif ch == curses.KEY_DOWN:
            current_action |= PlayerAction.DOWN
        elif ch == curses.ascii.SP:
            current_action |= PlayerAction.DROP
        elif ch == curses.ascii.NL:
            current_action |= PlayerAction.SWAP

        if not gamestate.step(current_action, dt):
            break

    curses.endwin()


try:
    main()
finally:
    curses.endwin()
