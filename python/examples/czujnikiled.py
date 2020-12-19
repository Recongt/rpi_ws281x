#!/usr/bin/python

import time

import RPi.GPIO as GPIO
from rpi_ws281x import *

# LED strip configuration:
LED_COUNT      = 5     # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

GPIO.setmode(GPIO.BOARD)  # Set GPIO to pin numbering
pir = 8  # Assign pin 8 to PIR
led = 15  # Assign pin 10 to LED
GPIO.setup(pir, GPIO.IN)  # Setup GPIO pin PIR as input
GPIO.setup(led, GPIO.OUT)  # Setup GPIO pin for LED as output
print("Sensor initializing . . .")
time.sleep(2)  # Give sensor time to startup
print("Active")
print("Press Ctrl+c to end program")

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=60):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

try:
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    while True:
        if GPIO.input(pir) == True:  # If PIR pin goes high, motion is detected
            print("Motion Detected!")
            GPIO.output(led, True)  # Turn on LED
            colorWipe(strip, Color(243, 95, 11))  # Red wipe
            time.sleep(1)  # Keep LED on for 4 seconds
            GPIO.output(led, False)  # Turn off LED
            time.sleep(0.01)
        else:
            colorWipe(strip, Color(0, 0, 0),1)  # Red wipe

except KeyboardInterrupt:  # Ctrl+c
    pass  # Do nothing, continue to finally

finally:
    GPIO.output(led, False)  # Turn off LED in case left on
    GPIO.cleanup()  # reset all GPIO
    print("Program ended")
