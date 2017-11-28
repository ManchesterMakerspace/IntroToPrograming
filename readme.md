# Intro To Programing Class Examples

This repo contains a series of code examples all a geared towards first time experiences programing. The class utilized the Circuit Playground Express as a platform to experiment with the Python programing language.

[The Circuit Playground Express](https://www.adafruit.com/product/3333) (or CPX for short):  Is and Arduino compatible microcontroller with input and output components that make it easy to get started and experiment. The device can be programed in three separate ways. One with the Arduino IDE, Two is with Microsoft Make Code, Three is by using Python. The included examples use Python, each folder contains a code.py file that can be transfered to the CPX when it has the flashed with the proper [firmware](https://learn.adafruit.com/adafruit-circuit-playground-express/circuitpython-quick-install) and includes the proper [libraries](https://learn.adafruit.com/adafruit-circuit-playground-express/installing-libraries). Refer to Adafruit's [complete guide](https://learn.adafruit.com/adafruit-circuit-playground-express/overview) to learn more about the board and find more examples to build derive your own creations from

## Class Notes

The goal of the class is to introduce programing concepts and ideas to those starting from little to no experience. With less emphasis on language peculiarities, electronics engineering, or professional disciplines. The class will cover some tougher concepts like object orientation and asynchronous programing. This is to help overcome blockers in taking the next steps in exploring practical applications and going beyond examples. Its okay to have a hard time with these concepts at first and use global variables and sleep/delay from related examples on in the Adafruit Learning system or Arduino Playground. The examples are meant to show better patterns to follow and to avoid struggling to find good examples when the related problems do arise.

Terms that might be used during the class are covered in the [Terms Handout]()

## Troubleshooting Notes

The developer edition of the CPX has some quirks with writing files to it. Sometimes if a files takes too long to right the board can get into a bad state. If this issue occurs with your board please follow the thread [here](https://forums.adafruit.com/viewtopic.php?f=58&t=126031) to come up with a way to rectify the issue. The best answer to avoiding this issue is to use the [MU text editor](https://codewith.mu/#download) This editor also conveniently contains a python REPL to debug your code. Also you can use the terminal to write the board in a safe way. The following is an example.

 ```cp code.py /media/yourusername/CIRCUITPY/code.py; sync```
