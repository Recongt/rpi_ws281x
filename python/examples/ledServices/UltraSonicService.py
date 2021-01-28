import RPi.GPIO as GPIO
import time

def distance(GPIO_Trigger, GPIO_Echo):
    # GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BOARD)

    # set GPIO Pins

    GPIO_TRIGGER = 38
    GPIO_ECHO = 37

    if (GPIO_Trigger != None):
        GPIO_TRIGGER = GPIO_Trigger

    if (GPIO_Echo != None):
        GPIO_ECHO = GPIO_Echo

    # set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.01)
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





def sonicSensor(sensorSonicState1, reportTime, trigger_pin, echo_pin):

    print('jestem w watku sensora ultrasonicznego')
    try:
        lastValue = 0
        lastValue2 = 0
        while True:
            time.sleep(0.01)
            dist = distance(trigger_pin, echo_pin)
            roundDistance = (dist + lastValue + lastValue2) / 3
            print("Measured Distance = %.1f cm" % roundDistance)
            time.sleep(0.3)
            lastValue2 =lastValue
            lastValue = roundDistance

            if roundDistance < 100:
                sensorSonicState1.set()
            else:
                sensorSonicState1.clear()
            time.sleep(reportTime / 1000.0)
    except RuntimeError:
        print("watek padl zamkniety dostep do GPIO")
        GPIO.cleanup()  # reset all GPIO



def distanceLessThan(dist, trig_pin, echo_pin):
    dista = distance(trig_pin, echo_pin)
    dista1 = distance(trig_pin, echo_pin)
    dista2 = distance(trig_pin, echo_pin)

    avg_dista = (dista+dista1+dista2)/3
    print("Pin numer:", echo_pin, "Odleglosc: ", avg_dista)
    print(dist)
    print(avg_dista)
    if(avg_dista < dist):
        return True
    else:
        return False