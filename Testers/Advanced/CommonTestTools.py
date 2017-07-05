#######################################
#                                     #
# Common Widget Tester Tools          #
# Written by Ryan Eggers              #
# Copyright 2017 Abetter Automation   #
#                                     #
#######################################

import Tkinter
import tkFont
import tkMessageBox
from ttk import Separator
from inspect import getdoc, getargspec


def getwidgetname(widget, fullyqualified=False):
    name = widget.__class__.__name__
    if fullyqualified:
        name = ".".join([widget.__class__.__module__, name])
    return name


def getfunctionsignature(func):
    argspec = getargspec(func)
    args = argspec[0]
    varargs = argspec[1]
    kwargs = argspec[2]
    defaults = list(argspec[3])
    argsig = ""
    if kwargs:
        argsig = "**" + kwargs
    if varargs:
        sep = ["", ", "][len(argsig) > 0]
        argsig = sep.join("*" + varargs, argsig)
    while len(args):
        arg = args.pop()
        try:
            default = defaults.pop()
        except IndexError:
            pass
        else:
            arg = "=".join([arg, str(default)])
        sep = ["", ", "][len(argsig) > 0]
        argsig = sep.join([arg, argsig])
    return func.__name__ + "(" + argsig + ")"


def showinfo(module):
    about_title = "About %s Tester" % module
    about_msg = "This tool is intended to provide an\n"
    about_msg += "interactive interface from which to\n"
    about_msg += "visualize & test the Viewidget %s." % module
    about_msg += "\n\nCopyright (c) 2017 Abetter Automation."
    tkMessageBox.showinfo(about_title, about_msg)


def gettextwidth(text, family=None, size=None):
    if family and size:
        width = tkFont.Font(family=family, size=size).measure(text)
    elif family:
        width = tkFont.Font(family=family).measure(text)
    else:
        width = tkFont.Font().measure(text)
    return width


class WidgetData(object):
    def __init__(self, widget=None, **data):
        self.widget = widget
        self.dataframe = Tkinter.Frame()
        row = 0
        for name, value in data.items():
            self.add_datablock(row, name, value)
            row += 1

    def add_datablock(self, row, name, value):
        Tkinter.Label(self.dataframe, text=name).grid(row=row, column=0)
        Tkinter.Label(self.dataframe, text=value).grid(row=row, column=1)


class WidgetBlock(Tkinter.Frame):
    def __init__(self, master, *widgetdata):
        Tkinter.Frame.__init__(self, master)
        self.add_widgetdata(*widgetdata)

    def add_widgetdata(self, *widgetdata):
        n = len(widgetdata)
        for i in range(n):
            # row = [0,3][i%2]
            # col = (i//2)*3
            row = (i // 2) * 2
            col = [0, 3][i % 2]
            widgetdata[i].widget.grid(in_=self, row=row, column=col)
            widgetdata[i].dataframe.grid(in_=self, row=row, column=col + 1)
            if col == 0 and n - i > 3:
                # Separator(self, orient=Tkinter.VERTICAL).grid(row=row, column=col+2, rowspan=3, sticky='ns')
                Separator(self, orient=Tkinter.HORIZONTAL).grid(row=row + 1, column=col, columnspan=5, sticky='ew')
        if n > 1:
            # Separator(self, orient=Tkinter.HORIZONTAL).grid(row=1, columnspan=(n//2)*3, sticky='ew')
            Separator(self, orient=Tkinter.VERTICAL).grid(row=0, column=2, rowspan=row + 1, sticky='ns')


class ErrorDisplay(Tkinter.Canvas):
    """Canvas extension to display text when user enters bad value; replaces Viewidget Canvas object in case of error"""

    def __init__(self, master, size, error=None):
        Tkinter.Canvas.__init__(self, master, width=size, height=size, borderwidth=0, highlightthickness=0)
        self.create_text(size / 2, size / 2, text='CANNOT\n DISPLAY\n  IMAGE')
        if error:
            self.create_text(size / 2, size, text='ERROR: ' + str(error), fill='red', width=size)
