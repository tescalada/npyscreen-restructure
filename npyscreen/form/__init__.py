# encoding: utf-8

"""
The npyscreen.form package provides Form classes and utilities for creating
custom Forms. These Forms are added to Apps and represent a unit of display
content (of which Widgets are the subunits).
"""

from .Form import FormBaseNew, Form, TitleForm, TitleFooterForm, SplitForm,\
                    FormExpanded, FormBaseNewExpanded
from .ActionForm import ActionForm, ActionFormExpanded
from .FormWithMenus import FormWithMenus, ActionFormWithMenus,\
                          FormBaseNewWithMenus, SplitFormWithMenus
from .Popup import Popup, MessagePopup, ActionPopup, PopupWide, ActionPopupWide
from .FormMutt import FormMutt, FormMuttWithMenus
from .FileSelector import FileSelector, selectFile
from .FormMuttActive import ActionControllerSimple, TextCommandBox,\
                            FormMuttActive, FormMuttActiveWithMenus
from .FormMultiPage import FormMultiPage, FormMultiPageAction,\
                           FormMultiPageActionWithMenus, FormMultiPageWithMenus




