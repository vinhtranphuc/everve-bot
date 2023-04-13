import logging
import threading
import time

def worker(event, i):
    print(f"\n{time.strftime('%X')} : start wait thread :", i)
    event.wait(10)
    print(f"\n{time.strftime('%X')} : end wait thread :", i)

def main():
    event = threading.Event()

    for i in range(1, 10):
        print('\n-----------')
        print('\nSTART THREAD :',i)
        thread = threading.Thread(target=worker, args=(event,i))
        thread.start()
        print('\n-----------')

if __name__ == "__main__":
    idList = [1,2,3,9,1,4,5]
    blackList = [3,4,1,7,9,12,13,15]
    exceptList = list(set(idList) - set(list(set(idList) - set(blackList))))
    print(exceptList)

