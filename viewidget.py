###########################################################################
#                                                                         #
# viewidget.py                                                            #
# Version 1.0                                                             #
# Written by Ryan Eggers (ryan.eggers@abetterautomation.com)              #
# Copyright 2017 Abetter Automation Technologies Company                  #
#                                                                         #
# This program is free software: you can redistribute it and/or modify    #
# it under the terms of the GNU General Public License as published by    #
# the Free Software Foundation, either version 3 of the License, or       #
# (at your option) any later version.                                     #
#                                                                         #
# This program is distributed in the hope that it will be useful,         #
# but WITHOUT ANY WARRANTY; without even the implied warranty of          #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
# GNU General Public License for more details.                            #
#                                                                         #
# You should have received a copy of the GNU General Public License       #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.   #
#                                                                         #
###########################################################################

"""
GUI widgets for items typically seen in scientific & industrial interfaces.

Based on Tkinter and designed for automation software, the widgets in this
module have been implemented in such a way to be versatile in their
appearance and functionality, thereby providing potential for use in a
wide variety of visual software applications.

Viewidgets extend Tkinter's Canvas. The following widgets are included:
    - Dial: Designed after a temperature dial, this widget can represent
        any type dial with a similar appearance.
    - LED: Represents an indicator light, complete with blink and fade
        effects.
    - Digit: Single character of a classic segment display, such as
        the numbers on a digital clock.

Non-widget support objects:
    - ViewidgetError: Extended from built-in Exception; thrown when
        a user action is egregious enough to halt the program.
    - ViewidgetWarning: Extended from built-in UserWarning; used when
        there should be some non-fatal alert to the user.

Support methods in this module:
    - mean(iterable): Math function to calculate the average from an
        iterable set of values. Returns float.

"""


import warnings
import math
import tkinter
import tkinter.font
from time import time
from collections import deque
from colorsys import rgb_to_hls, hls_to_rgb
from cmath import exp as cexp


# FUNCTIONS
# ------------
def mean(iterable):
    """Returns the average of the values in the iterable."""
    return math.fsum(iterable) / max(len(iterable), 1)


# CLASSES
# ------------
class ViewidgetError(Exception):
    """Exception class for viewidget errors."""
    pass


class ViewidgetWarning(UserWarning):
    """Warning class for viewidget alerts."""
    pass


