# https://stackoverflow.com/questions/4214936/how-can-i-get-the-values-of-the-locals-of-a-function-after-it-has-been-executed
# author: Niklas R
import sys, types, inspect
def call_function_get_frame(func, *args, **kwargs):
  """
  Calls the function *func* with the specified arguments and keyword
  arguments and snatches its local frame before it actually executes.
  """

  frame = None
  trace = sys.gettrace()
  def snatch_locals(_frame, name, arg):
    nonlocal frame
    if frame is None and name == 'call':
      frame = _frame
      sys.settrace(trace)
    return trace
  sys.settrace(snatch_locals)
  try:
    result = func(*args, **kwargs)
  finally:
    sys.settrace(trace)
  return frame, result

class Proxy: 
  def __iter__(self): return self.step()
  def __next__(self): return next(self.__it__)

def get_module(func):
  frame, result = call_function_get_frame(func)
  try:
    module = Proxy()
    module.__dict__.update(frame.f_locals)
    return module
  finally:
    del frame

def sub_scene(func):
  module = get_module(func)
  if not hasattr(module, "step"): 
    return module
  module.__it__ = iter(module)
  module.step = lambda : next(module.__it__)
  return module

def cluster(func):
  module = get_module(func)
  module.__iter__ = module.__dict__.values().__iter__
  return module

@cluster
def thing():
  eggs = 'spam'
  class Bar:
    def hello(self):
      print("Hello, World!")

def unpack(ns):
    return rf"""
for k,v in {ns}.items():
    exec(f"{{k}} = {{v}}")
"""

def inline(func):
    src = inspect.getsource(func).split('\n')
    for cut,ch in enumerate( src[1] ):
        if ch not in " \t":
            break
    return '\n'.join(ln[cut:] for ln in src[1:])

if __name__ == "__main__":
    assert thing.eggs == 'spam'
    thing.Bar().hello()
