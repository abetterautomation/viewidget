############################################
#                                          #
# LED Widget Functionality Tester          #
# Written by Ryan Eggers                   #
# Copyright 2017 Abetter Automation        #
#                                          #
############################################

import warnings
import random
import tkinter
from tkinter import ttk

from viewidget import LED

import CommonTestTools as Ctt


class Introduction(tkinter.Frame):
    """Provides an introduction from LED's docstring"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'Introduction\n'
        innerframe = tkinter.Frame(self)
        widget = LED(innerframe, diodecolor='#ffcc00', state=LED.ON)
        widget.pack(side='right')
        docframe = tkinter.Frame(innerframe)
        name = Ctt.getwidgetname(widget, True)
        doc = Ctt.getdoc(widget)
        tkinter.Label(docframe, text=name, font=('Helvetica', 16, 'bold')).pack(side='top', pady=2)
        tkinter.Label(docframe, text=doc, justify='left').pack(side='bottom')
        docframe.pack(side='left')
        innerframe.pack(side='left', fill='x', expand=1, padx=50)


class Construction(tkinter.Frame):
    """Provides information on LED's __init__ function"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'Construction\n'
        innerframe = tkinter.Frame(self)
        widget = LED(innerframe, size=125, bulbcolor='green', state=LED.ON)
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


class SizeCasewidth(tkinter.Frame):
    """Demonstrates LED configuration functionality: size and casewidth"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'size and\ncasewidth'

        widget1 = LED()  # Default: size=100, casewidth=10
        widget2 = LED(size=150, casewidth=10)
        widget3 = LED(size=100, casewidth=5)
        widget4 = LED(size=50, casewidth=5)

        block1 = Ctt.WidgetData(widget1, size=100, casewidth=10)
        block2 = Ctt.WidgetData(widget2, size=150, casewidth=10)
        block3 = Ctt.WidgetData(widget3, size=100, casewidth=5)
        block4 = Ctt.WidgetData(widget4, size=50, casewidth=5)
        Ctt.WidgetBlock(self, block1, block2, block3, block4).pack(fill='both', expand=1)


class StateColor(tkinter.Frame):
    """Demonstrates LED configuration functionality: state, diodecolor, and bulbcolor"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'state, diodecolor\nand bulbcolor'

        widget1 = LED()  # Default: state=False, diodecolor='white', bulbcolor='white'
        widget2 = LED(state=True)
        widget3 = LED(diodecolor='cyan')
        widget4 = LED(state=True, diodecolor='cyan')
        widget5 = LED(bulbcolor='cyan')
        widget6 = LED(state=True, bulbcolor='cyan')
        widget7 = LED(diodecolor='yellow', bulbcolor='cyan')
        widget8 = LED(state=True, diodecolor='yellow', bulbcolor='cyan')

        block1 = Ctt.WidgetData(widget1, state=False, diodecolor='white', bulbcolor='white')
        block2 = Ctt.WidgetData(widget2, state=True, diodecolor='white', bulbcolor='white')
        block3 = Ctt.WidgetData(widget3, state=False, diodecolor='cyan', bulbcolor='white')
        block4 = Ctt.WidgetData(widget4, state=True, diodecolor='cyan', bulbcolor='white')
        block5 = Ctt.WidgetData(widget5, state=False, diodecolor='white', bulbcolor='cyan')
        block6 = Ctt.WidgetData(widget6, state=True, diodecolor='white', bulbcolor='cyan')
        block7 = Ctt.WidgetData(widget7, state=False, diodecolor='yellow', bulbcolor='cyan')
        block8 = Ctt.WidgetData(widget8, state=True, diodecolor='yellow', bulbcolor='cyan')
        Ctt.WidgetBlock(self, block1, block2, block3, block4, block5, block6, block7, block8).pack(fill='both',
                                                                                                   expand=1)


