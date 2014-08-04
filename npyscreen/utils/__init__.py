# encoding: utf-8


import curses
import curses.ascii
import sys


class InputHandler(object):
    "An object that can handle user input"

    def handle_input(self, _input):
        """
        Returns True if input has been dealt with, and no further action needs
        taking.

        First attempts to look up a method in self.input_handers (which is a
        dictionary), then runs the methods in self.complex_handlers (if any),
        which is an array of form (test_func, dispatch_func).

        If test_func(input) returns true, then dispatch_func(input) is called.
        Check to see if parent can handle.
        No further action taken after that point.
        """

        if _input in self.handlers:
            self.handlers[_input](_input)
            return True

        try:
            _unctrl_input = curses.ascii.unctrl(_input)
        except TypeError:
            _unctrl_input = None

        if _unctrl_input and (_unctrl_input in self.handlers):
            self.handlers[_unctrl_input](_input)
            return True

        if not hasattr(self, 'complex_handlers'):
            return False
        else:
            for test, handler in self.complex_handlers:
                if test(_input) is not False:
                    handler(_input)
                    return True
        if hasattr(self, 'parent_widget') and hasattr(self.parent_widget, 'handle_input'):
            if self.parent_widget.handle_input(_input):
                return True
        elif hasattr(self, 'parent') and hasattr(self.parent, 'handle_input'):
            if self.parent.handle_input(_input):
                return True

        else:
            pass
        #If we've got here, all else has failed, so:
        return False

    def set_up_handlers(self):
        """
        This function should be called somewhere during object initialisation
        (which all library-defined widgets do). You might like to override this
        in your own definition, but in most cases the `add_handlers` or
        `add_complex_handlers` methods are what you want.
        """
        #called in __init__
        self.handlers = {curses.ascii.NL: self.h_exit_down,
                         curses.ascii.CR: self.h_exit_down,
                         curses.ascii.TAB: self.h_exit_down,
                         curses.KEY_BTAB: self.h_exit_up,
                         curses.KEY_DOWN: self.h_exit_down,
                         curses.KEY_UP: self.h_exit_up,
                         curses.KEY_LEFT: self.h_exit_left,
                         curses.KEY_RIGHT: self.h_exit_right,
                         "^P": self.h_exit_up,
                         "^N": self.h_exit_down,
                         curses.ascii.ESC: self.h_exit_escape,
                         curses.KEY_MOUSE: self.h_exit_mouse}

        self.complex_handlers = []

    def add_handlers(self, handler_dictionary):
        """
        Update the dictionary of simple handlers. Pass in a dictionary with
        keyname (eg "^P" or curses.KEY_DOWN) as the key, and the function that
        key should call as the values
        """
        self.handlers.update(handler_dictionary)

    def add_complex_handlers(self, handlers_list):
        """add complex handlers: format of the list is pairs of
        (test_function, callback) sets"""

        for pair in handlers_list:
            assert len(pair) == 2
        self.complex_handlers.extend(handlers_list)

    def remove_complex_handler(self, test_function):
        _new_list = []
        for pair in self.complex_handlers:
            if not pair[0] == test_function:
                _new_list.append(pair)
        self.complex_handlers = _new_list

################################################################################
# Handler Methods here - npc convention - prefix with h_

    def h_exit_down(self, _input):
        """
        Called when user leaves the widget to the next widget
        """
        self.editing = False
        self.how_exited = EXITED_DOWN

    def h_exit_right(self, _input):
        self.editing = False
        self.how_exited = EXITED_RIGHT

    def h_exit_up(self, _input):
        """Called when the user leaves the widget to the previous widget"""
        self.editing = False
        self.how_exited = EXITED_UP

    def h_exit_left(self, _input):
        self.editing = False
        self.how_exited = EXITED_LEFT

    def h_exit_escape(self, _input):
        self.editing = False
        self.how_exited = EXITED_ESCAPE

    def h_exit_mouse(self, _input):
        mouse_event = self.parent.safe_get_mouse_event()
        if mouse_event and self.intersted_in_mouse_event(mouse_event):
            self.handle_mouse_event(mouse_event)
        else:
            if mouse_event:
                curses.ungetmouse(*mouse_event)
                ch = self.parent.curses_pad.getch()
                assert ch == curses.KEY_MOUSE
            self.editing = False
            self.how_exited = EXITED_MOUSE


class _LinePrinter(object):
    """
    A base class for printing lines to the screen.
    Do not use directly. For internal use only.
    Experimental.
    """
    def find_width_of_char(self, ch):
        # will eventually need changing.
        return 1

    def _print_unicode_char(self, ch, force_ascii=None):
        if hasattr(self, '_force_ascii') and force_ascii is None:
            force_ascii = self._force_ascii
        # return the ch to print.  For python 3 this is just ch
        if force_ascii:
            return ch.encode('ascii', 'replace')
        elif sys.version_info[0] >= 3:
            return ch
        else:
            return ch.encode('utf-8', 'replace')

    def add_line(self, realy, realx,
                unicode_string,
                attributes_list, max_columns,
                force_ascii=False):
        if isinstance(unicode_string, bytes):
            raise ValueError("This class prints unicode strings only.")

        if len(unicode_string) != len(attributes_list):
            raise ValueError("Must supply an attribute for every character.")

        column = 0
        place_in_string = 0

        if hasattr(self, 'curses_pad'):
            # we are a form
            print_on = self.curses_pad
        else:
            # we are a widget
            print_on = self.parent.curses_pad

        while column <= (max_columns - 1):
            try:
                width_of_char_to_print = self.find_width_of_char(unicode_string[place_in_string])
            except IndexError:
                break
            if column - 1 + width_of_char_to_print > max_columns:
                break
            try:
                print_on.addstr(realy,
                                realx + column,
                                self._print_unicode_char(unicode_string[place_in_string]),
                                attributes_list[place_in_string])
            except IndexError:
                break
            column += width_of_char_to_print
            place_in_string += 1

    def make_attributes_list(self, unicode_string, attribute):
        """
        A convenience function.  Retuns a list the length of the unicode_string
        provided, with each entry of the list containing a copy of attribute.
        """
        if isinstance(unicode_string, bytes):
            raise ValueError("This class is intended for unicode strings only.")

        atb_array = []
        ln = len(unicode_string)
        for x in range(ln):
            atb_array.append(attribute)
        return atb_array