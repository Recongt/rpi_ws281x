import argparse
import multiprocessing
import time
from rpi_ws281x import *
from LEDMEthods import *
from IRService import *
from UltraSonicService import *
from threading import Thread

# LED strip configuration:
LED_COUNT = 20  # Number of LED pixels.
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

if __name__ == '__main__':
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
        # Create NeoPixel object with appropriate configuration.
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        strip.begin()
        thread_safe = False
        is_blinding = False
        sensorIr1 = multiprocessing.Event()
        irSensorDaemon = multiprocessing.Process(name='irSensor',
                                          target=irSensor1,
                                          args=(sensorIr1, 0.0003,))
        irSensorDaemon.start()
        print("Przed sonicem")
        sensorSonicState1 = multiprocessing.Event()
        sonicSensorDemon = multiprocessing.Process(name='sonicSensor',
                                          target=sonicSensor,
                                          args=(sensorSonicState1, 0.002,))
        sonicSensorDemon.start()

        while True:
            time.sleep(0.8)
            print(sensorIr1.is_set())
            print(sensorSonicState1.is_set())

            if sensorSonicState1.is_set():
                print("Motion Sonic Detected!xD")
                t = Thread(target=processData, args=(strip, Color(255, 120, 33), 40, False, thread_safe, mutex))
                t.start()
                is_blinding = True
                sensorSonicState1.clear()

                if t.is_alive():
                    print("Wątek sonic żyje")
                    #time.sleep(1)
                else:
                    print("Wątek sonic leży")

            elif(sensorIr1.is_set()):
                print("Motion Ir Detected!xD")
                t = Thread(target=processData, args=(strip, Color(255, 120, 133), 40, True, thread_safe, mutex))
                t.start()
                is_blinding = True
                sensorSonicState1.clear()

                if t.is_alive():
                    print("Wątek ir żyje")
                    #time.sleep(1)
                else:
                    print("Wątek ir leży")
            else:
                print("No motion Detected!xD")
                if is_blinding:
                    if t.is_alive():
                        time.sleep(0.5)
                    else:
                        t2 = Thread(target=processData, args=(strip, Color(0, 0, 0), 0.01, False, thread_safe, mutex))
                        t2.start()
                        is_blinding = False



    except (RuntimeError, KeyboardInterrupt):
        t.join()
        t3 = Thread(target=processData, args=(strip, Color(0, 0, 0), 0.005, True, thread_safe, mutex))
        t3.start()

    finally:
      #  GPIO.cleanup()  # reset all GPIO
        print("Program ended")
