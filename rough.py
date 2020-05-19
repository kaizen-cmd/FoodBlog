from threading import Thread
import time

def tester():
    while True:
        print("Hello")
        time.sleep(3)

t = Thread(target=tester)
t.start()
time.sleep(20)
print("Bye World")