# encoding: utf-8

"""
The npyscreen.form package provides Form classes and utilities for creating
custom Forms. These Forms are added to Apps and represent a unit of display
content (of which Widgets are the subunits).
"""

from .form import FormBaseNew, Form, TitleForm, TitleFooterForm, SplitForm,\
                  FormExpanded, FormBaseNewExpanded
from .actionform import ActionForm, ActionFormExpanded
from .formwithmenus import FormWithMenus, ActionFormWithMenus,\
                           FormBaseNewWithMenus, SplitFormWithMenus
from .popup import Popup, MessagePopup, ActionPopup, PopupWide, ActionPopupWide
from .formmutt import FormMutt, FormMuttWithMenus
from .fileselector import FileSelector, selectFile
from .formmuttactive import ActionControllerSimple, TextCommandBox,\
                            FormMuttActive, FormMuttActiveWithMenus
from .formmultipage import FormMultiPage, FormMultiPageAction,\
                           FormMultiPageActionWithMenus, FormMultiPageWithMenus
