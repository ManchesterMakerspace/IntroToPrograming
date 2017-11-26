# Async user input ~ Copyright 2017 Paul Beaudet ~ MIT License
# Beginer demonstration of multi-tasking and user input
from digitalio import DigitalInOut, Direction, Pull       # Methods in digitalio library that we would like
import board                                              # Board library, pinout shorthand
import time                                               # Time library with .sleep() and .monotonic() methods
# Libraries help simplify and abstract details so more time can be spent solving higer level problems

# Classes and Functions are ways for a programer to organize code
# functions and methods are nested in "def". Differance between them is a method is nested in a class which has persistent properties
class Output():                                           # classes create a template of properties and methods called an Object
    def __init__(self, pin):                              # methods are replicable units of code
        # in a "def" parameters inside of parentheses(parameters) represent data that can be passed to this unit of code
        self.output = DigitalInOut(pin)                   # self refers to a unique persistent property of object that will be created
        self.output.direction = Direction.OUTPUT          # hardware: remember pin's role (deliver power)
        self.blinking = False                             # remember if we are blining, we are not blinking
    def turnOff(self):                                    # def is a definition of a "methods" (in class) or "function" (outside class)
        self.output.value = False                         # .value property tells pin to deliver or in this case not deliver power
    def turnOn(self):                                     # Descriptive method names like "turnOn" are helpful
        self.output.value = True                          # Turn output ON (True or 1, off is False or 0)
    def blink(self, durration=0.4):                       # Intiates blinkin Default durration of 400 milliseconds
        self.blinking = not self.blinking                 # remember whether we are blinking or not
        self.blinkDurration = durration                   # remember requested durration
        self.lastBlink = time.monotonic()                 # monotonic() returns seconds(with milliseconds as a fraction) from start up
    def run(self):                                        # meant to be polled in a non blocking event loop
        if self.blinking:                                 # are we blinking?
            durration = time.monotonic() - self.lastBlink # temporarily note how long has it been since we blinked
            if durration > self.blinkDurration:           # detect when we need to blink again
                self.output.value = not self.output.value # Set actual output state 
                self.lastBlink = time.monotonic()         # Set new time to measure against

class Button():                                           # multiple unique button objects can be created with this one class
    def __init__(self, pin, bounceTime=0.01):             # __init__ Constructors are called when an instance of an object is created
        self.button = DigitalInOut(pin)                   # set pin of this unique button to the pin that is given on construction
        self.button.direction = Direction.INPUT           # direction of a button is always set to INPUT
        self.button.pull = Pull.DOWN                      # Use internal pull down resistor, opposed to using an external resistor
        self.changeStart = time.monotonic()               # give a time to start from to keep track of passing time
        self.bouncePeriod = False                         # bounces happen in a window of milliseconds when metal surfaces connect
        self.held = False                                 # remember if this button is being held or not
        self.lastGoodState = self.button.value            # remember first resting state
        self.bounceTime = bounceTime                      # 10 to 20 milliseconds is a good waiting range to ignore contact bounce
    def detect(self, onClick, onRelease, onHold=False):   # poll this method to detect button changes without detecting bounce
        stateDurration = time.monotonic() - self.changeStart # durration since last state change
        if self.bouncePeriod:                             # durring bounce period ( after a detected change )
            if stateDurration > self.bounceTime:          # escape out state changes from being detected
                self.bouncePeriod = False                 # conclude bounce period
        else:                                             # where there is no concern of bounce
            currentState = self.button.value              # placehold current button state, may change if parsed multiple times
            if self.lastGoodState == currentState:        # given state persist / remains same as last good state
                if currentState and stateDurration > 0.4 and not self.held: # given button is being held DOWN
                    self.held = True                      # Remember this button is being held
                    if onHold:                            # if a hold callback was passed
                        onHold(0.1)                       # execute that callback {blink} with a 100 millisecond durration
            else:                                         # given state changed, button pressed or released
                self.changeStart = time.monotonic()       # note timestamp of change to measure how long to ignore potential bounce and detect hold
                self.bouncePeriod = True                  # this button is now in a period of detecting a bounce
                self.held = False                         # note that this button is no longer being held in its state, redundant for release
                self.lastGoodState = currentState         # remember last good state to compare in future
                if currentState:                          # shorthand for if pressed. pressed == True
                    onClick()                             # execute callback to call on a click event
                else:                                     # opposite of being pressed is being released
                    onRelease()                           # execute release callback

# High level business end of code starts here!
# instantiate hardware that is going to be used
buttonA = Button(board.BUTTON_A)                       # Creates a unique instance of Button class with pin of button A
buttonB = Button(board.BUTTON_B)                       # ButtonB is a unique object from buttonA
led = Output(board.D13)                                # set up red light next to micro usb connector

# infinate loop where event possibilities are compared against appropriate time and state to occur
while True:                                            # continuously repeat: "Event Loop"
    buttonA.detect(led.turnOn, led.turnOff, led.blink) # Detect when button is pressed, pass "pointers" to methods to use AKA callbacks
    # methods/functions without parentheses reffer/point at the act. Using parentheses executes the action
    buttonB.detect(led.turnOn, led.turnOff, led.blink) # Also ignores button contact bounces that would produce false signals
    led.run()                                          # decides when blinking is appropriate
