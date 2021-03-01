import os, time

def counter(count):
    for i in range(count):
        time.sleep(1)
        print('[%s] => %s' % (os.getpid(), i))

for i in range(5):
    newpid = os.fork()
    if newpid != 0:
        print('A process with pid %s spawned!' % newpid)
    else:
        counter(5)
        os._exit(0)

