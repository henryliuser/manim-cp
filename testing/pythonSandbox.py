class X:
    def __init__(self):
        self.a = 5
        self.b = "asd"
        self.c = 2.3598723

    def foo(self, x):
        print(x)

x = X()
print( callable(x.foo) )