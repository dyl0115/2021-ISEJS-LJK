import threading
import time
from playsound import playsound

counter = 0

def sound():

    while True:
        if counter > 30 and counter < 100:
            playsound("./timeout.mp3")


th2 = threading.Thread(target = sound)

def count():
    while True:
        global counter
        counter += 1
        time.sleep(0.1)
        print(counter)
   
th1 = threading.Thread(target = count)

th1.start()
th2.start()
