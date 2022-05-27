############################################
#                                          #
# Digit Widget Functionality Tester        #
# Written by Ryan Eggers                   #
# Copyright 2017 Abetter Automation        #
#                                          #
############################################

import warnings
import time
import tkinter
from tkinter import ttk

from viewidget import Digit, LED

import CommonTestTools as Ctt


class Introduction(tkinter.Frame):
    """Provides an introduction from Digit's docstring"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'Introduction\n'
        innerframe = tkinter.Frame(self)
        widget = Digit(innerframe)
        widget.pack(side='right')
        docframe = tkinter.Frame(innerframe)
        name = Ctt.getwidgetname(widget, True)
        doc = Ctt.getdoc(widget)
        tkinter.Label(docframe, text=name, font=('Helvetica', 16, 'bold')).pack(side='top', pady=2)
        tkinter.Label(docframe, text=doc, justify='left').pack(side='bottom')
        docframe.pack(side='left')
        innerframe.pack(side='left', fill='x', expand=1, padx=50)


class Construction(tkinter.Frame):
    """Provides information on Digit's __init__ function"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'Construction\n'
        innerframe = tkinter.Frame(self)
        widget = Digit(innerframe, size=115, value=8, fg='green')
        widget.pack(side='right')
        docframe = tkinter.Frame(innerframe)
        name = Ctt.getwidgetname(widget) + ".__init__"
        sig = Ctt.getfunctionsignature(widget.__init__)
        doc = Ctt.getdoc(widget.__init__)
        t = '\t'.expandtabs(4)
        doc = t + doc.replace('\n', '\n' + t)
        tkinter.Label(docframe, text=name, font=('Helvetica', 16, 'bold')).pack(side='top', pady=2)
        tkinter.Label(docframe, text='\n'.join([sig, doc]), justify='left').pack(side='bottom')
        docframe.pack(side='left')
        innerframe.pack(side='left', fill='x', expand=1, padx=50)


class SizeValue(tkinter.Frame):
    """Demonstrates Digit configuration functionality: size and value"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'size and\nvalue'

        widget1 = Digit()  # Default: size=100, value=0
        widget2 = Digit(value=None)
        widget3 = Digit(value=1)
        widget4 = Digit(value=9)
        widget5 = Digit(size=50, value=2)
        widget6 = Digit(size=50, value='A')
        widget7 = Digit(size=200, value=8)
        widget8 = Digit(size=200, value='F')

        block1 = Ctt.WidgetData(widget1, size=100, value=0)
        block2 = Ctt.WidgetData(widget2, size=100, value='None')
        block3 = Ctt.WidgetData(widget3, size=100, value=1)
        block4 = Ctt.WidgetData(widget4, size=100, value=9)
        block5 = Ctt.WidgetData(widget5, size=50, value=2)
        block6 = Ctt.WidgetData(widget6, size=50, value='A')
        block7 = Ctt.WidgetData(widget7, size=200, value=8)
        block8 = Ctt.WidgetData(widget8, size=200, value='F')
        Ctt.WidgetBlock(self, block1, block2, block3, block4, block5, block6, block7, block8).pack(fill='both',
                                                                                                   expand=1)


class ForegroundBackground(tkinter.Frame):
    """Demonstrates Digit configuration functionality: foreground and background"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'foreground and\nbackground'
        bg_color = 'SystemMenu'

        widget1 = Digit(value=8)  # Default: foreground='red', background='black'
        widget2 = Digit(value=8, foreground='black', background='red')
        widget3 = Digit(value=8, foreground='#fff', background='#000')
        widget4 = Digit(value=8, foreground='#fff', background='#f00')
        try:
            widget5 = Digit(value=8, fg='black', bg=bg_color)
        except tkinter.TclError:  # SystemMenu color unknown (probably Linux)
            bg_color = self.cget('bg')
            widget5 = Digit(value=8, fg='black', bg=bg_color)
        widget6 = Digit(value=8, fg='red', bg=bg_color)
        widget7 = Digit(value=8, fg=bg_color, bg='blue')
        widget8 = Digit(value=8, fg='purple', bg='pink')

        block1 = Ctt.WidgetData(widget1, foreground='red', background='black')
        block2 = Ctt.WidgetData(widget2, foreground='black', background='red')
        block3 = Ctt.WidgetData(widget3, foreground='#fff', background='#000')
        block4 = Ctt.WidgetData(widget4, foreground='#fff', background='#f00')
        block5 = Ctt.WidgetData(widget5, fg='black', bg=bg_color)
        block6 = Ctt.WidgetData(widget6, fg='red', bg=bg_color)
        block7 = Ctt.WidgetData(widget7, fg=bg_color, bg='blue')
        block8 = Ctt.WidgetData(widget8, fg='purple', bg='pink')
        Ctt.WidgetBlock(self, block1, block2, block3, block4, block5, block6, block7, block8).pack(fill='both',
                                                                                                   expand=1)


