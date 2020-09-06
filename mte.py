import curses
import loc_constants as const
from typing import List
# constants


def main(stdscr):
    # TODO loading from files
    contents: List[List[str]] = [[]]
    char = ""
    special = ""
    while True:
        # getting current cursour coordinates
        x: int
        y: int
        y, x = stdscr.getyx()

        max_x: int
        max_y: int
        max_y, max_x = stdscr.getmaxyx()

        upper_rights = [f"{y}:{x}", ""]  # text in the upper right corner

        # printing the test in the upper right corner
        def print_rights(elements):
            try:
                for num, el in enumerate(elements):
                    stdscr.addstr(num*2, max_x - len(el) - 2, el)
                stdscr.move(y, x)
                stdscr.refresh()
            except Exception:
                pass

        print_rights(upper_rights)

        # getting a key
        char: str = stdscr.getkey()

        # exit condition default: ^Q
        if char == "\x11" or char == const.A_EXIT:
            try:
                special = "EXIT (y/n)"
                upper_rights[1] = special
                print_rights(upper_rights)
                accept = stdscr.getkey()
                accepted = {"y", "Y", " ", "    "}
                if accept in accepted:
                    exit()
                else:
                    special = "not exiting"
                    upper_rights[1] = special
            except Exception:
                pass

        # printing  ascii characters
        if len(char) == 1 and ord(char) in range(32, 256) and char != "\x0a":
            try:
                contents[y].insert(x, char)
                y, x = y, x + 1
            except Exception:
                pass

        # newline
        elif char == "\n":
            try:
                if x == len(contents[y]):   # newline in the end of a line
                    contents.insert(y + 1, [])
                else:   # newline in the middle of a line
                    popped_value = contents[y][x:]
                    contents.insert(y + 1, popped_value)
                    del popped_value
                y, x = y + 1, 0
            except Exception:
                pass

        # backspace
        elif char == "\x08" or char == "^?":
            try:
                if not (y == 0 and x == 0):  # cant delete nothing
                    if x > 0:   # standard backspace
                        contents[y].pop(x-1)
                        y, x = y, x - 1
                        stdscr.refresh()
                    else:   # backspace on a newline
                        popped_value = contents.pop(y)
                        if popped_value != "" and y != 0:
                            for el in popped_value:
                                contents[y-1].append(el)
                            y, x = y - 1, len(contents[y - 1])
            except Exception:
                pass

        # keys default: arrows or ^ESDF
        elif char == "KEY_UP" or char == "\x05" or char == const.A_UP:
            try:
                if y > 0:
                    if len(contents[y - 1]) >= x:
                        y, x = y - 1, x
                    else:
                        y, x = y-1, len(contents[y - 1])
            except Exception:
                pass
        elif char == "KEY_DOWN" or char == "\x04" or char == const.A_DOWN:
            try:
                if y < len(contents) - 1:
                    if len(contents[y + 1]) >= x:
                        y, x = y + 1, x
                    else:
                        y, x = y + 1, len(contents[y + 1])
            except Exception:
                pass
        elif char == "KEY_LEFT" or char == "\x13" or char == const.A_LEFT:
            try:
                if not (y == 0 and x == 0):
                    if x != 0:
                        y, x = y, x - 1
                    else:
                        y, x = y - 1, len(contents[y - 1])
            except Exception:
                pass
        elif char == "KEY_RIGHT" or char == "\x06" or char == const.A_RIGHT:
            try:
                if not (y == len(contents) - 1 and x == len(contents[y])):
                    if x != len(contents[y]):
                        y, x = y, x + 1
                    else:
                        y, x = y + 1, 0
            except Exception:
                pass
        # printing the contents to screen
        stdscr.clear()
        print_rights(upper_rights)
        for num, line in enumerate(contents):
            stdscr.addstr(num, 0, "".join(line))
        stdscr.move(y, x)


curses.wrapper(main)
