import time


isTimeEnd = False


timeStart=time.time()
time.sleep(1)
timeEnd=time.time()

print(timeEnd-timeStart)

while isTimeEnd == False:
    timeEnd=time.time()
    print(timeEnd-timeStart)
    if timeEnd-timeStart>10:
        print("juz czas")
        isTimeEnd = True
    else:
        print("jeszcze nie czas")
        time.sleep(0.5)

