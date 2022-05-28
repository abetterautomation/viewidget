#######################################
#                                     #
# Digit Widget Tester                 #
# Written by Ryan Eggers              #
# Copyright 2017 Abetter Automation   #
#                                     #
#######################################

import tkinter
from viewidget import Digit


TestWindow = tkinter.Tk()
TestWindow.title('Digit Test')
TestWindow.geometry('325x300')
TestWindow.frame = tkinter.Frame(TestWindow, relief='ridge', borderwidth=2)
TestWindow.frame.pack(fill='both', expand=1)

# Add two Digit Viewidgets
TestWindow.digitframe = tkinter.Frame(TestWindow.frame)
TestWindow.digitframe.pack(expand=1)
TestWindow.digit1 = Digit(TestWindow.digitframe, size=100)
TestWindow.digit1.pack(side=tkinter.LEFT)
TestWindow.digit2 = Digit(TestWindow.digitframe, size=100, value='F', fg='green')
TestWindow.digit2.pack(side=tkinter.LEFT)

# Add quit button
TestWindow.quitbutton = tkinter.Button(TestWindow.frame, text='Quit', width=10, command=TestWindow.quit)
TestWindow.quitbutton.pack(side='bottom', pady=17)

# Set up an event every 1s to increase the digit1 by +1
for i in range(10):
    TestWindow.after(i * 1000, TestWindow.digit1.set_value, i)

# Make Window viewable
TestWindow.focus_set()
TestWindow.mainloop()
