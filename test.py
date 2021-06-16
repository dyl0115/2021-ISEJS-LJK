import threading
from playsound import playsound

class Thread1(threading.Thread):
    def run(self) -> None:
        for i in range(10):
            print("hello")


class Thread2(threading.Thread):
    def run(self) -> None:
        for i in range(4):
            playsound("./timeout.mp3")



t1 = Thread1()
t1.start()
t2 = Thread2()
t2.start()