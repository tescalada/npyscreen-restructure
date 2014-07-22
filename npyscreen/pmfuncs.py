# encoding: utf-8

import curses
import os


class ResizeError(Exception):
    "The screen has been resized"


def hide_cursor():
    try:
        curses.curs_set(0)
    except:
        pass


def show_cursor():
    try:
        curses.curs_set(1)
    except:
        pass


def call_subshell(subshell):
    """
    Call this function if you need to execute an external command in a subshell
    (os.system).  All the usual warnings apply -- the command line will be
    expanded by the shell, so make sure it is safe before passing it to this
    function.
    """
    curses.def_prog_mode()
    #curses.endwin() # Probably causes a memory leak.

    rtn = os.system("%s" % (subshell))
    curses.reset_prog_mode()
    if rtn is not 0:
        return False
    else:
        return True