class Reflectstyle(tkinter.Frame):
    """Demonstrates LED configuration functionality: reflectstyle (steadystate)"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'reflectstyle\n(steadystate)'

        widget1 = LED(diodecolor='blue')  # Default: reflectstyle=0b111
        widget2 = LED(diodecolor='blue', state=True)
        widget3 = LED(bulbcolor='blue')
        widget4 = LED(bulbcolor='blue', state=True)
        widget5 = LED(bulbcolor='blue', reflectstyle=1)
        widget6 = LED(bulbcolor='blue', reflectstyle=1, state=True)
        widget7 = LED(bulbcolor='#0000ff', reflectstyle=0)
        widget8 = LED(bulbcolor='#0000FF', reflectstyle=0, state=True)

        block1 = Ctt.WidgetData(widget1, state=False, diodecolor='blue', bulbcolor='white', reflectstyle=bin(7))
        block2 = Ctt.WidgetData(widget2, state=True, diodecolor='blue', bulbcolor='white', reflectstyle=bin(7))
        block3 = Ctt.WidgetData(widget3, state=False, diodecolor='white', bulbcolor='blue', reflectstyle=bin(7))
        block4 = Ctt.WidgetData(widget4, state=True, diodecolor='white', bulbcolor='blue', reflectstyle=bin(7))
        block5 = Ctt.WidgetData(widget5, state=False, diodecolor='white', bulbcolor='blue', reflectstyle=bin(1))
        block6 = Ctt.WidgetData(widget6, state=True, diodecolor='white', bulbcolor='blue', reflectstyle=bin(1))
        block7 = Ctt.WidgetData(widget7, state=False, diodecolor='#ffffff', bulbcolor='#0000ff', reflectstyle=bin(0))
        block8 = Ctt.WidgetData(widget8, state=True, diodecolor='#FFFFFF', bulbcolor='#0000FF', reflectstyle=bin(0))
        Ctt.WidgetBlock(self, block1, block2, block3, block4, block5, block6, block7, block8).pack(fill='both',
                                                                                                   expand=1)


class ReflectFadeBlink(tkinter.Frame):
    """Demonstrates LED configuration functionality: reflectstyle (transient), faderate, blinkrate"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'reflectstyle (transient),\nfaderate and blinkrate'

        widget1 = LED(diodecolor='red', state=True)  # Default: reflectstyle=0b111, faderate=0, blinkrate=0
        widget2 = LED(diodecolor='red', state=True, blinkrate=1000)
        widget3 = LED(bulbcolor='red', state=True, blinkrate=2000)
        widget4 = LED(bulbcolor='red', state=True, blinkrate=2000, faderate=1000)
        widget5 = LED(bulbcolor='red', state=True, blinkrate=3500, faderate=3000)
        widget6 = LED(bulbcolor='red', state=True, blinkrate=3500, faderate=3000, reflectstyle=3)
        widget7 = LED(bulbcolor='#ff0000', state=True, blinkrate=3500, faderate=3000, reflectstyle=1)
        widget8 = LED(bulbcolor='#FF0000', state=True, blinkrate=3500, faderate=3000, reflectstyle=0)

        block1 = Ctt.WidgetData(widget1, diodecolor='red', bulbcolor='white', reflectstyle=bin(7), faderate=0,
                                blinkrate=0)
        block2 = Ctt.WidgetData(widget2, diodecolor='red', bulbcolor='white', reflectstyle=bin(7), faderate=0,
                                blinkrate=1000)
        block3 = Ctt.WidgetData(widget3, diodecolor='white', bulbcolor='red', reflectstyle=bin(7), faderate=0,
                                blinkrate=2000)
        block4 = Ctt.WidgetData(widget4, diodecolor='white', bulbcolor='red', reflectstyle=bin(7), faderate=1000,
                                blinkrate=2000)
        block5 = Ctt.WidgetData(widget5, diodecolor='white', bulbcolor='red', reflectstyle=bin(7), faderate=3000,
                                blinkrate=3500)
        block6 = Ctt.WidgetData(widget6, diodecolor='white', bulbcolor='red', reflectstyle=bin(3), faderate=3000,
                                blinkrate=3500)
        block7 = Ctt.WidgetData(widget7, diodecolor='#ffffff', bulbcolor='#ff0000', reflectstyle=bin(1), faderate=3000,
                                blinkrate=3500)
        block8 = Ctt.WidgetData(widget8, diodecolor='#FFFFFF', bulbcolor='#FF0000', reflectstyle=bin(0), faderate=3000,
                                blinkrate=3500)
        Ctt.WidgetBlock(self, block1, block2, block3, block4, block5, block6, block7, block8).pack(fill='both',
                                                                                                   expand=1)


