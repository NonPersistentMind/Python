import glob
import os

for filename in glob.glob(os.getcwd()+'/*'):
    location, name = os.path.split(filename)
    print(location, name, '=>', os.path.join('/home/andrew_lick/', name))
