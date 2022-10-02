# Get the classes simple name
def class_simple_name(c):
  s = c.__name__.split('.')
  return s[len(s)-1]
