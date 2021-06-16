from multiprocessing import Process
from playsound import playsound

sound_on = False

def print_hello():
    count = 0
    while True:
        count += 1
        print("안녕 ", count)

        if count % 10000 == 0:
            sound_on = True
        else:
            sound_on = False

def print_sound():
    print(sound_on)
    if sound_on:
        playsound("./timeout.mp3")
    else:
        pass

if __name__ == '__main__':
    p1 = Process(target = print_hello)
    p2 = Process(target = print_sound)

    p1.start()
    p2.start()

    p1.join()
    p2.join()