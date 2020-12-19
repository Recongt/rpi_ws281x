#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import argparse
from threading import Thread, Lock
import threading
import time


from rpi_ws281x import *

# LED strip configuration:
LED_COUNT = 70  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

#threads
exitFlag = 0
mutex = Lock()

def processData(strip, thread_safe):
    if thread_safe:
        mutex.acquire()
    try:
        colorWipe(strip, Color(205, 11, 2), 80)  # Red wipe
    finally:
        if thread_safe:
            mutex.release()

def processDataReverse(strip, thread_safe):
    if thread_safe:
        mutex.acquire()
    try:
        colorWipeReverse(strip, Color(255, 80, 30), 80)  # Red wipe
    finally:
        if thread_safe:
            mutex.release()

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=60):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


# Define functions which animate LEDs in various ways.
def colorWipeReverse(strip, color, wait_ms=60):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(strip.numPixels()-1 - i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=50, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(strip, wait_ms=50, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(500.0 / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

class myThread(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        strip.begin()
        print("Starting " + self.name)

        print('Color wipe animations.')
        colorWipe(strip, Color(85, 11, 2),80)  # Red wipe
        exit()
        print("Exiting " + self.name)

class myThreadReverse(threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        strip.begin()
        print("Starting " + self.name)
        print('Color wipe animations.')
        colorWipeReverse(strip, Color(85, 11, 2),80)  # Red wipe
        print("Exiting " + self.name)
        exit()


def print_time(threadName, counter, delay):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

    try:
        while True:
            print('Color wipe animations.')
            #colorWipe(strip, Color(85, 11, 2),0.00001)  # Red wipe
            #colorWipe(strip, Color(255, 123, 23),10)  # Red wipe
            #colorWipe(strip, Color(255, 120, 33))  # Red wipe
            #colorWipeReverse(strip, Color(0, 0, 0),5)  # Red wipe
            #time.sleep(2000.0 / 1000.0)
            # Create new threads
            #thread1 = myThread(1, "Thread-1", 1)
            #thread2 = myThreadReverse(2, "Thread-2", 2)

            # Start new Threads
            #thread1.start()
            #thread2.start()
            thread_safe = False
            t = Thread(target=processData, args=(strip, thread_safe))
            t.start()

            t2 = Thread(target=processDataReverse, args=(strip, thread_safe))
            t2.start()

            time.sleep(5000.0 / 1000.0)
            # colorWipe(strip, Color(0,0,0), 10)
            # colorWipe(strip, Color(0, 0, 0))  # Blue wipe
            # colorWipe(strip, Color(0, 0, 255))  # Green wipe
            # print ('Theater chase animations.')
            # theaterChase(strip, Color(127, 127, 127))  # White theater chase
            # theaterChase(strip, Color(127,   0,   0))  # Red theater chase
            # theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
            # print ('Rainbow animations.')
            # rainbow(strip)
            # rainbowCycle(strip)
            # theaterChaseRainbow(strip)

    except (RuntimeError, KeyboardInterrupt):
        time.sleep(2000.0 / 1000.0)
        colorWipe(strip, Color(0,0,0), 0.001)
