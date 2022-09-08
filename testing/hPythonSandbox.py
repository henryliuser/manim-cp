from inspect import getsource
def inline(func):
    src = inspect.getsource(func).split('\n')
    for cut,ch in enumerate( src[1] ):
        if ch not in " \t":
            break
    return '\n'.join(ln[cut:] for ln in src[1:])

def foo(x):
    x *= 5
    A = [x]
    print(A)
    return [ x * A[0], A ]


def my_func():
    fn = lambda x : x+5*2
    print( inline(fn) )
    # print( inline(foo) )

def unpack(ns):
    return rf"""
for k,v in {ns}.items():
    exec(f"{{k}} = {{v}}")
"""

    
ns = { "asd":5, "x":"'q8weu'", "a":[123,5] }
print( unpack('ns') )
exec( unpack("ns") )
print( locals() )