class Brightness(tkinter.Frame):
    """Demonstrates LED's set_brightness functionality"""

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'Setting\nbrightness'

        self.led = LED(self, bulbcolor='#0F0', state=LED.ON)
        self.led.pack(side='left', padx=50)

        self.slide = tkinter.Scale(self, label='brightness', takefocus=False,
                                   command=self.update_brightness)  # , relief='groove', borderwidth=2)
        self.slide.config(from_=100, to=0)  # Reverse slider so 0 is on the bottom
        self.slide.set(100)
        self.slide.pack(side='left', ipadx=10, ipady=20)

    def update_brightness(self, value):
        self.led.set_brightness(float(value) / 100)


class Demonstration(tkinter.Frame):
    """Allows the user to try out the LED's features interactively"""

    DEFAULT_CONFIG = dict(size=100,
                          casewidth=10,
                          diodecolor='white',
                          bulbcolor='white',
                          reflectstyle=0b111, )

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'Interactive\nDemonstration'

        # LEDs frame for both off and on demonstrators
        self.leds_frame = tkinter.Frame(self)
        self.leds_frame.pack(side='left', fill='y', expand=1, pady=20)
        self.ledoff = tkinter.LabelFrame(self.leds_frame, text="OFF", labelanchor='n', relief='flat')
        self.ledoff.pack(fill='y', expand=1)
        self.ledon = tkinter.LabelFrame(self.leds_frame, text="ON", labelanchor='n', relief='flat')
        self.ledon.pack(fill='y', expand=1)

        self.leds_config = Demonstration.DEFAULT_CONFIG.copy()
        self.led1 = LED(self.ledoff, **self.leds_config)
        self.led1.pack(fill='y', expand=1)
        self.led2 = LED(self.ledon, **self.leds_config)
        self.led2.turnon()
        self.led2.pack(fill='y', expand=1, anchor='n')

        # Interact subframe
        self.interactframe = tkinter.Frame(self)
        self.interactframe.pack(side='right', fill='y', expand=1, pady=10)
        tkinter.Label(self.interactframe, text="Please enter LED options...*").pack(anchor='w', pady=5)
        # Entry frame contains config variable keys as labels and corresponding entry widgets with values of each key
        self.entryframe = tkinter.Frame(self.interactframe)
        row = 0
        for key, value in self.leds_config.items():
            tkinter.Label(self.entryframe, text=key).grid(row=row, column=0)
            ent = tkinter.Entry(self.entryframe, name=key)
            if key == 'reflectstyle':
                ent.insert(0, bin(value))
            else:
                ent.insert(0, str(value))
            ent.bind('<Return>', lambda e: self.refresh())
            ent.grid(row=row, column=1)
            row += 1
        self.entryframe.pack()
        # Reset and animate buttons
        self.animate_button = tkinter.Button(self.interactframe, text='Animate', width=10,
                                             command=lambda: Animation(self, **self.leds_config))
        self.animate_button.pack(pady=10)
        tkinter.Button(self.interactframe, text='Reset', width=10, command=self.reset).pack()
        msg = "*Press <enter> after typing in an option\n value to refresh the LED widget"
        tkinter.Label(self.interactframe, text=msg, justify='left').pack(anchor='w', pady=10)

    # end init

    def refresh(self):
        """Reads the inputs from the entry widgets and updates the GUI; includes alerts for errors and warnings"""
        # Parse config inputs (catch input eval errors)
        haserror = False
        for key in self.leds_config:
            input = self.entryframe.nametowidget(key).get()
            if key == 'diodecolor' or key == 'bulbcolor':
                # Config options that takes text: colors - convert to RGB first
                try:
                    self.leds_config[key] = "#%04x%04x%04x" % self.winfo_rgb(input)
                except Exception as error:
                    haserror = True
                    self.entryframe.nametowidget(key).config(bg='red')
                else:
                    self.entryframe.nametowidget(key).config(bg='white')
            else:
                try:
                    self.leds_config[key] = eval(input)
                except Exception as error:
                    haserror = True
                    self.entryframe.nametowidget(key).config(bg='red')
                else:
                    self.entryframe.nametowidget(key).config(bg='white')

        # Draw new LED (catch LED constructor errors and warnings)
        self.ledoff.destroy()
        self.ledon.destroy()
        if haserror:
            size = Demonstration.DEFAULT_CONFIG['size'] * 2
            self.ledoff = Ctt.ErrorDisplay(self.leds_frame, size, error)
            self.ledon = tkinter.Frame(self.leds_frame)
        else:
            with warnings.catch_warnings(record=True) as warns:
                warnings.simplefilter("always")
                try:
                    self.ledoff = tkinter.LabelFrame(self.leds_frame, text="OFF", labelanchor='n', relief='flat')
                    self.ledon = tkinter.LabelFrame(self.leds_frame, text="ON", labelanchor='n', relief='flat')
                    self.led1 = LED(self.ledoff, **self.leds_config)
                    self.led1.pack(fill='y', expand=1)
                    self.led2 = LED(self.ledon, **self.leds_config)
                    self.led2.turnon()
                    self.led2.pack(fill='y', expand=1, anchor='n')
                except Exception as error:
                    haserror = True
                    size = Demonstration.DEFAULT_CONFIG['size'] * 2
                    self.ledoff = Ctt.ErrorDisplay(self.leds_frame, size, error)
                    self.ledon = tkinter.Frame(self.leds_frame)
                    for key in self.leds_config:
                        if any(key == word for word in str(error).split(' ')):
                            self.entryframe.nametowidget(key).config(bg='red')
                else:
                    offset = 0
                    warn_messages = {str(warn.message) for warn in warns}
                    for warn_message in warn_messages:
                        warn_text = 'WARNING: ' + warn_message
                        size = self.leds_config['size']
                        self.led1.create_text(size / 2, size - offset, text=warn_text, fill='gold', width=size)
                        offset += 10 * (Ctt.gettextwidth(warn_text) // size + 2)
                        for key in self.leds_config:
                            if any(key == word for word in warn_message.split(' ')):
                                self.entryframe.nametowidget(key).config(bg='gold')
        self.ledoff.pack(fill='y', expand=1)
        self.ledon.pack(fill='y', expand=1)
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
            if key == 'reflectstyle':
                ent.insert(0, bin(value))
            else:
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
        y_offset = 50
        self.geometry("+%d+%d" % (master.winfo_rootx() + x_offset, master.winfo_rooty() + y_offset))

        # LED
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.led = LED(self, **config)
        self.led.pack(pady=30)

        # Additional LED Parameters for Animation
        self.entryframe = tkinter.Frame(self)
        self.entryframe.pack()
        # faderate
        name = 'faderate'
        tkinter.Label(self.entryframe, text=name).grid(row=0, column=0)
        ent = tkinter.Entry(self.entryframe, name=name, width=10)
        ent.insert(0, str(self.led.faderate))
        ent.bind('<Return>', lambda e: self.set_rates())
        ent.grid(row=0, column=1)
        # blinkrate
        name = 'blinkrate'
        tkinter.Label(self.entryframe, text=name).grid(row=1, column=0)
        ent = tkinter.Entry(self.entryframe, name=name, width=10)
        ent.insert(0, str(self.led.blinkrate))
        ent.bind('<Return>', lambda e: self.set_rates())
        ent.grid(row=1, column=1)

        # On button
        button = tkinter.Button(self, text='On', width=10, command=self.turnon)
        button.pack(pady=5)

        # Off button
        button = tkinter.Button(self, text='Off', width=10, command=self.turnoff)
        button.pack(pady=5)

        # Quit button
        self.button = tkinter.Button(self, text='Quit', width=10, command=self.cancel)
        self.button.pack(pady=10)

        msg = "Rates are set when buttons are pressed,\nor type a rate and press <enter> to\nset while running."
        tkinter.Label(self, text=msg).pack(pady=5)

        self.focus_set()

    def turnon(self):
        self.set_rates()
        self.led.turnon()

    def turnoff(self):
        self.set_rates()
        self.led.turnoff()

    def set_blinkrate(self):
        haserror = self.set_rate('blinkrate', self.led.set_blinkrate)
        if haserror:
            pass

    def set_faderate(self):
        haserror = self.set_rate('faderate', self.led.set_faderate)
        if haserror:
            pass

    def set_rate(self, key, ratefunc):
        haserror = False
        # check for input errors
        try:
            input = eval(self.entryframe.nametowidget(key).get())
        except Exception as error:
            haserror = True
            self.entryframe.nametowidget(key).config(bg='red')
        else:
            self.entryframe.nametowidget(key).config(bg='white')
        # check for set rate errors, else set rate
        if not haserror:
            try:
                ratefunc(input)
            except Exception as error:
                haserror = True
                self.entryframe.nametowidget(key).config(bg='red')
            else:
                self.entryframe.nametowidget(key).config(bg='white')
        return haserror

    def set_rates(self):
        self.set_blinkrate()
        self.set_faderate()

    def cancel(self):
        self.master.focus_set()
        self.destroy()


class Advanced(tkinter.Frame):
    """Demonstrates more advanced usage of the LED"""

    COLORS = ['green', 'orange', 'blue']
    ROWS = 12
    COLUMNS = 30

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.title = 'Advanced\nDesign'

        topframe = tkinter.Frame(self)
        topframe.pack(pady=50, side='top')
        # first blinking LED
        color = self.COLORS[0]
        led = LED(topframe, size=56, casewidth=5, state=LED.ON, diodecolor=color, reflectstyle=5)
        led.set_faderate(2000)
        led.diodecolor = color
        led.grid(row=0, column=0)
        self.update_LED(led)
        # message
        msg = "The LED can be utilized in various ways and designs.\n"
        msg += "An example of LEDs used as an equalizer display is shown below."
        tkinter.Label(topframe, text=msg, justify='left').grid(row=0, column=1)
        # second blinking LED
        color = self.COLORS[1]
        led = LED(topframe, size=56, casewidth=5, state=LED.ON, diodecolor=color, reflectstyle=5)
        led.set_faderate(2000)
        led.diodecolor = color
        led.grid(row=0, column=2)
        self.after(500, self.update_LED, led)

        # Array of LEDs
        self.LEDs = []
        LEDframe = tkinter.Frame(self)
        LEDframe.pack(padx=10, pady=10)
        for i in range(self.COLUMNS):
            LEDs = []
            for j in range(self.ROWS):
                if j < 2:
                    diodecolor = 'red'
                elif j < 4:
                    diodecolor = 'yellow'
                else:
                    diodecolor = 'green'
                led = LED(LEDframe, size=20, casewidth=0, reflectstyle=0, diodecolor=diodecolor)
                led.grid(row=j, column=i)
                LEDs.append(led)
            self.LEDs.append(LEDs)
        self.init_array()

    def update_LED(self, led):
        if not led.state:
            i = self.COLORS.index(led.diodecolor) + 1
            if i < len(self.COLORS):
                color = self.COLORS[i]
            else:
                color = self.COLORS[0]
            led.change_color(color)
            led.diodecolor = color
        led.change_state()
        self.after(1000, self.update_LED, led)

    def init_array(self):
        self.LEDoutput = [random.randint(0, self.ROWS - 1)]
        for i in range(1, self.COLUMNS):
            next_output = self.next_output(self.LEDoutput[-1])
            self.LEDoutput.append(next_output)
        self.update_array()

    def update_array(self):
        for i in range(self.COLUMNS):
            column_output = self.LEDoutput[i]
            for j in range(self.ROWS):
                self.LEDs[i][j].turn(column_output >= self.ROWS - j)
        self.after(500, self.update_output)

    def update_output(self):
        for i in range(self.COLUMNS):
            self.LEDoutput[i] = self.next_output(self.LEDoutput[i])
        self.update_array()

    def next_output(self, seed):
        goodval = False
        while not goodval:
            next_output = seed + random.randint(-2, 2)
            if 0 <= next_output <= self.ROWS:
                goodval = True
        return next_output


if __name__ == '__main__':
    module = 'LED'

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
    tabframes.append(SizeCasewidth(TestWindow))
    tabframes.append(StateColor(TestWindow))
    tabframes.append(Reflectstyle(TestWindow))
    tabframes.append(ReflectFadeBlink(TestWindow))
    tabframes.append(Brightness(TestWindow))
    tabframes.append(Demonstration(TestWindow))
    tabframes.append(Advanced(TestWindow))

    for tabframe in tabframes:
        tabs.add(tabframe, text=tabframe.title)

    # Make Window viewable
    TestWindow.focus_set()
    TestWindow.mainloop()
