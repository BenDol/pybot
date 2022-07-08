import util.math as math

# is rgba a match of rgbb with a tolerance (tol) setting
def is_match(rgba, rgbb, tol):
  return math.is_within(rgba[0], rgbb[0], tol) and math.is_within(rgba[1], rgbb[1], tol) and math.is_within(rgba[2], rgbb[2], tol)