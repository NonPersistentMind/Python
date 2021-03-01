import pyperclip

# ============================ Formatters Definitions ============================
def format_comment(comment:str, size:int=80, symbol:str='=', copy:bool=True):
    """
    Adds 'symbols' symmetrically to make 'comment' 'size'-length
    size : int          => resulting number of characters in string
    symbol : char  => symbol to add in case given len(string) is less than size
    copy : bool       => automatically copy the result to clipboard
    """
    symbols_to_add = size -2 - len(comment)
    if symbols_to_add < 0:
        return comment
    left_symbols = (symbols_to_add//2)
    right_symbols = symbols_to_add - left_symbols

    empty_comment = comment==''
    res = '# ' + symbol*left_symbols + ((not empty_comment)*' ') + comment + ((not empty_comment)*' ') + symbol*right_symbols

    pyperclip.copy(res)
    return res


def format_definition(name, func_args, types = "function", copy=True, indentation_char = '    '):
    types_arr = types.split(' ')
    res = ''
    if 'function' in types_arr:
        res += 'def %s(' % name
        if 'class' in types_arr:
            res+= 'self'
            types_arr.remove('class')
        for arg in func_args:
            res += ', ' + arg
        res += '):'
        types_arr.remove('function')
    
    format_dict = formater(indentation_char)()  # Get a formater dictionary that knows all types of functions that have patterns
    default_formater = format_dict['default']   # Ask for a default pattern (basically just returns result back)

    res = format_dict.get(name, default_formater)(
        res, func_args
    )

    pyperclip.copy(res)
    return res

def formater(indentation_char='    '):
    # ======================= Formatter function declarations ========================
    def init_formater(res, func_args, indentation_char = indentation_char):
        res += '\n' 
        for arg in func_args:
            res+= indentation_char
            res+='self.%s' % arg
            res+= ' = %s' % arg
            res+='\n'
        return res

    # ======================= Formatter dictionary declaration =======================
    format_dict = {}
    format_dict['default'] = lambda res, *x: res

    format_dict['__init__']  = init_formater
    
    return ( lambda: format_dict )

# ==============================================================================

def commas(N):
    """
    Formats any number (even floating-point) to the form of 'xxx,yyy,zzz' discarding the floating part if present
    """
    digits = str(int(N))
    res = ''
    while digits:
        digits, last3 = digits[:-3], digits[-3:]
        res = (last3 + ',' + res) if res else last3
    return res

def money(N, numwidth=0, currency='$', accuracy=2):
    """
    Formats any number to the form of '$ -xxx,yyy,zzz' with:

    numwidth : int     => the size of a resulting field, including currency size 
                                      (adds spaces if numwidth is bigger than number:  money(123, numwidth=5) => '  123')    
    currency : char     => sign at the beginning (currency='' for no sign, currency='GBP' => 'GBP -xxx,yyy,zzz')
    accuracy : int        => decimal places for floating part
    """
    sign = '-' if N<0 else ''
    N = abs(N)
    int_part = commas(int(N))                                                         # Create comma-separated integer part of N 
    form_str = '%.*f'                                                                         # being used via  'form_str % (num, acc)'  formats 'num' to 'acc'-decimal places
    floating_part = (form_str % (accuracy,N))[-accuracy:]               # for accuracy = 4 : takes 4 last digits from 4-decimal places string representation of N
    number = '%s%s.%s' % (sign, int_part, floating_part)
    if currency: 
        currency+=' '
    
    actual_numwidth = numwidth - len(currency)
    return '%s%*s' % (currency, actual_numwidth, number)


# ================================= Testing Mode =================================

if __name__ == "__main__":
    import sys
    import math

    def selftest():
        tests = -1, 1.23
        tests += 12, 123, 1234, 12345, 123456, 1234567
        tests+= 2**32, 2**100
        for res in map(commas, tests):
            print(res)

        print()
        print()
        tests = 0, 1, -1, 1.23, 1., 1.2, math.pi
        tests += 12.34, 12.344, 12.345, 12.346
        tests+= 2**32, (2**32 + .2345)
        tests+= 1.2345, 1.2, 0.2345
        tests+= -1.2345, -1.2, -0.2345
        tests+= -(2**32), -(2**32 + .2345)
        tests+= 2**100, -(2**100)
        for res in map(money, tests):
            print(res)

    if len(sys.argv)==1:
        selftest()
    else:
        if sys.argv[1] == 'money':
            # ===================== Order: N, numwidth, currency, accuracy =====================        
            funcs = [float, int, lambda x: x, int]          
            args = sys.argv[2:]     
            # ================= Converts arguments as long as they are given ===============
            params = zip(funcs, args)       
            new_args = []
            for param in params:
                arg = param[0](param[1])
                new_args.append(arg)
            # ===================================================================
            print(money(*new_args))

        # =================== Formats comment if nothing else specified ====================
        else:
            print(format_comment(sys.argv[1]))


        
