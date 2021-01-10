import RPi.GPIO as GPIO
import time


def irSensor1(sensorIr1, reportTime):
    # IR sensor
    GPIO.setmode(GPIO.BOARD)  # Set GPIO to pin numbering
    pir = 8  # Assign pin 8 to PIR
    GPIO.setup(pir, GPIO.IN)  # Setup GPIO pin PIR as input
    print("Sensor initializing . . .")
    time.sleep(2)  # Give sensor time to startup
    print("Active")
    print("Press Ctrl+c to end program")

    print('jestem w watku sensora')
    try:
        while True:
            if GPIO.input(pir) == True:
                sensorIr1.set()
            else:
                sensorIr1.clear()
            time.sleep(reportTime / 1000.0)
    except RuntimeError:
        print("watek padl zamkniety dostep do GPIO")
        GPIO.cleanup()  # reset all GPIO

def getIrState():
    GPIO.setmode(GPIO.BOARD)  # Set GPIO to pin numbering
    pir = 8  # Assign pin 8 to PIR
    GPIO.setup(pir, GPIO.IN)  # Setup GPIO pin PIR as input

    try:
        if GPIO.input(pir) == True:
            return True
        else:
            return False
    except RuntimeError:
        print("watek padl zamkniety dostep do GPIO")
    finally:
        GPIO.cleanup()  # reset all GPIO