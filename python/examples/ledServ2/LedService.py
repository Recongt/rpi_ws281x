import argparse
import multiprocessing
import time
from rpi_ws281x import *
from LEDMEthods import *
import RPi.GPIO as GPIO
from threading import Thread

# LED strip configuration:
LED_COUNT = 120  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

# threads
exitFlag = 0
mutex = multiprocessing.Lock()

class MyList:
    def __init__(self):
        self.firstValue = 1000
        self.secondValue = 1000
        self.thirdValue = 1000

    def avg(self):
        return (self.firstValue + self.secondValue + self.thirdValue) / 3

    def nextValue(self, newValue):
        self.thirdValue = self.secondValue
        self.secondValue = self.firstValue
        self.firstValue = newValue




def distanceProcess(GPIO_Trigger, GPIO_Echo, GPIO_Trigger2, GPIO_Echo2, eventLong, eventShort, reportTime, triggerDistance1,
                    triggerDistance2):
    # GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(GPIO_Trigger, GPIO.OUT)
    GPIO.setup(GPIO_Echo, GPIO.IN)

    GPIO.setup(GPIO_Trigger2, GPIO.OUT)
    GPIO.setup(GPIO_Echo2, GPIO.IN)


    try:
        list1 = MyList()
        list2 = MyList()

        while True:
            # set Trigger to HIGH
            GPIO.output(GPIO_Trigger2, True)

            # set Trigger after 0.01ms to LOW
            time.sleep(0.00001)
            GPIO.output(GPIO_Trigger2, False)
            StartTime2 = time.time()
            StopTime2 = time.time()

            # save StartTime
            while GPIO.input(GPIO_Echo2) == 0:
                StartTime2 = time.time()

            # save time of arrival
            while GPIO.input(GPIO_Echo2) == 1:
                StopTime2 = time.time()

            # time difference between start and arrival
            TimeElapsed2 = StopTime2 - StartTime2
            # multiply with the sonic speed (34300 cm/s)
            # and divide by 2, because there and back
            distance2 = (TimeElapsed2 * 34300) / 2

            list2.nextValue(distance2)
            if(list2.avg()<100):
                eventLong.set()
            else:
                eventLong.clear()



            ##############
            # set Trigger to HIGH
            GPIO.output(GPIO_Trigger, True)

            # set Trigger after 0.01ms to LOW
            time.sleep(0.00001)
            GPIO.output(GPIO_Trigger, False)
            StartTime = time.time()
            StopTime = time.time()

            # save StartTime
            while GPIO.input(GPIO_Echo) == 0:
                StartTime = time.time()

            # save time of arrival
            while GPIO.input(GPIO_Echo) == 1:
                StopTime = time.time()

            # time difference between start and arrival
            TimeElapsed = StopTime - StartTime
            # multiply with the sonic speed (34300 cm/s)
            # and divide by 2, because there and back
            distance = (TimeElapsed * 34300) / 2
            list1.nextValue(distance)
            if (list1.avg() < 100):
                eventShort.set()
            else:
                eventShort.clear()
            time.sleep(0.01)



    except (RuntimeError, KeyboardInterrupt) as e:
        print("watek padl zamkniety dostep do GPIO")
        print('blad: ',str(e))
        GPIO.cleanup()  # reset all GPIO


if __name__ == '__main__':

    TIME_FOR_LIGHT_Sec = 10
    TIME_FOR_SILENCE_Sec = 5
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
        thread_safe = False
        is_blinding = False
        timeStart = time.time()

        eventLong = multiprocessing.Event()
        eventShort = multiprocessing.Event()



        p = multiprocessing.Process(target=distanceProcess, args=(38, 37, 16, 15, eventLong, eventShort, 1000, 100, 100,))
        p.start()

        while True:
            stateLong =eventLong.is_set()
            stateShort = eventShort.is_set()
            shortLed = Thread(target=processData, args=(strip, Color(255, 120, 33), 40, False, thread_safe, mutex))
            if stateShort and not is_blinding:
                colorWipeLumen(strip, 10)
                shortLed.start()
                is_blinding = True
                timeStart = time.time()
                if shortLed.is_alive():
                    print("Wątek sonic żyje")
                    time.sleep(1)
                else:
                    print("Wątek sonic leży")
            elif stateShort and is_blinding and (time.time() - timeStart > TIME_FOR_SILENCE_Sec):
                time.sleep(0.5)
                timeStart = time.time()
                shortLed.start()
                
        ##long
            longLed = Thread(target=processData, args=(strip, Color(255, 120, 133), 40, True, thread_safe, mutex))
            if (stateLong) and not is_blinding:
                colorWipeLumen(strip, 10)
                longLed.start()
                is_blinding = True
                timeStart = time.time()

                if longLed.is_alive():
                    print("Wątek ir żyje")
                    time.sleep(1)
                else:
                    print("Wątek ir leży")


            elif (stateLong) and is_blinding and (time.time() - timeStart > TIME_FOR_SILENCE_Sec):
                timeStart = time.time()
                if longLed.is_alive():
                    time.sleep(0.5)
                else:
                    longLed = Thread(target=processData, args=(strip, Color(255, 120, 133), 40, True, thread_safe, mutex))
                    longLed.start()
                    is_blinding = True

            print("przed wylączaniem")
            if is_blinding & ((time.time() - timeStart) > TIME_FOR_LIGHT_Sec):
                if longLed.is_alive() or shortLed.is_alive():
                    print("zaczekam az czas sie skonczy")
                    time.sleep(0.1)
                elif (time.time() - timeStart) > TIME_FOR_LIGHT_Sec & is_blinding:
                    print("Czas sie skonczył wyłączam")
                    print((time.time() - timeStart) > TIME_FOR_LIGHT_Sec & is_blinding)
                    print((time.time() - timeStart))
                    colorWipeDimming(strip, 15)
                    is_blinding = False

            time.sleep(0.4)




    except (RuntimeError, KeyboardInterrupt):
        print('Exception')
        time.sleep(1000.0 / 1000.0)
        if longLed.is_alive():
            longLed.join()
        if shortLed.is_alive():
            shortLed.join()
        t3 = Thread(target=processData, args=(strip, Color(0, 0, 0), 0.005, True, thread_safe, mutex))
        t3.start()


    finally:
        #GPIO.cleanup()  # reset all GPIO
        print("Program ended")