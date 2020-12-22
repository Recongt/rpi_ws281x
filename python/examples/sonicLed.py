# Libraries
import RPi.GPIO as GPIO
import time

# GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

# set GPIO Pins
GPIO_TRIGGER = 20
GPIO_ECHO = 26

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


from rpi_ws281x import *

# LED strip configuration:
LED_COUNT = 50  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

# threads
exitFlag = 0

def colorWipe(strip, color, wait_ms=60):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def colorWipeByDistance(strip, color,distance, wait_ms=60):
    print(distance)
    print(LED_COUNT)
    val = LED_COUNT-((int(distance) * int(LED_COUNT)))/LED_COUNT
    borderledNumber = int(round(val))
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        if i > borderledNumber:
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
        else:
            strip.setPixelColor(i, Color(0, 0, 0))
            strip.show()
            time.sleep(wait_ms / 1000.0)


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance


if __name__ == '__main__':
    try:
        lastValue = 0
        lastValue2 =0
        # Create NeoPixel object with appropriate configuration.
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        strip.begin()
        while True:
            dist = distance()
            r = (dist+lastValue+lastValue2)/3

            brightValue = int(round(r))
            if brightValue > 244:
                brightValue = 255
            elif brightValue < 1:
                brightValue = 0

            red = brightValue
            blue = int(round(brightValue/0.2))
            green = int(round(brightValue/0.1))

            colorWipeByDistance(strip, Color(255, 93, 23), brightValue, 0.00001)  # Red wipe
            print(brightValue)
            print("Measured Distance = %.1f cm" % dist)
            time.sleep(0.2)
            lastValue2 =lastValue
            lastValue = dist

        # Reset by pressing CTRL + C
    except (RuntimeError, KeyboardInterrupt):
        colorWipe(strip, Color(0, 0, 0), 0.00001)
        print("Measurement stopped by User")
        GPIO.cleanup()