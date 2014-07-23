# encoding: utf-8

from .textbox import Textfield
from . import titlefield


class PasswordEntry(Textfield):
    def _print(self):
        strlen = len(self.value)
        if self.maximum_string_length < strlen:
            tmp_x = self.relx
            for i in range(self.maximum_string_length):
                self.parent.curses_pad.addch(self.rely, tmp_x, '-')
                tmp_x += 1

        else:
            tmp_x = self.relx
            for i in range(strlen):
                self.parent.curses_pad.addstr(self.rely, tmp_x, '-')
                tmp_x += 1


class TitlePassword(titlefield.TitleText):
    _entry_type = PasswordEntry
