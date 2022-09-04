from inspect import getsource
def inline(func):
    src = getsource(func).split('\n')
    return '\n'.join(ln[4:] for ln in src[1:])


def foo(x):
    x *= 5
    A = [x]
    print(A)
    return [ x * A[0], A ]


def my_func():
    fn = lambda x : x+5*2
    print( inline(fn) )
    # print( inline(foo) )

my_func()