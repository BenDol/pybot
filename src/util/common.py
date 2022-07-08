import imp
import sys

def print(msg, *args, clearLine=False):
  end = clearLine and '\r' or '\n'
  print(msg, *args, end=end, flush=True)
  if clearLine:
    sys.stdout.write("\033[K")

def dynamic_import(name, class_name=None):
    # find_module() method is used to find the module 
    # and return its description and path.
    try:
      fp, path, desc = imp.find_module(name)  
    except ImportError:
      print ("module not found: " + name)
          
    try:
    # load_modules loads the module 
    # dynamically ans takes the filepath
    # module and description as parameter
      example_package = imp.load_module(name, fp, path, desc) 
    except Exception as e:
        print(e)

    myclass = None
    if class_name:
      try:
          myclass = imp.load_module("% s.% s" % (name, class_name), 
                                    fp, path, desc)
      except Exception as e:
        print(e)

    return example_package, myclass