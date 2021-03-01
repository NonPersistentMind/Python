import sys, os

def lister(root):
    for (dir, subdirs, files) in os.walk(root):
        print('[ ' + dir + ' ]')
        for filename in files:
            print(os.path.join(dir, filename))
        
if __name__ == "__main__":
    if len(sys.argv) == 2:
        lister(sys.argv[1])
    else:
        lister(os.curdir)