class SetMasks(tkinter.Frame):
    """Demonstrates Digit's low-level set_mask function"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'Setting\nmasks'

        currentmask = 0b1111111
        self.digit = Digit(self, size=200)
        self.digit.set_mask(currentmask)
        self.digit.pack(side='left', padx=50)

        self.maskframe = tkinter.Frame(self)
        self.maskframe.pack(side='left', expand=1, fill='x')

        self.binlabel = tkinter.Label(self.maskframe, text='mask value: ' + bin(currentmask), relief='ridge')
        self.binlabel.pack(pady=5, ipadx=5, ipady=5, anchor='w')

        self.choiceframe = tkinter.Frame(self.maskframe)
        self.choiceframe.pack(anchor='w')
        self.masks = []
        for i in range(7):
            self.masks.append(tkinter.IntVar())
            cbutton = tkinter.Checkbutton(self.choiceframe, text='mask %i' % i, variable=self.masks[i],
                                          command=self.updatemasks)
            cbutton.select()
            cbutton.config(takefocus=False)
            cbutton.pack(side='bottom')
        self.masks.reverse()

    def updatemasks(self):
        currentmask = '0b%i%i%i%i%i%i%i' % tuple([mask.get() for mask in self.masks])
        self.digit.set_mask(eval(currentmask))
        self.binlabel.config(text='mask value: ' + currentmask)


class Demonstration(tkinter.Frame):
    """Allows the user to try out the Digit's features interactively"""

    DEFAULT_CONFIG = dict(size=100,
                          value=0,
                          background='black',
                          foreground='red', )

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'Interactive\nDemonstration'
        self.digit_config = Demonstration.DEFAULT_CONFIG.copy()
        self.digit = Digit(self, **self.digit_config)
        self.digit.pack(side='left', fill='y', expand=1, pady=30)

        # Interact subframe
        self.interactframe = tkinter.Frame(self)
        self.interactframe.pack(side='right', fill='y', expand=1, pady=20)
        tkinter.Label(self.interactframe, text="Please enter Digit options...*").pack(anchor='w', pady=5)
        # Entry frame contains config variable keys as labels and corresponding entry widgets with values of each key
        self.entryframe = tkinter.Frame(self.interactframe)
        row = 0
        for key, value in self.digit_config.items():
            tkinter.Label(self.entryframe, text=key).grid(row=row, column=0)
            ent = tkinter.Entry(self.entryframe, name=key)
            ent.insert(0, str(value))
            ent.bind('<Return>', lambda e: self.refresh())
            ent.grid(row=row, column=1)
            row += 1
        self.entryframe.pack()
        # Reset buttons
        tkinter.Button(self.interactframe, text='Reset', width=10, command=self.reset).pack(pady=10)
        msg = "*Press <enter> after typing in an option\n value to refresh the Digit widget"
        tkinter.Label(self.interactframe, text=msg, justify='left').pack(anchor='w')

    # end init

    def refresh(self):
        """Reads the inputs from the entry widgets and updates the GUI; includes alerts for errors and warnings"""
        # Parse config inputs (catch input eval errors)
        haserror = False
        for key in self.digit_config:
            input = self.entryframe.nametowidget(key).get()
            if key in ['foreground', 'fg', 'background', 'bg']:
                # Config options that takes text: colors - convert to RGB first
                try:
                    self.digit_config[key] = "#%04x%04x%04x" % self.winfo_rgb(input)
                except Exception as error:
                    haserror = True
                    self.entryframe.nametowidget(key).config(bg='red')
                else:
                    self.entryframe.nametowidget(key).config(bg='white')
            elif key == 'value':
                try:
                    self.digit_config[key] = eval(input)
                except Exception:
                    self.digit_config[key] = input
            else:
                try:
                    self.digit_config[key] = eval(input)
                except Exception as error:
                    haserror = True
                    self.entryframe.nametowidget(key).config(bg='red')
                else:
                    self.entryframe.nametowidget(key).config(bg='white')

        # Draw new Digit (catch Digit constructor errors and warnings)
        self.digit.destroy()
        if haserror:
            size = Demonstration.DEFAULT_CONFIG['size']
            self.digit = Ctt.ErrorDisplay(self, size, error)
        else:
            with warnings.catch_warnings(record=True) as warns:
                warnings.simplefilter("always")
                try:
                    self.digit = Digit(self, **self.digit_config)
                except Exception as error:
                    haserror = True
                    size = Demonstration.DEFAULT_CONFIG['size']
                    self.digit = Ctt.ErrorDisplay(self, size, error)
                    for key in self.digit_config:
                        if any(key == word for word in str(error).split(' ')):
                            self.entryframe.nametowidget(key).config(bg='red')
                else:
                    offset = 0
                    for warn in warns:
                        warn_message = str(warn.message)
                        warn_text = 'WARNING: ' + warn_message
                        size = self.digit_config['size']
                        self.digit.create_text(size / 2, size - offset, text=warn_text, fill='gold', width=size)
                        offset += 10 * (Ctt.gettextwidth(warn_text) // size + 2)
                        for key in self.digit_config:
                            if any(key == word for word in warn_message.split(' ')):
                                self.entryframe.nametowidget(key).config(bg='gold')
        self.digit.pack(side='left', fill='y', expand=1, pady=30)

    # end refresh

    def reset(self):
        """Resets back to the default configuration"""
        for key, value in Demonstration.DEFAULT_CONFIG.items():
            ent = self.entryframe.nametowidget(key)
            ent.delete(0, tkinter.END)
            ent.insert(0, str(value))
        self.refresh()


class Advanced(tkinter.Frame):
    """Demonstrates the use of multiple coordinated Digits"""

    FOREGROUND = 'black'
    MASKPATTERN = [0, 3, 5, 1, 4, 2]

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'Advanced\nDesign'
        self.BACKGROUND = self.cget('bg')

        top_frame = tkinter.Frame(self)
        top_frame.pack(pady=50, side='top')
        # spinning Digit
        self.digit = Digit(top_frame, size=65, value=None)
        self.digit.grid(row=0, column=0, padx=10)
        self.update_digit(self.MASKPATTERN[0])
        # message
        msg = "Below is an array of digits performing their quintessential role: A digital clock."
        tkinter.Label(top_frame, text=msg, justify='left').grid(row=0, column=1)

        self.clock = tkinter.Frame(self)
        self.clock.pack()

        self.digits = []
        size = 125
        for i in range(2):
            # digits
            for j in range(2):
                digit = Digit(self.clock, size=size, background=self.BACKGROUND, foreground=self.FOREGROUND)
                digit.pack(side='left')
                self.digits.append(digit)
            # colon in the middle
            if i == 0:
                self.colon = tkinter.Canvas(self.clock, height=size, width=size * 1 / 10, borderwidth=0,
                                            highlightthickness=0, bg=self.BACKGROUND)
                self.colon.create_oval(0, size * 3 / 10, size * 1 / 10, size * 4 / 10, fill=self.FOREGROUND, width=0,
                                       tags='colon')
                self.colon.create_oval(0, size * 7 / 10, size * 1 / 10, size * 8 / 10, fill=self.FOREGROUND, width=0,
                                       tags='colon')
                self.colon.pack(side='left')
        ledframe = tkinter.Frame(self.clock)
        ledframe.pack(side='left', anchor='n', pady=10)
        self.am_pm = LED(ledframe, size=14, casewidth=0, reflectstyle=0, bulbcolor='red')
        self.am_pm.grid(row=0, column=0, ipady=1)
        tkinter.Label(ledframe, text="PM").grid(row=0, column=1)

        self.H, self.M, self.S = None, None, None
        self.update_time()

    def update_digit(self, next_mask):
        self.digit.set_mask(0)
        self.digit.set_mask(2 ** next_mask)
        i = self.MASKPATTERN.index(next_mask) + 1
        if i == len(self.MASKPATTERN):
            i = 0
        self.after(500, self.update_digit, self.MASKPATTERN[i])

    def update_time(self):
        H, M, S = time.strftime('%H:%M:%S').split(':')
        hours = int(H)
        if hours == 0:
            H = '12'
        elif hours > 12:
            H = str(hours - 12)
        else:
            H = str(hours)

        if H != self.H:  # The hour has changed
            # Turn on or off the LED if not in the correct state
            if hours >= 12 and not self.am_pm.state:
                self.am_pm.turnon()
            elif not hours < 12 and self.am_pm.state:
                self.am_pm.turnoff()
            # Update hour digits
            if len(H) == 2:
                self.digits[0].set_value(H[0])
                self.digits[1].set_value(H[1])
            else:
                self.digits[0].set_value(None)
                self.digits[1].set_value(H[0])
            self.H = H
        if M != self.M:
            # update minute digits
            self.digits[2].set_value(M[0])
            self.digits[3].set_value(M[1])
            self.M = M
        if S != self.S:
            # blink colon
            if int(S) % 2:
                self.colon.itemconfig('colon', fill=self.BACKGROUND)
            else:
                self.colon.itemconfig('colon', fill=self.FOREGROUND)
            self.S = S
        self.after(200, self.update_time)


if __name__ == '__main__':
    module = 'Digit'

    TestWindow = tkinter.Tk()
    TestWindow.title('%s Widget Functionality Tester' % module)

    quickmenu = tkinter.Menu(TestWindow)
    TestWindow.config(menu=quickmenu)
    filemenu = tkinter.Menu(quickmenu, tearoff=0)
    quickmenu.add_cascade(label="File", menu=filemenu)
    filemenu.add_command(label="About", command=lambda: Ctt.showinfo(module))
    filemenu.add_command(label="Exit", command=TestWindow.quit)

    tabs = ttk.Notebook(TestWindow)
    tabs.pack(fill='both', expand=1)
    tabframes = []

    # Add tests
    tabframes.append(Introduction(TestWindow))
    tabframes.append(Construction(TestWindow))
    tabframes.append(SizeValue(TestWindow))
    tabframes.append(ForegroundBackground(TestWindow))
    tabframes.append(SetMasks(TestWindow))
    tabframes.append(Demonstration(TestWindow))
    tabframes.append(Advanced(TestWindow))

    for tabframe in tabframes:
        tabs.add(tabframe, text=tabframe.title)

    # Make Window viewable
    TestWindow.focus_set()
    TestWindow.mainloop()
