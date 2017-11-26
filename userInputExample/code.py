# Async user input ~ Copyright 2017 Paul Beaudet ~ MIT License
from digitalio import DigitalInOut, Direction, Pull
import board
import time
    
class Output():
    def __init__(self, pin):
        self.output = DigitalInOut(pin)
        self.output.direction = Direction.OUTPUT
        self.blinking = False
    def turnOff(self):
        self.output.value = False
    def turnOn(self):
        self.output.value = True
    def blink(self, durration):
        self.blinking = not self.blinking
        self.blinkDurration = durration
        self.lastBlink = time.monotonic()
    def run(self):                                        # meant to be polled in a non blocking event loop
        if self.blinking:                                 # are we blinking?
            durration = time.monotonic() - self.lastBlink # how long has it been since we blinked
            if durration > self.blinkDurration:           # detect when we need to blink again
                self.output.value = not self.output.value # Set actual output state 
                self.lastBlink = time.monotonic()         # Set new time to measure against

class Button():
    def __init__(self, button, bounceTime=0.01):
        self.button = DigitalInOut(button)
        self.button.direction = Direction.INPUT
        self.button.pull = Pull.DOWN
        self.changeStart = time.monotonic()
        self.bouncePeriod = False
        self.held = False
        self.lastGoodState = self.button.value
        self.bounceTime = bounceTime
    def detect(self, onClick, onRelease, onHold):
        stateDurration = time.monotonic() - self.changeStart # durration since last state change
        currentState = self.button.value            # placehold current button state, may change if parsed multiple times
        if self.bouncePeriod:                       # durring bounce period ( after a detected change )
            if stateDurration > self.bounceTime:    # escape out state changes from being detected
                self.bouncePeriod = False           # conclude bounce period
        else:                                       # where there is no concern of bounce
            if self.lastGoodState == currentState:
                if currentState and stateDurration > 0.4 and not self.held:
                    self.held = True
                    onHold(0.1)
            else:
                self.changeStart = time.monotonic()
                self.bouncePeriod = True
                self.held = False
                self.lastGoodState = currentState
                if currentState:
                    onClick()
                else:
                    onRelease()

buttonA = Button(board.BUTTON_A)
buttonB = Button(board.BUTTON_B)
led = Output(board.D13)

while True:
    buttonA.detect(led.turnOn, led.turnOff, led.blink)
    buttonB.detect(led.turnOn, led.turnOff, led.blink)
    led.run()
