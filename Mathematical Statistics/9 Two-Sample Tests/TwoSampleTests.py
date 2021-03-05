import numpy as np
from math import sqrt
import scipy.stats as st
import warnings
import sys
arr = np.array
warn = warnings.warn


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



def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return 'WARNING: ' + str(msg) + '\n'


warnings.formatwarning = custom_formatwarning


def _define_basic_statistical_properties(first_sample, second_sample):
    return (first_sample_mean := first_sample.mean(),
            second_sample_mean := second_sample.mean(),
            S_x := first_sample.std(ddof=1),
            S_y := second_sample.std(ddof=1),
            n := len(first_sample),
            m := len(second_sample))


def _get_welchs_freedom_degrees(first_sample, second_sample):
    first_sample_mean, second_sample_mean, S_x, S_y, n,m = _define_basic_statistical_properties(first_sample, second_sample)
    
    theta = (S_x/S_y)**2

    numerator = (theta + n/m)**2
    denominator = theta**2/(n-1) + (n/m)**2 / (m-1)

    return round(numerator/denominator)


def one_sample_test(data, supposed_mean, alpha=0.5):
    sample_mean = data.mean()
    sample_std = data.std(ddof=1)
    n = len(data)
    return (sample_mean-supposed_mean)/(sample_std/n**0.5)


def two_sample_test(first_sample, second_sample, alpha=0.05, var_alpha=0.02):
    """
    A method that provides hypothesis test on whether means of two samples are equal or not.
    Before testing, method executes an F_test on two variances to determine if they are equal. In case of very obvious inequality, this method displays a warning

    first_sample:np.array - the first collection of observations to test on means equality
    second_sample:np.array - the second collection of observations to test on means equality
    """
    first_sample_mean = first_sample.mean()
    second_sample_mean = second_sample.mean()
    S_x = first_sample.std(ddof=1)
    S_y = second_sample.std(ddof=1)
    n = len(first_sample)
    m = len(second_sample)

    F = st.f
    F_df1 = n-1
    F_df2 = m-1

    t = st.t
    df = n+m-2

    # An interval of not-rejection of variance equality hypothesis
    interval = (F.ppf(var_alpha/2, F_df1, F_df2),
                F.ppf(1-var_alpha/2, F_df1, F_df2))

    different_variances = (F_sampled := (S_y/S_x)**2) <= interval[0] or F_sampled >= interval[1]

    if different_variances:        
        warn(f'Acquired F_test interval is {interval}')
        warn(f'Samle variances ratio is {F_sampled}', category=UserWarning)
        warn(
            f'Variances cannot be assumed to be equal with {1-var_alpha} confidence level', category=UserWarning)

        df = _get_welchs_freedom_degrees(first_sample, second_sample)

    sum_of_variations = (n-1)*S_x**2 + (m-1)*S_y**2
    pooled_std = sqrt(sum_of_variations/(n+m-2))
    return t.ppf(alpha/2, df=df), (first_sample_mean-second_sample_mean) / (sqrt(1/n + 1/m) * pooled_std), t.ppf(1-alpha/2, df=df)


def variance_ratio_confidence_interval(first_sample, second_sample, alpha=0.05):
    """
    A method that returns (1-alpha) confidence interval for the ratio of two variances based on the F random variable.

    first_sample:np.array - the first collection of observations to test on means equality
    second_sample:np.array - the second collection of observations to test on means equality
    alpha:float - the desired confidence level
    """
    first_sample_mean = first_sample.mean()
    second_sample_mean = second_sample.mean()
    S_x = first_sample.std(ddof=1)
    S_y = second_sample.std(ddof=1)
    n = len(first_sample)
    m = len(second_sample)

    F_df1 = n-1
    F_df2 = m-1
    F_ppf = lambda alpha: st.f.ppf(alpha, F_df1, F_df2)

    S_ratio_sqr = (S_x/S_y)**2

    return S_ratio_sqr * F_ppf(alpha/2), S_ratio_sqr * F_ppf(1-alpha/2)


def mean_difference_confidence_interval(first_sample,second_sample, alpha=0.05):
    """
    A method that returns (1-alpha) confidence interval for the difference between two means based on the Student T random variable.
    This method assumes the variances are equal, so be carefull using in the wrong context

    first_sample:np.array - the first collection of observations to test on means equality
    second_sample:np.array - the second collection of observations to test on means equality
    alpha:float - the desired confidence level
    """
    first_sample_mean, second_sample_mean, S_x, S_y, n,m = _define_basic_statistical_properties(first_sample, second_sample)

    df = n+m-2
    t_ppf = lambda alpha: st.t.ppf(alpha, df=df)

    sum_of_variations = (n-1)*S_x**2 + (m-1)*S_y**2
    S_pooled = sqrt(sum_of_variations/(n+m-2))
    sample_mean_difference = first_sample_mean - second_sample_mean

    return t_ppf(alpha/2)*S_pooled*sqrt(1/n+1/m) - sample_mean_difference, t_ppf(1-alpha/2)*S_pooled*sqrt(1/n+1/m) - sample_mean_difference





if __name__ == '__main__':
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        file = open(filename, 'r')

        sample = 0
        sample_one = []
        sample_two = []
        data = [sample_one, sample_two]

        for line in file:
            if '%' in line:
                sample = 1
                continue
            data[sample].append(float(line))

        sample_one = np.array(sample_one)
        sample_two = np.array(sample_two)
    else:
        sample_one = arr([24, 25, 28, 28, 28, 29, 29, 31, 31, 35, 35, 35])
        sample_two = arr([21, 22, 24, 27, 27, 28, 29, 32, 32])

    # print(two_sample_test(sample_one, sample_two, alpha=0.05, var_alpha = 0.1))
    # print(mean_difference_confidence_interval(sample_one, sample_two, alpha=0.01))
    print(get_data_from_file('another_file'))
