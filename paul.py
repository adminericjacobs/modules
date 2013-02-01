import os

def uname():
    ret = os.uname()
    return ret

def yell(**kargs):
    #ret = [arg.upper() for arg in args]
    #ret = ' '.join(args).upper()
    #return ' '.join(args).upper()
    return kargs


