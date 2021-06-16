from multiprocessing import Process
from playsound import playsound

sound_on = False
count = 0

def print_hello():
    global count
    global sound_on
    while True:
        count += 1
        print(count, ", ",sound_on)

        if count > 50000 == 0:
            sound_on = True

        

def print_sound():
    playsound("./timeout.mp3")


if __name__ == '__main__':

    p1 = Process(target = print_hello)
    p2 = Process(target = print_sound)

    p1.start()
    p2.start()

    p1.join()
    p2.join()