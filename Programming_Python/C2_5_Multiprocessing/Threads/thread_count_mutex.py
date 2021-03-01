import _thread as thread, time

mutex = thread.allocate_lock()

def counter(myId, count):
    for i in range(count):
        time.sleep(1)       # Simulation of the real job
        mutex.acquire()
        print('Thread %s is on %s' % (myId, i))
        mutex.release()

for i in range(5):
    thread.start_new_thread(counter, (i, 5))

time.sleep(6)
print('Main End')

