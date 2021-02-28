# Usage: chain_ratios.py [num of denominators] -n [numerators to use] -d [denominators to use] 
# If [num of denominators] > len([denominators to use]) or len(numerators to use), last denominator and numerator will be used remaining number of times
# [denominators to use] are space-divided numbers, used to compute chain-ratio
import sys
if sys.argv:
    args = sys.argv.copy()
    args_length = int(args[1])
    
    numerator_start_index = args.index('-n') + 1
    denominator_start_index = args.index('-d') + 1
    numerators = list(map(int, args[numerator_start_index:denominator_start_index-1]))
    denominators = list(map(int, args[denominator_start_index:]))
    num_of_numerators = len(numerators)
    num_of_denominators = len(denominators)

    if num_of_numerators<args_length:
        numerators += [numerators[-1]]*(args_length-num_of_numerators)
    if num_of_denominators<args_length:
        denominators += [denominators[-1]]*(args_length-num_of_denominators)
    
    numerators.reverse()
    denominators.reverse()

    res = numerators[0]/denominators[0]
    for i in range(1, args_length):
        res = numerators[i]/(denominators[i]+res)
    print(res)
        

