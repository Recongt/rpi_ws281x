import time
from rpi_ws281x import *

def processData(strip, color, speed, reverse, thread_safe, mutex):
    if thread_safe:
        mutex.acquire()
    try:
        if reverse:
            colorWipeReverse(strip, color, speed)
        else:
            colorWipe(strip, color, speed)
    finally:
        if thread_safe:
            mutex.release()

def colorWipe(strip, color, wait_ms=60):
    """Wipe color across display a pixel at a time."""
    blank = Color(0, 0, 0)
    for i in range(strip.numPixels()):
        if(i < strip.numPixels()):
            strip.setPixelColor(i+1, blank)
            strip.setPixelColor(i, color)
        else:
            strip.setPixelColor(i, color)

        strip.show()
        time.sleep(wait_ms / 1000.0)

def colorWipeLumen(strip,wait_ms=60):
    """Wipe color across display a pixel at a time."""
    start = 0
    for y in range(0, 100, 1):
        for i in range(strip.numPixels()):
            if(i == strip.numPixels()):
                color = Color(int(round(y)), int(round(y*0.564)), int(round(y*0.1896)))
                strip.setPixelColor(i, color)
            else:
                color = Color(int(round(y + 50)), int(round((y + 50) * 0.564)), int(round((y + 50) * 0.1896)))
                strip.setPixelColor(i, color)

            #strip.show()
        time.sleep(wait_ms / 1000.0)
        strip.show()

def colorWipeDimming(strip,wait_ms=60):
    """Wipe color across display a pixel at a time."""
    start = 0
    for y in range(0, 250, 1):
        z = strip.numPixels()-y-1


        for i in range(strip.numPixels()):
            if(i == strip.numPixels()):
                color = Color(valueGreatherThanZero(z), valueGreatherThanZero(z*0.564), valueGreatherThanZero(z*0.1896))
                strip.setPixelColor(i, color)
            else:
                color = Color(valueGreatherThanZero(z), valueGreatherThanZero(z*0.564), valueGreatherThanZero(z*0.1896))
                strip.setPixelColor(i, color)

            #strip.show()
        time.sleep(wait_ms / 1000.0)
        strip.show()

def valueGreatherThanZero(value):
    if (value <=0 ):
        return 0
    else:
        return int(round(value))

def colorStrip(strip, color):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()


# Define functions which animate LEDs in various ways.
def colorWipeReverse(strip, color, wait_ms=60):
    """Wipe color across display a pixel at a time."""
    blank = Color(0, 0, 0)
    for i in range(strip.numPixels()):
        strip.setPixelColor(strip.numPixels() - 1 - i, color)
        if(i>0):
            strip.setPixelColor(strip.numPixels()-2-i, blank)
        strip.show()
        time.sleep(wait_ms / 1000.0)