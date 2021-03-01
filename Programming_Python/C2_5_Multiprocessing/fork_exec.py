import os

proc_num = 0
while True:
    proc_id = os.fork()
    if proc_id==0:
        os.execlp('python3', 'python3', 'child.py', str(proc_num))
        assert False, 'error starting program'
    else:
        print('New process with ID %s has been started' % proc_id)
        proc_num+=1
        if input() =='q': break


