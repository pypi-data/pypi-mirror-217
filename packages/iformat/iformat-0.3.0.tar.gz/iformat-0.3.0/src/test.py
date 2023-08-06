import iformat
from re import match
class A:
    def b():
        pass
    def c():
        pass
    d = ...
    e = ...

a = A()
#print(", ".join([f"{k}: {v}" for k, v in A.__dict__.items() if not match(r"__doc__", k)]))
iformat.iprint(A)