import argparse
import multiprocessing
import time
from rpi_ws281x import *
from LEDMEthods import *
from IRService import *
from UltraSonicService import *
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
        # Create NeoPixel object with appropriate configuration.
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        # Intialize the library (must be called once before other functions).
        strip.begin()
        thread_safe = False
        is_blinding = False
        timeStart = time.time()

        while True:
            time.sleep(0.2)
            sonicState = distanceLessThan(90, 38, 37)
            time.sleep(0.003)
           # irState = getIrState()
            irState =distanceLessThan(90, 16, 15)
            tSonic = Thread(target=processData, args=(strip, Color(255, 120, 33), 40, False, thread_safe, mutex))
            if sonicState and not is_blinding:
                print("Motion Sonic Detected!xD")
                colorWipeLumen(strip, 10)
                tSonic.start()
                is_blinding = True
                timeStart = time.time()

                if tSonic.is_alive():
                    print("Wątek sonic żyje")
                    #time.sleep(1)
                else:
                    print("Wątek sonic leży")
            elif sonicState and is_blinding and (time.time() - timeStart > TIME_FOR_SILENCE_Sec):
                print('Sonic aktywny ale nadal świeci')
                timeStart = time.time()
                tSonic.start()

            #IR
            tIr = Thread(target=processData, args=(strip, Color(255, 120, 133), 40, True, thread_safe, mutex))
            if(irState) and not is_blinding:
                print("Motion Ir Detected!xD")
               # tIr = Thread(target=processData, args=(strip, Color(255, 120, 133), 40, True, thread_safe, mutex))
                colorWipeLumen(strip, 10)
                tIr.start()
                is_blinding = True
                timeStart = time.time()

                if tIr.is_alive():
                    print("Wątek ir żyje")
                    #time.sleep(1)
                else:
                    print("Wątek ir leży")


            elif(irState) and is_blinding and (time.time() - timeStart > TIME_FOR_SILENCE_Sec):
                print("Ir Motion Detected! But is blindig")
                timeStart = time.time()
                print("odpalam nową wiazakę")
                if tIr.is_alive():
                    print("ir zywy")
                else:
                    tIr = Thread(target=processData, args=(strip, Color(255, 120, 133), 40, True, thread_safe, mutex))
                    tIr.start()
                    is_blinding=True

            print("przed wylączaniem")
            if is_blinding & ((time.time() - timeStart) > TIME_FOR_LIGHT_Sec):
                if tIr.is_alive() or tSonic.is_alive():
                    print("zaczekam az czas sie skonczy")
                    time.sleep(0.1)
                elif (time.time() - timeStart) >TIME_FOR_LIGHT_Sec & is_blinding:
                    print("Czas sie skonczył wyłączam")
                    print((time.time() - timeStart) >TIME_FOR_LIGHT_Sec & is_blinding)
                    print((time.time() - timeStart))
                    colorWipeDimming(strip, 15)
                    is_blinding = False



    except (RuntimeError, KeyboardInterrupt):
        if tIr.is_alive():
            tIr.join()
        if tSonic.is_alive():
            tSonic.join()
        t3 = Thread(target=processData, args=(strip, Color(0, 0, 0), 0.005, True, thread_safe, mutex))
        t3.start()

    finally:
      #  GPIO.cleanup()  # reset all GPIO
        print("Program ended")