##################
# Dial Viewidget #
##################
class Dial(tkinter.Canvas):
    """
    Tkinter-based dial widget.

    The Viewidget Dial was originally designed after a bi-metal thermometer;
    however, its appearance is flexible enough to represent many other
    types of dials, for instance a pressure gauge or speedometer.

    Major appearance options are defined during construction, although like
    any Tkinter object its appearance can be modified at any time. In
    addition, the majority of Dial Canvas items have been provided tags
    to facilitate with modification beyond its standard appearance.

    Besides the methods inherited from its superclass Tkinter.Canvas,
    the Viewidget Dial contains one fundamental method:
        - set_value(value): Points needle to the value given.

    """

    # Class Attributes
    # ------------------
    DEGREE = u'\u00B0'  # Degree sign

    # Class Methods
    # ------------------
    def __init__(self, master=None, **kwargs):
        """
        Dial constructor arguments:
        - master: Parent object.
        - kwargs: Dial constructor accepts the following keyword arguments...
            - size: Size of Dial; >0, default 300.
            - casewidth: Width of the Dial case border; >=0, default 15.
            - start: Angle Dial begins in degrees; (-360,360), default 225.
            - extent: Angle Dial extends in degrees; [-360,360], default -270.
            - min: Value Dial begins; (-inf,inf), default 60.
            - max: Value Dial ends; (-inf,inf), default 220.
            - majorscale: Delta between numbered long ticks; >0, default 20.
            - semimajorscale: Delta between non-numbered long ticks, must be
                factor of majorscale, set to 0 to disable; >=0, default 10.
            - minorscale: Delta between non-numbered short ticks, set to 0 to
                disable; >=0, default 2.
            - unit: Dial text to specify units; string, default None.
            - bound: Adds hard stops at Dial min/max; boolean, default True.
            - withdisplay: Flag to add readout display; boolean, default True.
            - value: Initial value of Dial; (-inf,inf), default min.

        Example:
            Dial(size=275, casewidth=10, min=0, max=100, value=14.7, unit='psi')

        """

        self.value = None  # Dial value
        self.bound = True  # Flag whether dial is prohibited from moving past boundaries
        self.display = None  # Dial readout display canvas object (only gets initialized if withdisplay is enabled)
        self.displaycolor = ['black',
                             'red']  # List of readout display colors (if withdisplay is enabled) [<normal>, <alert>]
        self.displayroundto = 1  # Number to round past the decimal on the readout display (if withdisplay is enabled)

        size = 300  # Size of dial
        casewidth = 15  # Size of dial case border
        self.start = 225  # Angle of starting point (from positive x-axis in degrees)
        extent = -270  # Angle to extend arc from starting point (extends from self.start counter-clockwise in degrees)
        self.min = 60  # Minimum scale value
        self.max = 220  # Maximum scale value
        majorscale = 20  # Step size of major counts on scale (long ticks, with number); Must be greater than zero
        semimajorscale = 10  # Step size semimajor counts (long ticks, no number); Must be factor of majorscale or zero
        minorscale = 2  # Step size of minor counts on scale (short ticks, no number); Set to zero to disable
        unit = None  # Unit value to show on dial (e.g. degC, psi, rpm, etc...)
        initvalue = None  # Initial value of dial; Defaults to self.min if no value is specified during initialization
        bound = None  # User set bound flag; Defaults to self.bound if not set; Note bound is turned off if extent >360
        withdisplay = True  # Flag to turn on dial readout display

        # Parse keyword arguments
        # -----------------------
        for key, value in kwargs.items():
            if key == 'size':
                if value > 0:
                    size = value
                else:
                    raise ViewidgetError('Dial size must be greater than zero')
            elif key == 'casewidth':
                if value >= 0:
                    casewidth = value
                else:
                    raise ViewidgetError('Dial casewidth must be greater than or equal to zero')
            elif key == 'start':
                if abs(value) < 360:
                    self.start = value
                else:
                    raise ViewidgetError('Dial start angle must be smaller than +/-360 degrees')
            elif key == 'extent':
                if abs(value) <= 360:
                    extent = value
                    if abs(value) == 360:
                        self.bound = False
                else:
                    raise ViewidgetError('Dial extent angle must be smaller than or equal to +/-360 degrees')
            elif key == 'min':
                self.min = value
            elif key == 'max':
                self.max = value
            elif key == 'majorscale':
                if value > 0:
                    majorscale = value
                else:
                    raise ViewidgetError('Dial majorscale must be greater than zero')
            elif key == 'semimajorscale':
                if value >= 0:
                    semimajorscale = value
                else:
                    raise ViewidgetError('Dial semimajorscale must be greater than or equal to zero')
            elif key == 'minorscale':
                if value >= 0:
                    minorscale = value
                else:
                    raise ViewidgetError('Dial minorscale must be greater than or equal to zero')
            elif key == 'unit':
                if type(value) == str:
                    unit = value.replace('deg', Dial.DEGREE)
                else:
                    unit = value
            elif key == 'value':
                initvalue = value
            elif key == 'bound':
                bound = bool(value)
            elif key == 'withdisplay':
                withdisplay = bool(value)
            else:
                raise ViewidgetError('Dial init keyword "%s" unknown' % key)

        # Set initial values and check for user input errors
        # --------------------------------------------------
        self.end = self.start + extent

        if bound is not None:
            self.bound = bound

        if self.min == self.max:
            raise ViewidgetError('Dial min cannot be equal to the max')
        elif self.min > self.max:
            warnings.warn('Dial min is greater than the max', ViewidgetWarning)
            count_direction = -1
        else:
            count_direction = 1

        if semimajorscale:
            if semimajorscale >= majorscale:
                warnings.warn('Dial semimajorscale greater than or equal to majorscale', ViewidgetWarning)
                semimajorscale = 0
            elif majorscale % semimajorscale:
                warnings.warn('Dial semimajorscale must be a factor of the majorscale', ViewidgetWarning)
                # semimajorscale = majorscale / int(majorscale / semimajorscale)
                semimajorscale = 0

        try:
            if size / casewidth < 10:
                warnings.warn('Dial casewidth must be less than or equal to 1/10 the size', ViewidgetWarning)
                casewidth = size / 10
        except ZeroDivisionError:
            pass

        # Call Canvas Constructor
        # -----------------------
        shadow3D = math.floor(math.log(2 * size, 10))
        light3D = math.ceil(shadow3D / 2)
        length = size + casewidth + shadow3D
        tkinter.Canvas.__init__(self, master, width=length, height=length, borderwidth=0, highlightthickness=0)

        # Draw Dial body
        # --------------
        self.create_oval(casewidth, casewidth - light3D, size, size - light3D, width=casewidth, fill='white',
                         outline='white')
        self.create_oval(casewidth, casewidth + shadow3D, size, size + shadow3D, width=casewidth, fill='gray5',
                         outline='gray5')
        # Dial face
        self.create_oval(casewidth, casewidth, size, size, width=casewidth, fill='white', outline='gray60', tags='face')
        self.xm = self.ym = (size + casewidth) / 2  # Coordinate reference to center of dial
        dialrad = (size - casewidth) / 2  # Radius of dial

        # Dial scale markings
        # -------------------
        absdiff = abs(self.max - self.min)
        arcoffset = dialrad / 3

        # minor scale ticks
        if minorscale != 0:
            tags = ('minorscale', 'minorscale_ticks', 'scale_ticks', 'scale')
            numoflines = int(absdiff / minorscale) + 1
            angles = (self.start + n * extent * minorscale / absdiff for n in range(numoflines))
            for angle in angles:
                x1 = self.xm + (dialrad - arcoffset) * math.cos(math.radians(angle))
                y1 = self.ym - (dialrad - arcoffset) * math.sin(math.radians(angle))
                x2 = x1 + arcoffset / 5 * math.cos(math.radians(angle))
                y2 = y1 - arcoffset / 5 * math.sin(math.radians(angle))
                self.create_line(x1, y1, x2, y2, tags=tags)

        # semimajor scale ticks
        if semimajorscale != 0:
            tags = ('minorscale', 'semimajorscale_ticks', 'scale_ticks', 'scale')
            numoflines = int(absdiff / semimajorscale) + 1
            angles = (self.start + n * extent * semimajorscale / absdiff for n in range(numoflines))
            for angle in angles:
                x1 = self.xm + (dialrad - arcoffset) * math.cos(math.radians(angle))
                y1 = self.ym - (dialrad - arcoffset) * math.sin(math.radians(angle))
                x2 = x1 + arcoffset / 3 * math.cos(math.radians(angle))
                y2 = y1 - arcoffset / 3 * math.sin(math.radians(angle))
                self.create_line(x1, y1, x2, y2, tags=tags)

        # major scale ticks and numbering
        tags = ('majorscale', 'majorscale_ticks', 'scale_ticks', 'scale')
        numoflines = int(absdiff / majorscale) + int(abs(extent) != 360)
        angles = (self.start + n * extent * majorscale / absdiff for n in range(numoflines))
        textvals = (self.min + n * majorscale * count_direction for n in range(numoflines))
        textpos = arcoffset / 2.5
        texttags = ('majorscale', 'scale_text', 'scale')
        self.scalefont = tkinter.font.Font(size=int(arcoffset / 5), weight='bold')
        for angle, textval in zip(angles, textvals):
            x1 = self.xm + (dialrad - arcoffset) * math.cos(math.radians(angle))
            y1 = self.ym - (dialrad - arcoffset) * math.sin(math.radians(angle))
            x2 = x1 + arcoffset / 3 * math.cos(math.radians(angle))
            y2 = y1 - arcoffset / 3 * math.sin(math.radians(angle))
            self.create_line(x1, y1, x2, y2, width=3, tags=tags)
            x1 = self.xm + (dialrad - textpos) * math.cos(math.radians(angle))
            y1 = self.ym - (dialrad - textpos) * math.sin(math.radians(angle))
            self.create_text(x1, y1, text=textval, font=self.scalefont, tags=texttags)

        # scale arc
        tags = ('majorscale', 'scale_arc', 'scale')
        x1 = y1 = arcoffset + casewidth
        x2 = y2 = size - arcoffset
        if abs(extent) != 360:
            self.create_arc(x1, y1, x2, y2, start=self.start, extent=extent, width=2, style='arc', tags=tags)
        else:
            self.create_oval(x1, y1, x2, y2, width=2, tags=tags)

        # Add unit markings and readout display (if withdisplay is enabled)
        # -----------------------------------------------------------------
        x1 = self.xm
        y1 = self.ym + arcoffset * 4 / 3
        self.displayfont = tkinter.font.Font(size=int(arcoffset / 3), weight='bold')
        if withdisplay:
            self.display = self.create_text(x1, y1, font=self.displayfont, tags=('readout', 'display'))
            x1 = self.xm + max(self.displayfont.measure(self.min), self.displayfont.measure(self.max)) + 2
        # unit display
        self.create_text(x1, y1, text=unit, font=self.displayfont, tags=('unit', 'display'))

        # Draw Dial needle and pin
        # ------------------------
        pinrad = size / 25  # radius of the pin
        # needle starts by pointing in the pos x-axis direction (0 degrees)
        xy1 = (self.xm + 2.5 * arcoffset, self.ym)
        xy2 = (self.xm - arcoffset, self.ym + 0.75 * pinrad)
        xy3 = (self.xm - arcoffset, self.ym - 0.75 * pinrad)
        self.needlecoords = [xy1, xy2, xy3]
        self.needle = self.create_polygon(self.needlecoords, tags='needle')
        self.create_oval(self.xm - pinrad, self.ym - pinrad - light3D, self.xm + pinrad, self.ym + pinrad - light3D,
                         fill='gray95', outline='gray95')
        self.create_oval(self.xm - pinrad, self.ym - pinrad + shadow3D, self.xm + pinrad, self.ym + pinrad + shadow3D,
                         fill='gray5', outline='gray5')
        # Dial pin
        self.create_oval(self.xm - pinrad, self.ym - pinrad, self.xm + pinrad, self.ym + pinrad, fill='gray70',
                         outline='#DDDDDD', tags='pin')

        self.set_value(initvalue)

    # End Dial.__init__

    def set_value(self, value):
        """Set Dial needle to point at the given value."""

        if value is None:
            value = self.min
        # only perform an update if the value has changed
        # -----------------------------------------------
        if self.value != value:
            self.value = value
            angle = (value - self.min) * (self.end - self.start) / (self.max - self.min) + self.start

            # if dial is bound, check if value is out of bounds
            # -------------------------------------------------
            self.outofbounds = False
            if self.bound:
                if self.min < self.max:  # scale is increasing (1,2,3,...)
                    if value < self.min:
                        angle = self.start
                        self.outofbounds = True
                    elif value > self.max:
                        angle = self.end
                        self.outofbounds = True
                else:  # scale is decreasing (3,2,1,...)
                    if value > self.min:
                        angle = self.start
                        self.outofbounds = True
                    elif value < self.max:
                        angle = self.end
                        self.outofbounds = True

            # rotate needle (via complex numbers)
            # for more info on algorithm see:
            # http://www.effbot.org/zone/tkinter-complex-canvas.htm
            # -----------------------------------------------------
            newxy = []
            offset = complex(self.xm, self.ym)
            for x, y in self.needlecoords:
                v = cexp(math.radians(-angle) * 1j) * (complex(x, y) - offset) + offset
                newxy.append(v.real)
                newxy.append(v.imag)
            self.coords(self.needle, *newxy)

            # update the readout display (if enabled)
            # ---------------------------------------
            if self.display:
                if self.displayroundto > 0:
                    displayvalue = round(value, self.displayroundto)
                else:
                    displayvalue = int(round(value))
                displaycolor = self.displaycolor[self.outofbounds]
                self.itemconfig(self.display, text=displayvalue, fill=displaycolor)

    # End Dial.set_value

