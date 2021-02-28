from math import sqrt
import numpy as np
from scipy import stats as st


def get_data_from_file(filename):
    """
    Returns a python list of numpy arrays formed from the specified file. 
    Example below will be converted to [np.array(67,80,48), np.array(24,56,42)] 

    File is structured like this:
    67
    80
    48
    %
    24
    56
    42
    So every number is on a newline and different samples are divided by a '%' symbol that is also on a newline

    filename:string - a path to the file where all the numbers reside
    """
    with open(filename, 'r') as file:
        data = []
        current_sample = []
        for line in file:
            if '%' in line:
                data.append(np.array(current_sample))
                current_sample = []
            else:
                current_sample.append(float(line))

        data.append(np.array(current_sample))

    return data


X, Y = get_data_from_file('another_file')
print(X.sum(), Y.sum(), sep='\n')
print((X**2).sum(), (Y**2).sum(), sep='\n')