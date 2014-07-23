# encoding: utf-8

"""
The npyscreen.widget package provides tools for Widgets and Widget classes.
"""

import copy
import sys
import curses
import curses.ascii
import weakref
from .. import global_options
import locale

#import warnings  # unused
#import curses.wrapper  #unused
#import codecs  # unused

from ..globals import DEBUG

from .constants import *

from .widget import Widget, DummyWidget
from .button import MiniButton, MiniButtonPress
Button, ButtonPress = MiniButton, MiniButtonPress  # Alias MiniButton[Press]
from .textbox import Textfield, FixedText
from .titlefield import TitleText, TitleFixedText
from .password import PasswordEntry, TitlePassword
from .slider import Slider, TitleSlider
from .multiline import MultiLine, Pager, TitleMultiLine, TitlePager,\
                       MultiLineAction, BufferPager, TitleBufferPager
from .multiselect import MultiSelect, TitleMultiSelect, MultiSelectFixed,\
                         TitleMultiSelectFixed, MultiSelectAction
from .editmultiline import MultiLineEdit
from .combobox import ComboBox, TitleCombo
from .checkbox import Checkbox, RoundCheckBox, CheckBoxMultiline,\
                      RoundCheckBoxMultiline, CheckBox, CheckboxBare
from .FormControlCheckbox import FormControlCheckbox
from .autocomplete import TitleFilename, Filename, Autocomplete
#from .Menu import Menu  # Is this appropriate
from .select import SelectOne, TitleSelectOne
from .datecombo import DateCombo, TitleDateCombo
from .multilinetree import MultiLineTree, SelectOneTree, MultiLineTreeNew,\
                           MultiLineTreeNewAction, TreeLine, MLTree,\
                           MLTreeAnnotated, MLTreeAction,\
                           TreeLineAnnotated, MultiLineTreeNewAnnotatedAction,\
                           MultiLineTreeNewAnnotated, MLTreeAnnotatedAction

#Experimental Widgets (take care and report issues!)
from .multilinetreeselectable import MLTreeMultiSelect, TreeLineSelectable
from .multilinetreeselectable import MLTreeMultiSelectAnnotated,\
                                     TreeLineSelectableAnnotated
from .filenamecombo import FilenameCombo, TitleFilenameCombo
from .annotatetextbox import AnnotateTextboxBaseRight
from .multiline import MultiLineActionWithShortcuts
from .multilineeditable import MultiLineEditable, MultiLineEditableTitle,\
                               MultiLineEditableBoxed
from .monthbox import MonthBox
from .grid import SimpleGrid
from .gridcoltitles import GridColTitles
from .boxwidget import BoxBasic, BoxTitle
from .NewMenu                 import NewMenu, MenuItem
from .NMenuDisplay            import MenuDisplay, MenuDisplayScreen

#Where should the menu code really go? should it be a widget subpackage?
