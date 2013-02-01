#__outputter__ = {'item': 'grains'}

def item(*args):
    # Dict comprehension introduced in python 2.7
    #ret = {k: __grains__[k] for k in args if k in __grains__}
    ret = {}
    for k in args:
        if k in __grains__:
            ret[k] = __grains__[k]
    return ret
