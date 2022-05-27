############################################
#                                          #
# Dial Widget Functionality Tester         #
# Written by Ryan Eggers                   #
# Copyright 2017 Abetter Automation        #
#                                          #
############################################

import warnings
import tkinter
from tkinter import ttk

from viewidget import Dial, Digit

import CommonTestTools as Ctt


class Introduction(tkinter.Frame):
    """Provides an introduction from Dial's docstring"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'Introduction\n'
        innerframe = tkinter.Frame(self)
        widget = Dial(innerframe, unit='degF')
        widget.pack(side='right')
        docframe = tkinter.Frame(innerframe)
        name = Ctt.getwidgetname(widget, True)
        doc = Ctt.getdoc(widget)
        tkinter.Label(docframe, text=name, font=('Helvetica', 16, 'bold')).pack(side='top', pady=2)
        tkinter.Label(docframe, text=doc, justify='left').pack(side='bottom')
        docframe.pack(side='left')
        innerframe.pack(side='left', fill='x', expand=1, padx=50)


class Construction(tkinter.Frame):
    """Provides information on Dial's __init__ function"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'Construction\n'
        innerframe = tkinter.Frame(self)
        widget = Dial(innerframe, size=275, casewidth=10, min=0, max=100, value=14.7, unit='psi', withdisplay=False)
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


class SizeCasewidthValue(tkinter.Frame):
    """Demonstrates Dial configuration functionality: size, casewidth and value"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'size, casewidth\nand value'

        widget1 = Dial()  # Default: size=300, casewidth=15, value=min
        widget2 = Dial(size=150, casewidth=7, value=220)
        widget3 = Dial(size=200, casewidth=12, value=120)
        widget4 = Dial(size=200, casewidth=6, value=160)

        block1 = Ctt.WidgetData(widget1, size=300, casewidth=15, value=60)
        block2 = Ctt.WidgetData(widget2, size=150, casewidth=7, value=220)
        block3 = Ctt.WidgetData(widget3, size=200, casewidth=12, value=120)
        block4 = Ctt.WidgetData(widget4, size=200, casewidth=6, value=160)
        Ctt.WidgetBlock(self, block1, block2, block3, block4).pack(fill='both', expand=1)


class StartExtentMinMax(tkinter.Frame):
    """Demonstrates Dial configuration functionality: start, extent, min, and max"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'start/extent and\nmin/max'

        widget1 = Dial()  # Default: start=225, extent=-270, min=60, max=220
        widget2 = Dial(min=0, max=100)
        widget3 = Dial(start=180, extent=-180)
        widget4 = Dial(start=180, extent=180, min=0, max=100)

        block1 = Ctt.WidgetData(widget1, start=225, extent=-270, min=60, max=220)
        block2 = Ctt.WidgetData(widget2, start=225, extent=-270, min=0, max=100)
        block3 = Ctt.WidgetData(widget3, start=180, extent=-180, min=60, max=220)
        block4 = Ctt.WidgetData(widget4, start=180, extent=180, min=0, max=100)
        Ctt.WidgetBlock(self, block1, block2, block3, block4).pack(fill='both', expand=1)


class ScaleUnit(tkinter.Frame):
    """Demonstrates Dial configuration functionality: majorscale, semimajorscale, minorscale, and unit"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'scale and unit\n(markings)'

        widget1 = Dial()  # Default: majorscale=20, semimajorscale=10, minorscale=2, unit=None
        widget2 = Dial(semimajorscale=0, minorscale=0, unit='psi')
        widget3 = Dial(majorscale=40, semimajorscale=5, minorscale=1, unit='degF')
        widget4 = Dial(majorscale=15, semimajorscale=0, minorscale=4, unit='degC')

        block1 = Ctt.WidgetData(widget1, majorscale=20, semimajorscale=10, minorscale=2, unit='None')
        block2 = Ctt.WidgetData(widget2, majorscale=20, semimajorscale=0, minorscale=0, unit='psi')
        block3 = Ctt.WidgetData(widget3, majorscale=40, semimajorscale=5, minorscale=1, unit='degF')
        block4 = Ctt.WidgetData(widget4, majorscale=15, semimajorscale=0, minorscale=4, unit='degC')
        Ctt.WidgetBlock(self, block1, block2, block3, block4).pack(fill='both', expand=1)


class BoundWithdisplay(tkinter.Frame):
    """Demonstrates Dial configuration functionality: bound and withdisplay"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'bound and\nwithdisplay'

        widget1 = Dial(value=55)  # Default: bound=True, withdisplay=True
        widget2 = Dial(bound=False, value=55)
        widget3 = Dial(withdisplay=False, value=225)
        widget4 = Dial(bound=False, withdisplay=False, value=225)

        block1 = Ctt.WidgetData(widget1, bound=True, withdisplay=True, value=50)
        block2 = Ctt.WidgetData(widget2, bound=False, withdisplay=True, value=50)
        block3 = Ctt.WidgetData(widget3, bound=True, withdisplay=False, value=225)
        block4 = Ctt.WidgetData(widget4, bound=False, withdisplay=False, value=225)
        Ctt.WidgetBlock(self, block1, block2, block3, block4).pack(fill='both', expand=1)


