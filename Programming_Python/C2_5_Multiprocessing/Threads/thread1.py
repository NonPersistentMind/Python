import _thread

def child(tid):
    print('Hello from thread %s' % tid)

def parent():
    i=0
    while True:
        i+=1 
        if input()=='q':
            break
        _thread.start_new_thread(child, (i,))

parent()