# End Dial class


#################
# LED Viewidget #
#################
class LED(tkinter.Canvas):
    """
    Tkinter-based LED widget.

    Light-emitting diodes (LEDs) are used for a multitude of purposes and
    have become the de-facto discrete indicator in electronics. While it
    is relatively easy to implement a basic LED in Tkinter (a circle that
    changes from dark to light is all it really takes), the Viewidget LED
    has several features included in its design to provide a more real-
    world look and feel.

    The Viewidget LED can be turned on or off, blink, fade, and/or change
    color. It contains a number of operational methods:
        - turn(state): Turns LED on or off; or use these shortcuts:
            - turnon(): Turns LED on.
            - turnoff(): Turns LED off.
        - change_color(diode, bulb): Changes color of the diode and/or bulb.
        - set_brightness(level): Dims LED from 0% to 100%.
        - set_blinkrate(rate): Sets LED to blink at the rate given (in ms).
        - set_faderate(rate): Sets LED to fade at the rate given (in ms).
        And more...

    """

    # Class Attributes
    # ------------------
    ON = 1
    OFF = 0

    # Class Methods
    # ------------------
    def __init__(self, master=None, **kwargs):
        """
        LED constructor arguments:
        - master: Parent object.
        - kwargs: LED constructor accepts the following keyword arguments...
            - size: Size of LED; >0, default 100.
            - casewidth: Width of the LED case border; >=0, default 10.
            - state: Initial state of LED on/off; boolean, default False.
            - diodecolor: Color of the LED light; accepts RGB value string
                i.e. "#fff" for white, or local color names; default "white".
            - bulbcolor: Color of the bulb which filters LED light; accepts
                RGB value string, or local color names; default "white".
            - reflectstyle: Binary flag for 3 reflection-styling options:
                0b001=visible (yes/no), 0b010=color (bulb/monotone),
                0b100=bightness algorithm (quadratic/linear); default 0b111.
            - faderate: Time at which the LED takes to reach full brightness,
                in ms (gives warm up/cool down appearance); >=0, default 0.
            - blinkrate: Time at which the LED turns on/off automatically,
                in ms (won't blink if set to 0); >=0, default 0.

        Example:
            LED(size=125, bulbcolor='green', state=LED.ON)

        """

        self.state = LED.OFF  # LED state (on/off)
        self.faderate = 0  # Amount of time (in ms) to reach on/off; Gives the appearance of warming up/cooling down
        self.blinkrate = 0  # Controls how fast (in ms) the LED blinks; Set to 0 to disable blinking
        self.fadeID = 0  # keeps track of the timer after-event ID used in the LED 'fade' capability function
        self.blinkID = 0  # keeps track of the timer after-event ID used in the LED 'blink' capability function
        self.fadetimestep = 20  # time step, in ms, of the fade function
        self.isblinking = False  # Flag whether LED is currently in blinking mode

        size = 100  # Size of LED
        casewidth = 10  # Size of LED case border
        initstate = self.state  # Initial state of LED
        diodecolor = 'white'  # Color of the light emitting diode inside the bulb casing
        bulbcolor = 'white'  # Color of bulb casing (white = clear); Makes the bulb colored when off
        # Note diode and bulb color are bitwise and'ed i.e. the bulb 'filters' the diode color like a real colored bulb
        # This behavior can be modified in the change_color function so they are bitwise or'ed to combine colors
        reflectstyle = 0x7  # Reflection options: 0b001=visible, 0b010=color, 0b100=brightness rate (quadratic/linear)

        # Parse keyword arguments
        # -----------------------
        for key, value in kwargs.items():
            if key == 'size':
                if value > 0:
                    size = value
                else:
                    raise ViewidgetError('LED size must be greater than zero')
            elif key == 'casewidth':
                if value >= 0:
                    casewidth = value
                else:
                    raise ViewidgetError('LED casewidth must be greater than or equal to zero')
            elif key == 'state':
                initstate = value
            elif key == 'diodecolor':
                if value is not None:
                    diodecolor = value
            elif key == 'bulbcolor':
                if value is not None:
                    bulbcolor = value
            elif key == 'reflectstyle':
                try:
                    reflectstyle = eval(hex(value))
                except TypeError:
                    warnings.warn('LED could not set reflectionsytle: must be an integer', ViewidgetWarning)
            elif key == 'faderate':
                self.set_faderate(value)
            elif key == 'blinkrate':
                self.set_blinkrate(value)
            else:
                raise ViewidgetError('LED init keyword "%s" unknown' % key)

        # Set initial values and check for user input errors
        # --------------------------------------------------
        if reflectstyle & 0x2:
            self.usemonotonereflection = False
        else:
            self.usemonotonereflection = True

        if reflectstyle & 0x4:
            self.usereflectquadraticstep = True
        else:
            self.usereflectquadraticstep = False

        try:
            if size / casewidth < 10:
                warnings.warn('LED casewidth must be less than or equal to 1/10 the size', ViewidgetWarning)
                casewidth = size / 10
        except ZeroDivisionError:
            pass

        # Call Canvas Constructor
        # -----------------------
        shadow3D = math.floor(math.log(2 * size, 10))
        light3D = math.ceil(shadow3D / 2)
        length = size + casewidth + shadow3D
        tkinter.Canvas.__init__(self, master, width=length, height=length, borderwidth=0, highlightthickness=0)

        # Draw LED
        # --------
        self.create_oval(casewidth, casewidth - light3D, size, size - light3D, width=casewidth, fill='white',
                         outline='white')
        self.create_oval(casewidth, casewidth + shadow3D, size, size + shadow3D, width=casewidth, fill='gray5',
                         outline='gray5')
        self.led = self.create_oval(casewidth, casewidth, size, size, width=casewidth, outline='gray60', tags='led')
        reflectoffset = (size - casewidth) / 6
        p1 = reflectoffset + casewidth
        p2 = size - reflectoffset
        self.reflection = self.create_arc(p1, p1, p2, p2, start=90, extent=90, width=(size - casewidth) / 20,
                                          style='arc', tags='reflection')
        if not reflectstyle & 0x1:
            self.itemconfig(self.reflection, state=tkinter.HIDDEN)

        # LED color
        # ---------
        self.current = {'led': None, 'reflection': None, 'brightness': 0}
        self.change_color(diodecolor, bulbcolor)

        self.turn(initstate)

    # End LED.__init__

    def _change_color(self, **colorargs):
        if colorargs.keys() <= self.current.keys():
            self.current.update(colorargs)
            self.itemconfig(self.led, fill=self.current['led'])
            self.itemconfig(self.reflection, outline=self.current['reflection'])
        else:
            diff = colorargs.keys() - self.current.keys()
            raise ViewidgetError('LED color keyword "%s" unknown' % diff.pop())

    def set_blinkrate(self, rate):
        """Set the time to pause in between switching LED ON/OFF, in ms."""
        if rate >= 0:
            self.blinkrate = int(round(rate))
            if self.blinkrate and self.state and not self.isblinking:
                self.blink()
            elif self.blinkrate == 0 and self.isblinking:
                self.blink_cancel()
                self.turnon()
        else:
            raise ViewidgetError('LED blinkrate must be greater than or equal to zero')

    def set_faderate(self, rate):
        """Set the time it takes for the LED to reach full brightness, in ms."""
        if rate >= 0:
            self.faderate = int(round(rate))
        else:
            raise ViewidgetError('LED faderate must be greater than or equal to zero')

    def turn(self, state):
        """Turn LED to given state, ON or OFF."""
        if not state:  # Turn OFF
            self.blink_cancel()
            if self.state:
                self.fade(LED.OFF)
        elif state and not self.state and not self.isblinking:  # Turn ON
            if self.blinkrate:
                self.blinkID = self.after(self.blinkrate, self.blink)
                self.isblinking = True
            self.fade(LED.ON)

    def turnon(self):
        """Turn LED ON."""
        self.turn(LED.ON)

    def turnoff(self):
        """Turn LED OFF."""
        self.turn(LED.OFF)

    def change_state(self):
        """Change state of LED."""
        self.turn(not self.state)

    def change_color(self, diodecolor=None, bulbcolor=None):
        """Change color of the LED and/or the bulb casing."""
        if bulbcolor is not None:
            # offcolor['led']= bulbcolor dimmed 25% luminosity; offcolor['reflection']= bulbcolor dimmed 50% luminosity
            self.bulbcolor_rgb = self.winfo_rgb(bulbcolor)
            hls = self.bulbcolor_hls = rgb_to_hls(*[i / 65535 for i in self.bulbcolor_rgb])
            offcolor = [int(round(i * 65535, 0)) for i in hls_to_rgb(hls[0], 0.25 * hls[1], hls[2])]
            if self.usemonotonereflection:
                sat = 0
            else:
                sat = hls[2]
            reflect = [int(round(i * 65535, 0)) for i in hls_to_rgb(hls[0], 0.5 * hls[1], sat)]
            self.offcolor = {'led': "#%04x%04x%04x" % tuple(offcolor), 'reflection': "#%04x%04x%04x" % tuple(reflect),
                             'brightness': 0}
        if diodecolor is not None:
            self.diodecolor_rgb = self.winfo_rgb(diodecolor)
        # oncolor['led'] = bitwise AND of diodecolor and bulbcolor; oncolor['reflection'] = white
        oncolor = [self.diodecolor_rgb[i] & self.bulbcolor_rgb[i] for i in range(3)]
        self.oncolor = {'led': "#%04x%04x%04x" % tuple(oncolor), 'reflection': "#FFFFFF", 'brightness': 1}
        # store oncolor HLS representation for brightness level calculations
        self.oncolor_hls = rgb_to_hls(*[i / 65535 for i in oncolor])
        self.set_brightness(self.current['brightness'])

    def set_brightness(self, level):
        """Set the luminosity of the LED, from 0% to 100%."""
        if level <= 0:
            self._change_color(**self.offcolor)
        # LED must be on or else it cannot get brighter
        elif self.state or level < self.current['brightness']:
            if level >= 1:
                self._change_color(**self.oncolor)
            else:
                # color luminosity goes from on.color's 1/4 to full luminosity -> 0.25*hls[1] to hsl[1]
                lum = self.oncolor_hls[1] * (0.75 * level + 0.25)
                if lum < 0.2 * self.bulbcolor_hls[1]:
                    color = self.offcolor['led']
                    reflect = self.offcolor['reflection']
                else:
                    color = "#%04x%04x%04x" % tuple(
                        [int(round(i * 65535, 0)) for i in hls_to_rgb(self.oncolor_hls[0], lum, self.oncolor_hls[2])])

                    # reflector luminosity goes from on.color's 1/2 luminosity to 1 (ie white) -> 0.5*hls[1] to 1
                    hue = self.oncolor_hls[0]
                    if self.usemonotonereflection:
                        sat = 0
                        targetlum = self.bulbcolor_hls[1]
                    else:
                        sat = self.oncolor_hls[2]
                        targetlum = self.oncolor_hls[1]
                    if self.usereflectquadraticstep:
                        power = 2
                    else:
                        power = 1
                    lum = (1 - 0.5 * targetlum) * level ** power + 0.5 * targetlum
                    reflect = "#%04x%04x%04x" % tuple([int(round(i * 65535, 0)) for i in hls_to_rgb(hue, lum, sat)])

                self._change_color(led=color, reflection=reflect, brightness=level)

    # End LED.set_brightness

    def blink_cancel(self):
        """Stop the LED from blinking."""
        if self.blinkID:
            self.after_cancel(self.blinkID)
            self.isblinking = False

    def blink(self):
        """Cause the LED to blink ON/OFF repeatedly at the set blinkrate."""
        self.blink_cancel()
        if self.blinkrate:
            self.change_state()
            if not self.state:
                self.blinkID = self.after(self.blinkrate, self.blink)
                self.isblinking = True

    def fade(self, state):
        """Cause the LED to fade to the given state (ON or OFF) at the set faderate."""

        # internal fade function
        def _fade(remaintime):
            if remaintime > self.fadetimestep:
                if len(latency) > 10:
                    latency.popleft()

                remainbrightness = targetbrightness - self.current['brightness']
                deltabrightness = (remainbrightness / remaintime) * (self.fadetimestep + mean(latency))
                self.set_brightness(self.current['brightness'] + deltabrightness)

                lastremaintime = remaintime
                remaintime = targetremainingtime - (time() - starttime) * 1000
                latency.append(lastremaintime - remaintime)
                self.fadeID = self.after(self.fadetimestep, _fade, remaintime - self.fadetimestep)
            else:
                self.set_brightness(targetbrightness)

        # fade function body
        if self.fadeID:
            self.after_cancel(self.fadeID)

        latency = deque()
        if state:
            targetbrightness = self.state = LED.ON
        else:
            targetbrightness = self.state = LED.OFF
        targetremainingtime = abs(targetbrightness - self.current['brightness']) * self.faderate
        starttime = time()
        _fade(targetremainingtime)

    # End LED.fade

