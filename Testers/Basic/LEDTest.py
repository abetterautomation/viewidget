#######################################
#                                     #
# LED Widget Tester                   #
# Written by Ryan Eggers              #
# Copyright 2017 Abetter Automation   #
#                                     #
#######################################

import tkinter
from viewidget import LED


TestWindow = tkinter.Tk()
TestWindow.title('LED Test')
TestWindow.geometry('325x300')
TestWindow.frame = tkinter.Frame(TestWindow, relief='ridge', borderwidth=2)
TestWindow.frame.pack(fill='both', expand=1)

# Add LED Viewidget
TestWindow.ledframe = tkinter.Frame(TestWindow.frame)
TestWindow.ledframe.pack(expand=1, fill='x')
TestWindow.led = LED(TestWindow.ledframe, bulbcolor='green', state=LED.ON, faderate=1000)
TestWindow.led.pack(side=tkinter.TOP)

# Add quit button
TestWindow.quitbutton = tkinter.Button(TestWindow.frame, text='Quit', width=10, command=TestWindow.quit)
TestWindow.quitbutton.pack(side='bottom', pady=17)

# Add state button to allow user to turn on or off
TestWindow.statebutton = tkinter.Button(TestWindow.frame, text='state', width=10, command=TestWindow.led.change_state)
TestWindow.statebutton.pack(side='bottom', pady=17)

# Make Window viewable
TestWindow.focus_set()
TestWindow.mainloop()
