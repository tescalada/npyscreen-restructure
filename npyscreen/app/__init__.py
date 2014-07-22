# encoding: utf-8

"""
The npyscreen.app package provides Application classes which are the basis for
creating terminal applications using npyscreen.

The following classes are provided in this package:

SimpleApp   - rudimentary application class that should only be used for special
              or very simple cases.

App         - standard application class that manages multiple forms.
AdvancedApp - experimental, does nothing right now!
"""


import curses
import weakref

from .. import safewrapper


class AlreadyOver(Exception):  # Where is this used?
    pass


class SimpleApp(object):
    _run_called = 0

    def main(self):
        """Overload this method to create your application"""

    def resize(self):
        pass

    def __remove_argument_call_main(self, screen, enable_mouse=True):
        # screen disgarded.
        if enable_mouse:
            curses.mousemask(curses.ALL_MOUSE_EVENTS)
        del screen
        return self.main()

    def run(self, fork=None):
        """Run application.  Calls Mainloop wrapped properly."""
        if fork is None:
            return safewrapper.wrapper(self.__remove_argument_call_main)
        else:
            return safewrapper.wrapper(self.__remove_argument_call_main,
                                           fork=fork)


class App(SimpleApp):
    """
    This class is intended to make it easier to create applications with many
    screens. With this in mind, consider the following:

    1. The programmer should not now select which Form to display, instead they
       should set the `next_active_form` class variable. See the register_form
       method for details.

       Doing so will avoid accidentally exceeding the maximum recursion depth.
       Forms themselves should be placed under the management of the class
       instance using the `add_form` or `add_form_class` method.

       NB.  * Applications should therefore use this mechanism in preference to
       calling the .edit() method of any form. *

    2. Forms that are managed by this class can access a proxy to the parent
       application through their `parent_app` attribute, which is created by
       this class.

    3. If the programmer wishes to sidestep the standard form editing loop, then
       they may override the `activate` method of the Form class and its parent
       App instance will call that method instead of the standard edit loop.

       Alternatively (and preferred) the programmer may supply `before_editing`
       and `after_editing` method which will be called just before and just
       after the edit loop respectively.

       **How and why should this be distinguished from `pre_edit_loop` and
       `post_edit_loop` modifications in the form edit loop. I would imagine
       that it has to do with the context... if you wish actions to belong to
       the form, modify the form; if you wish actions belong to the app, modify
       the app**

    4. The method `on_in_main_loop` is called after each screen has exited.
       This can be overridden.

    5. This method should be able to see which screen was last active using the
       `self._last_active_form` attribute, which is only set
       just before each screen is displayed.

    6. Unless you override the attribute `STARTING_FORM`, the first form to be
       called should be named `MAIN`

    7. Override the `on_start` and `on_clean_exit` functions if you wish.
    """

    STARTING_FORM = "MAIN"

    def __init__(self):
        super(App, self).__init__()
        self._form_visit_list = []
        #holds a form id (not class); set by add_form
        self.next_active_form = self.__class__.STARTING_FORM
        self._last_active_form = None
        self._forms = {}

    def add_form_class(self, f_id, form_class, *args, **keywords):
        self._forms[f_id] = [form_class, args, keywords]

    def add_form(self, f_id, form_class, *args, **keywords):
        """
        Create a form of the given class. f_id should be a string which will
        uniquely identify the form. *args will be passed to the Form
        constructor.

        Forms created in this way are handled entirely by the App class.
        """
        fm = form_class(parent_app=self, *args, **keywords)
        self.register_form(f_id, fm)
        return weakref.proxy(fm)

    def register_form(self, f_id, fm):
        """
        f_id should be a string which should uniquely identify the form.

        fm should be a Form.
        """
        fm.parent_app = weakref.proxy(self)
        self._forms[f_id] = fm

    def remove_form(self, f_id):
        del self._forms[f_id].parent_app
        del self._forms[f_id]

    def get_form(self, name):
        f = self._forms[name]
        try:
            return weakref.proxy(f)
        except:
            return f

    def set_next_form(self, fmid):
        """Set the form that will be selected when the current one exits."""
        self.next_active_form = fmid

    def switch_form(self, fmid):
        """Immediately switch to the form specified by fmid."""
        self._THISFORM.editing = False
        self.set_next_form(fmid)
        self.switch_form_now()

    def switch_form_now(self):
        self._THISFORM.editing = False
        try:
            self._THISFORM._widgets__[self._THISFORM.editw].editing = False
        except (AttributeError, IndexError):
            pass
        # Following is necessary to stop two keypresses being needed for titlefields
        try:
            self._THISFORM._widgets__[self._THISFORM.editw].entry_widget.editing = False
        except (AttributeError, IndexError):
            pass

    def remove_last_form_from_history(self):
        self._form_visit_list.pop()
        self._form_visit_list.pop()

    def switch_form_previous(self, backup=STARTING_FORM):
        self.set_next_form_previous()
        self.switch_form_now()

    def set_next_form_previous(self, backup=STARTING_FORM):
        try:
            if self._THISFORM.FORM_NAME == self._form_visit_list[-1]:
                #Remove the current form. if it is at the end of the list
                self._form_visit_list.pop()
            if self._THISFORM.FORM_NAME == self.next_active_form:
                #Take no action if it looks as if someone has already set the
                #next form.
                #Switch to the previous form if one exists
                self.set_next_form(self._form_visit_list.pop())
        except IndexError:
            self.set_next_form(backup)

    def get_history(self):
        return self._form_visit_list

    def reset_history(self):
        self._form_visit_list = []

    def main(self):
        """
        Call this function to start your application, usually called indirectly
        through the function `run`.

        You should not override this function, but override the
        `on_in_main_loop`, `on_start` and `on_clean_exit` methods instead if you
        need to modify the application's behavior.

        When this method is called, it will activate the form named by the class
        variable `STARTING_FORM`. By default this Form will be called 'MAIN'.

        When that form exits (user selecting an ok button or the like), the form
        named by object variable `next_active_form` will be activated.

        If `next_active_form` is None (or otherwise evaluates False), the `main`
        loop will exit.

        The form selected will be edited using it's `edit` method UNLESS it has
        been provided with an `activate` method, in which case that method will
        be called instead.  This is done so that the same class of form can be
        made App aware and have the normal SimpleApp `edit` loop.

        After a Form has been edited its `after_editing` method will be called,
        unless it was invoked with the `activate` method. A similar
        `before_editing` method will be called prior to editing the form. Again,
        the presence of an `activate` method will override this behavior.

        Note that `next_active_form` is a string that is the name of the form
        that was specified when `add_form` or `register_form` was called.
        """

        self.on_start()
        #Why test for nonempty string? Why not just test boolean?
        #Then any value for next_active_form which is False in a boolean
        #expression would stop loop
        #while self.next_active_form != "" and self.next_active_form is not None:
        while self.next_active_form:
            self._last_active_form = self._forms[self.next_active_form]
            #self.LAST_ACTIVE_FORM_NAME = self.next_active_form
            try:
                Fm, args, kwargs = self._forms[self.next_active_form]
                self._THISFORM = Fm(parent_app=self, *args, **kwargs)
            except TypeError:
                self._THISFORM = self._forms[self.next_active_form]
            self._THISFORM.FORM_NAME = self.next_active_form
            self.ACTIVE_FORM_NAME = self.next_active_form
            if len(self._form_visit_list) > 0:
                if self._form_visit_list[-1] != self.next_active_form:
                    self._form_visit_list.append(self.next_active_form)
            else:
                self._form_visit_list.append(self.next_active_form)
            #self._THISFORM._resize()
            #I think checking for methods in classes like this is really weird
            #and unnecessary in most cases, but in this one I don't see a
            #better (less convoluted way). Revisit later, note that I did change
            #similar uses situation below
            if hasattr(self._THISFORM, "activate"):
                self._THISFORM._resize()
                self._THISFORM.activate()
            else:
                self._THISFORM.before_editing()
                self._THISFORM._resize()
                self._THISFORM.edit()
                self._THISFORM.after_editing()
                #if hasattr(self._THISFORM, "beforeEditing"):
                #    self._THISFORM.beforeEditing()
                #self._THISFORM._resize()
                #self._THISFORM.edit()
                #if hasattr(self._THISFORM, "afterEditing"):
                #    self._THISFORM.afterEditing()

            self.on_in_main_loop()
        self.on_clean_exit()

    def on_in_main_loop(self):
        """
        Called between each screen while the application is running.

        Not called before the first screen. Override at will.
        """

    def on_start(self):
        """
        Override this method to perform any initialisation.
        """
        pass

    def on_clean_exit(self):
        """
        Override this method to perform any cleanup when application is exiting
        without error.
        """


class AdvancedApp(App):
    """
    EXPERIMENTAL and NOT for use.

    This class of application will eventually replace the  standard method of
    user input handling and deal with everything at the application level.
    """

    def _main_loop(self):
        pass