class Demonstration(tkinter.Frame):
    """Allows the user to try out the Dial's features interactively"""

    DEFAULT_CONFIG = dict(size=300,
                          casewidth=15,
                          start=225,
                          extent=-270,
                          min=60,
                          max=220,
                          majorscale=20,
                          semimajorscale=10,
                          minorscale=2,
                          unit=None,
                          withdisplay=True,
                          bound=True,
                          value=60)

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'Interactive\nDemonstration'

        self.dial_config = Demonstration.DEFAULT_CONFIG.copy()
        self.dial = Dial(self, **self.dial_config)
        self.dial.pack(side='left', fill='y', expand=1, pady=20)

        # Interact subframe
        self.interactframe = tkinter.Frame(self)
        self.interactframe.pack(side='right', fill='y', expand=1, pady=10)
        tkinter.Label(self.interactframe, text="Please enter Dial options...*").pack(anchor='w', pady=5)
        # Entry frame contains config variable keys as labels and corresponding entry widgets with values of each key
        self.entryframe = tkinter.Frame(self.interactframe)
        row = 0
        for key, value in self.dial_config.items():
            tkinter.Label(self.entryframe, text=key).grid(row=row, column=0)
            ent = tkinter.Entry(self.entryframe, name=key)
            ent.insert(0, str(value))
            ent.bind('<Return>', lambda e: self.refresh())
            ent.grid(row=row, column=1)
            row += 1
        self.entryframe.pack()
        # Reset and animate buttons
        self.animate_button = tkinter.Button(self.interactframe, text='Animate', width=10,
                                             command=lambda: Animation(self, **self.dial_config))
        self.animate_button.pack(pady=10)
        tkinter.Button(self.interactframe, text='Reset', width=10, command=self.reset).pack()
        msg = "*Press <enter> after typing in an option\n value to refresh the Dial widget"
        tkinter.Label(self.interactframe, text=msg, justify='left').pack(anchor='w', pady=10)

    # end init

    def refresh(self):
        """Reads the inputs from the entry widgets and updates the GUI; includes alerts for errors and warnings"""
        # Parse config inputs (catch input eval errors)
        haserror = False
        for key in self.dial_config:
            input = self.entryframe.nametowidget(key).get()
            if key == 'unit':
                # Only config option that takes text
                if input == 'None':
                    self.dial_config[key] = None
                else:
                    self.dial_config[key] = input
            else:
                try:
                    self.dial_config[key] = eval(input)
                except Exception as error:
                    haserror = True
                    self.entryframe.nametowidget(key).config(bg='red')
                else:
                    self.entryframe.nametowidget(key).config(bg='white')

        # Draw new Dial (catch Dial constructor errors and warnings)
        self.dial.destroy()
        if haserror:
            size = Demonstration.DEFAULT_CONFIG['size']
            self.dial = Ctt.ErrorDisplay(self, size, error)
        else:
            with warnings.catch_warnings(record=True) as warns:
                warnings.simplefilter("always")
                try:
                    self.dial = Dial(self, **self.dial_config)
                except Exception as error:
                    haserror = True
                    size = Demonstration.DEFAULT_CONFIG['size']
                    self.dial = Ctt.ErrorDisplay(self, size, error)
                    for key in self.dial_config:
                        if any(key == word for word in str(error).split(' ')):
                            self.entryframe.nametowidget(key).config(bg='red')
                else:
                    offset = 0
                    for warn in warns:
                        warn_message = str(warn.message)
                        warn_text = 'WARNING: ' + warn_message
                        size = self.dial_config['size']
                        self.dial.create_text(size / 2, size - offset, text=warn_text, fill='gold', width=size)
                        offset += 10 * (Ctt.gettextwidth(warn_text) // size + 2)
                        for key in self.dial_config:
                            if any(key == word for word in warn_message.split(' ')):
                                self.entryframe.nametowidget(key).config(bg='gold')
        self.dial.pack(side='left', fill='y', expand=1, pady=20)
        if haserror:
            self.animate_button.config(state=tkinter.DISABLED)
        elif self.animate_button['state'] != 'normal':
            self.animate_button.config(state=tkinter.NORMAL)

    # end refresh

    def reset(self):
        """Resets back to the default configuration"""
        for key, value in Demonstration.DEFAULT_CONFIG.items():
            ent = self.entryframe.nametowidget(key)
            ent.delete(0, tkinter.END)
            ent.insert(0, str(value))
        self.refresh()


class Animation(tkinter.Toplevel):
    """Toplevel window to run animation"""

    def __init__(self, master, **config):
        tkinter.Toplevel.__init__(self, master)
        self.transient(master)
        self.title('Animation')
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.grab_set()
        x_offset = 150
        y_offset = 100
        self.geometry("+%d+%d" % (master.winfo_rootx() + x_offset, master.winfo_rooty() + y_offset))

        # Dial
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.dial = Dial(self, **config)
        self.dial.pack(pady=50)

        # Run parameters
        self.entryframe = tkinter.Frame(self)
        units = config['unit']
        if not units:
            units = 'units'
        # Run min
        name = 'run min'
        tkinter.Label(self.entryframe, text=name).grid(row=0, column=0)
        ent = tkinter.Entry(self.entryframe, name=name)
        ent.insert(0, str(config['min']))
        ent.grid(row=0, column=1)
        tkinter.Label(self.entryframe, text=units).grid(row=0, column=2)
        # Run max
        name = 'run max'
        tkinter.Label(self.entryframe, text=name).grid(row=1, column=0)
        ent = tkinter.Entry(self.entryframe, name=name)
        ent.insert(0, str(config['max']))
        ent.grid(row=1, column=1)
        tkinter.Label(self.entryframe, text=units).grid(row=1, column=2)
        # Run speed
        name = 'run speed'
        tkinter.Label(self.entryframe, text=name).grid(row=2, column=0)
        ent = tkinter.Entry(self.entryframe, name=name)
        ent.insert(0, str(1))
        ent.grid(row=2, column=1)
        tkinter.Label(self.entryframe, text=units + "/sec").grid(row=2, column=2)
        self.entryframe.pack()

        # Start/Stop button
        self.button = tkinter.Button(self, text='Start', width=10, command=self.startstop)
        self.button.pack(pady=10)

        # Quit button
        tkinter.Button(self, text='Quit', width=10, command=self.cancel).pack()

        tkinter.Label(self, text="Note: Stopping causes direction\nto reverse upon restart.").pack(pady=5)
        self.isrunning = False
        self.direction = 1
        self.focus_set()

    def start(self):
        self.isrunning = True
        self.button.config(text='Stop')
        self.animation()

    def stop(self):
        self.cancel_animation()
        self.direction *= -1
        self.isrunning = False
        self.button.config(text='Start')

    def startstop(self):
        if self.isrunning:
            self.stop()
        else:
            self.start()

    def animation(self):
        wait = 100  # ms
        has_error = False
        name = 'run max'
        try:
            run_max = float(self.entryframe.nametowidget(name).get())
            self.entryframe.nametowidget(name).config(bg='white')
        except Exception:
            has_error = True
            self.entryframe.nametowidget(name).config(bg='red')
        name = 'run min'
        try:
            run_min = float(self.entryframe.nametowidget(name).get())
            self.entryframe.nametowidget(name).config(bg='white')
        except Exception:
            has_error = True
            self.entryframe.nametowidget(name).config(bg='red')
        name = 'run speed'
        try:
            run_speed = float(self.entryframe.nametowidget(name).get())
            self.entryframe.nametowidget(name).config(bg='white')
        except Exception:
            has_error = True
            self.entryframe.nametowidget(name).config(bg='red')
        if not has_error:
            delta = self.direction * run_speed * wait / 1000.0
            value = self.dial.value + delta
            value = min(max(value, run_min), run_max)
            self.dial.set_value(value)
            self.update_idletasks()
            if value == run_max:
                self.direction = -1
                wait *= 4
            elif value == run_min:
                self.direction = 1
                wait *= 4
        self.animation_id = self.after(wait, self.animation)

    def cancel_animation(self):
        try:
            self.after_cancel(self.animation_id)
        except Exception:
            pass

    def cancel(self):
        self.cancel_animation()
        self.master.focus_set()
        self.destroy()


class Advanced(tkinter.Frame):
    """Demonstrates some of the Dial's more advanced features"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'Advanced\nDesign'

        msg = "The Dial has additional methods for configuration after construction. "
        msg += "Many of these methods capitalize on Tkinter's functionality. Objects\n"
        msg += "in the Dial widget have been provided tags to help with configuration via "
        msg += "Tkinter's methods. Below is an example of a Dial that has had\n"
        msg += "additional features configured above and beyond that of the standard Dial's appearance."
        tkinter.Label(self, text=msg, justify='left').pack(pady=50)

        self.dial = Dial(self, min=0, max=220, withdisplay=0, extent=-205)
        self.dial.pack()
        # Use Tkinter's itemconfig widget method along with Dial's built-in object tag names to change
        # the appearance of items on the Dial
        self.dial.itemconfig('face', fill='black')
        self.dial.itemconfig('scale', fill='white')  # changes the fill color on the markings except the arc
        self.dial.itemconfig('scale_arc', outline='white')  # arc needs outline color changed to take effect
        self.dial.itemconfig('needle', fill='red')
        minorticks = self.dial.find_withtag('minorscale_ticks')
        redline = minorticks[int(3.0 / 4 * len(minorticks)):]  # Add redline to 3/4 of final scale
        for minortick in redline:
            self.dial.itemconfig(minortick, fill='red', width=6)
        # Add Viewidget Digit to look better than standard Dial withdisplay functionality.
        # Note this takes some playing around with the sizes, and would take additional effort
        # to make it dynamic with Dial size.
        self.dial.digitframe = tkinter.Frame(self.dial)
        self.dial.digits = []
        size = 36
        self.dial.digits.append(Digit(self.dial.digitframe, size=size))
        self.dial.digits.append(Digit(self.dial.digitframe, size=size))
        self.dial.digits.append(Digit(self.dial.digitframe, size=size))
        for dialdigit in self.dial.digits:
            dialdigit.pack(side='left')
        self.dial.create_window(self.dial.xm + 83, self.dial.ym + 30, window=self.dial.digitframe)

        # Test/Pause button
        self.button = tkinter.Button(self, text='Test', width=10, command=self.startstop)
        self.button.pack(pady=20)
        self.isrunning = False

    def startstop(self):
        if not self.isrunning:
            self.isrunning = True
            self.button.config(text='Pause')
            if self.dial.value >= self.dial.max:
                value = self.dial.min
            else:
                value = self.dial.value + 1
            self.update_value(value)
        else:
            try:
                self.after_cancel(self.after_id)
            except Exception:
                pass
            self.isrunning = False
            self.button.config(text='Test')

    def update_value(self, value):
        self.dial.set_value(value)
        hundreds = value // 100
        if hundreds == 0:
            self.dial.digits[0].set_value(None)
        else:
            self.dial.digits[0].set_value(hundreds)
        tens = value % 100 // 10
        if tens == 0 and hundreds == 0:
            self.dial.digits[1].set_value(None)
        else:
            self.dial.digits[1].set_value(tens)
        ones = int(round(value % 10))
        self.dial.digits[2].set_value(ones)
        redzone = self.dial.min + 3.0 / 4 * (self.dial.max - self.dial.min)
        fg = self.dial.displaycolor[value < redzone]
        bg = self.dial.displaycolor[value >= redzone]
        for dialdigit in self.dial.digits:
            dialdigit.change_color(fg, bg)
        if value < self.dial.max:
            self.after_id = self.after(100, self.update_value, value + 1)
        else:
            self.startstop()


if __name__ == '__main__':
    module = 'Dial'

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
    tabframes.append(SizeCasewidthValue(TestWindow))
    tabframes.append(StartExtentMinMax(TestWindow))
    tabframes.append(ScaleUnit(TestWindow))
    tabframes.append(BoundWithdisplay(TestWindow))
    tabframes.append(Demonstration(TestWindow))
    tabframes.append(Advanced(TestWindow))

    for tabframe in tabframes:
        tabs.add(tabframe, text=tabframe.title)

    # Make Window viewable
    TestWindow.focus_set()
    TestWindow.mainloop()
