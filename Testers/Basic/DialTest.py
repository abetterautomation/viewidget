#######################################
#                                     #
# Dial Widget Tester                  #
# Written by Ryan Eggers              #
# Copyright 2017 Abetter Automation   #
#                                     #
#######################################

import tkinter
from viewidget import Dial


TestWindow = tkinter.Tk()
TestWindow.title('Dial Test')
TestWindow.geometry('550x500')
TestWindow.frame = tkinter.Frame(TestWindow, relief='ridge', borderwidth=2)
TestWindow.frame.pack(fill='both', expand=1)

# Add Dial Viewidget
TestWindow.dialframe = tkinter.Frame(TestWindow.frame)
TestWindow.dialframe.pack(expand=1, fill='x')
value = 50
TestWindow.dial = Dial(TestWindow.dialframe, unit='degF', value=value)
TestWindow.dial.pack(side=tkinter.TOP)

# Add quit button
TestWindow.quitbutton = tkinter.Button(TestWindow.frame, text='Quit', width=10, command=TestWindow.quit)
TestWindow.quitbutton.pack(side='bottom', pady=17)

# Set up an event every 150ms to increase the dial by 1 degree
for i in range(231 - value):
    TestWindow.after(150 * i, TestWindow.dial.set_value, value + i)

# Make Window viewable
TestWindow.focus_set()
TestWindow.mainloop()
