# https://stackoverflow.com/questions/4214936/how-can-i-get-the-values-of-the-locals-of-a-function-after-it-has-been-executed
# author: Niklas R
import sys, types

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

def namespace(func):
  frame, result = call_function_get_frame(func)
  try:
    module = types.ModuleType(func.__name__)
    module.__dict__.update(frame.f_locals)
    module.__iter__ = module.__dict__.values().__iter__
    return module
  finally:
    del frame

@namespace
def thing():
  eggs = 'spam'
  class Bar:
    def hello(self):
      print("Hello, World!")

if __name__ == "__main__":
    assert thing.eggs == 'spam'
    thing.Bar().hello()