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
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def colorWipeLumen(strip,wait_ms=60):
    """Wipe color across display a pixel at a time."""
    start = 0
    for y in range(0, 200, 1):
        color = Color(int(round(y)), int(round(y)), int(round(y)))
        for i in range(strip.numPixels()):
            if(i == strip.numPixels()):
                color = Color(int(round(y)), int(round(y*0.664)), int(round(y*0.2396)))
                strip.setPixelColor(i, color)
            else:
                color = Color(int(round(y + 50)), int(round((y + 50) * 0.664)), int(round((y + 50) * 0.2396)))
                strip.setPixelColor(i, color)

            #strip.show()
        time.sleep(wait_ms / 1000.0)
        strip.show()


def colorStrip(strip, color):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()


# Define functions which animate LEDs in various ways.
def colorWipeReverse(strip, color, wait_ms=60):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(strip.numPixels() - 1 - i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)