# End LED class


###################
# Digit Viewidget #
###################
class Digit(tkinter.Canvas):
    """
    Tkinter-based seven-segment single digit widget.

    The seven-segment digit display is a denizen of the digital age. Multiple
    digits are combined together to form the basis for digital displays such
    as those found on digital clocks and LCD calculators, for example.

    The Viewidget Digit can be used singularly or combined as an array of
    digits. It contains basic methods to modify its appearance:
        - set_value(value): Sets the digit displayed to the value given.
        - change_color(fg, bg): Changes color of the foreground/background.
        - set_mask(mask): Low level way to turn on/off individual segments.

    """

    # Class Attributes
    # ------------------
    Masks = {
        0: 0b0111111, '0': 0b0111111,
        1: 0b0101000, '1': 0b0101000,
        2: 0b1011011, '2': 0b1011011,
        3: 0b1101011, '3': 0b1101011,
        4: 0b1101100, '4': 0b1101100,
        5: 0b1100111, '5': 0b1100111,
        6: 0b1110111, '6': 0b1110111,
        7: 0b0101001, '7': 0b0101001,
        8: 0b1111111, '8': 0b1111111,
        9: 0b1101111, '9': 0b1101111,
        0xa: 0b1111101, 'a': 0b1111101, 'A': 0b1111101,
        0xb: 0b1110110, 'b': 0b1110110, 'B': 0b1110110,
        0xc: 0b0010111, 'c': 0b0010111, 'C': 0b0010111,
        0xd: 0b1111010, 'd': 0b1111010, 'D': 0b1111010,
        0xe: 0b1010111, 'e': 0b1010111, 'E': 0b1010111,
        0xf: 0b1010101, 'f': 0b1010101, 'F': 0b1010101
    }

    # Class Methods
    # ------------------
    def __init__(self, master=None, **kwargs):
        """
        Digit constructor arguments:
        - master: Parent object.
        - kwargs: Digit constructor accepts the following keyword arguments...
            - size: Height of Digit (width is 2/3*size); >0, default 100.
            - value: Initial value of Digit; 0-9 & A-F (None=blank), default 0.
            - background or bg: Color of background; accepts RGB value string
                i.e. "#fff" for white, or local color names; default "black".
            - foreground or fg: Color of digit segments; accepts RGB value
                string, or local color names; default "red".

        Example:
            Digit(size=115, value=8, fg='green')

        """

        self.value = 8  # value set to 8 because that will be the display if users supplies a bad value at construction
        size = 100  # height of Digit; width is 2/3*size
        bg = 'black'  # default background color
        fg = 'red'  # default digit color
        initvalue = 0  # default value of Digit
        # Parse keyword arguments
        # -----------------------
        for key, value in kwargs.items():
            if key == 'size':
                if value > 0:
                    size = value
                else:
                    raise ViewidgetError('Digit size must be greater than zero')
            elif key == 'value':
                initvalue = value
            elif key == 'background' or key == 'bg':
                bg = value
            elif key == 'foreground' or key == 'fg':
                fg = value
            else:
                raise ViewidgetError('Digit init keyword "%s" unknown' % key)

        # Call Canvas Constructor
        # -----------------------
        tkinter.Canvas.__init__(self, master, height=size, width=size * 2 / 3, borderwidth=0, highlightthickness=0)

        # Draw DigitalDisplay
        # -------------------
        self.create_rectangle(0, 0, size, size, fill=bg, outline=bg, tags='bg')
        self.segments = []
        x1 = y1 = size * 9 / 100
        x2 = size * 57 / 100
        y2 = size * 89 / 100
        y3 = size * 49 / 100
        width = max(size // 175, 1)

        # Two trapezoids
        # --------------
        # first segment
        xy1 = (x1, y1)
        xy2 = (x2, y1)
        xy3 = (x2 - size * 1 / 10, y1 + size * 1 / 10)
        xy4 = (x1 + size * 1 / 10, y1 + size * 1 / 10)
        coords = [xy1, xy2, xy3, xy4]
        seg = self.create_polygon(coords, fill=fg, outline=bg, width=width, tags='fg')
        self.segments.append(seg)
        # second segment
        xy1 = (x1, y2)
        xy2 = (x2, y2)
        xy3 = (x2 - size * 1 / 10, y2 - size * 1 / 10)
        xy4 = (x1 + size * 1 / 10, y2 - size * 1 / 10)
        coords = [xy1, xy2, xy3, xy4]
        seg = self.create_polygon(coords, fill=fg, outline=bg, width=width, tags='fg')
        self.segments.append(seg)

        # Four 5-siders
        # -------------
        coords = [(x1, y1), (x2, y1), (x1, y2), (x2, y2)]
        for x, y in coords:
            xdir = [-1, 1][x == x1]
            ydir = [1, -1][y == y1]
            xy1 = (x, y)
            xy2 = (x, y3 + ydir * size * 1 / 20)
            xy3 = (x + xdir * size * 1 / 20, y3)
            xy4 = (x + xdir * size * 1 / 10, y3 + ydir * size * 1 / 20)
            xy5 = (x + xdir * size * 1 / 10, y - ydir * size * 1 / 10)
            coords = [xy1, xy2, xy3, xy4, xy5]
            seg = self.create_polygon(coords, fill=fg, outline=bg, width=width, tags='fg')
            self.segments.append(seg)

        # Single 6-sider (middle)
        # -----------------------
        # seventh segment
        xy1 = (x1 + size * 1 / 20, y3)
        xy2 = (x1 + size * 1 / 10, y3 - size * 1 / 20)
        xy3 = (x2 - size * 1 / 10, y3 - size * 1 / 20)
        xy4 = (x2 - size * 1 / 20, y3)
        xy5 = (x2 - size * 1 / 10, y3 + size * 1 / 20)
        xy6 = (x1 + size * 1 / 10, y3 + size * 1 / 20)
        coords = [xy1, xy2, xy3, xy4, xy5, xy6]
        seg = self.create_polygon(coords, fill=fg, outline=bg, width=width, tags='fg')
        self.segments.append(seg)

        self.set_value(initvalue)

    # End Digit.__init__

    def set_value(self, value):
        """Set display to the digital value (if valid)."""
        if value in self.Masks:
            self.set_mask(self.Masks[value])
            self.value = value
        elif value is None:
            self.set_mask(0)
            self.value = None

    def set_mask(self, mask):
        """Set which segments are activated."""
        for seg in self.segments:
            if 2 ** self.segments.index(seg) & mask:
                state = tkinter.NORMAL
            else:
                state = tkinter.HIDDEN
            self.itemconfig(seg, state=state)

    def change_color(self, foreground=None, background=None):
        """Change color of the segments and/or background."""
        if foreground is not None:
            self.itemconfig('fg', fill=foreground)
        if background is not None:
            self.itemconfig('bg', fill=background)
            self.itemconfig('bg', outline=background)
            self.itemconfig('fg', outline=background)

# End Digit class
