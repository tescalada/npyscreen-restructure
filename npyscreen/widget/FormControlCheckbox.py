# encoding: utf-8

from . import checkbox
import weakref


class FormControlCheckbox(checkbox.Checkbox):
    """
    """

    def __init__(self, *args, **kwargs):
        super(FormControlCheckbox, self).__init__(*args, **kwargs)
        self._visible_when_selected = []
        self._not_visible_when_selected = []

    def add_visible_when_selected(self, w):
        """Add a widget to be visible only when this box is selected"""
        self._register(w, vws=True)

    def add_invisible_when_selected(self, w):
        self._register(w, vws=False)

    def _register(self, w, vws=True):
        if vws:
            working_list = self._visible_when_selected
        else:
            working_list = self._not_visible_when_selected

        if w in working_list:
            pass
        else:
            try:
                working_list.append(weakref.proxy(w))
            except TypeError:
                working_list.append(w)

        self.update_dependents()

    def update_dependents(self):
        # This doesn't yet work.
        if self.value:
            for w in self._visible_when_selected:
                w.hidden = False
                w.editable = True
            for w in self._not_visible_when_selected:
                w.hidden = True
                w.editable = False
        else:
            for w in self._visible_when_selected:
                w.hidden = True
                w.editable = False
            for w in self._not_visible_when_selected:
                w.hidden = False
                w.editable = True
        self.parent.display()

    def h_toggle(self, *args):
        super(FormControlCheckbox, self).h_toggle(*args)
        self.update_dependents()



