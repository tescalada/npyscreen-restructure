# encoding: utf-8

from . import form
#from . import fmForm
#from . import fmActionForm
#import curses  # unused


class Popup(form.Form):
    DEFAULT_LINES = 12
    DEFAULT_COLUMNS = 60
    SHOW_ATX = 10
    SHOW_ATY = 2
    #def __init__(self,
    #    lines = 12,
    #    columns=60,
    #    minimum_lines=None,
    #    minimum_columns=None,
    #    *args, **kwargs):
    #    super(Popup, self).__init__(lines = lines, columns=columns,
    #    *args, **kwargs)
    #    self.show_atx = 10
    #    self.show_aty = 2


class ActionPopup(form.ActionForm, Popup):
    def __init__(self, *args, **kwargs):
        Popup.__init__(self, *args, **kwargs)


class MessagePopup(Popup):
    def __init__(self, *args, **kwargs):
        from . import wgmultiline as multiline
        super(MessagePopup, self).__init__(*args, **kwargs)
        self.TextWidget = self.add(multiline.Pager, scroll_exit=True, max_height=self.widget_useable_space()[0]-2)


class PopupWide(Popup):
    DEFAULT_LINES = 14
    DEFAULT_COLUMNS = None
    SHOW_ATX = 0
    SHOW_ATY = 0
    #def __init__(self,
    #    lines = 14,
    #    columns=None,
    #    minimum_lines=None,
    #    minimum_columns=None,
    #    *args, **kwargs):
    #    super(PopupWide, self).__init__(lines = lines, columns=columns,
    #    *args, **kwargs)
    #    self.show_atx = 0
    #    self.show_aty = 0


class ActionPopupWide(form.ActionForm, PopupWide):
    def __init__(self, *args, **kwargs):
        PopupWide.__init__(self, *args, **kwargs)


#Copied over from npyscreen.widget.multiline because this is a form,
#and having it over there was causing circular importing
class FilterPopupHelper(Popup):
    def create(self):
        super(FilterPopupHelper, self).create()
        self.filterbox = self.add(titlefield.TitleText, name='Find:', )
        self.nextrely += 1
        self.statusline = self.add(textbox.Textfield,
                                   color='LABEL',
                                   editable=False)

    def updatestatusline(self):
        self.owner_widget._filter = self.filterbox.value
        filtered_lines = self.owner_widget.get_filtered_indexes()
        len_f = len(filtered_lines)
        #if self.filterbox.value == None or self.filterbox.value == '':
        if self.filterbox.value is None or self.filterbox.value == '':
            self.statusline.value = ''
        elif len_f == 0:
            self.statusline.value = '(No Matches)'
        elif len_f == 1:
            self.statusline.value = '(1 Match)'
        else:
            self.statusline.value = '(%s Matches)' % len_f

    def adjust_widgets(self):
        self.updatestatusline()
        self.statusline.display()
