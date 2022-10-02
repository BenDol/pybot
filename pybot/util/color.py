import pybot.util.number as number

# is rgb_a a match of rgb_b with a tolerance (tol) setting
def is_match(rgb_a, rgb_b, tol):
  return number.is_within(rgb_a[0], rgb_b[0], tol) and \
         number.is_within(rgb_a[1], rgb_b[1], tol) and \
         number.is_within(rgb_a[2], rgb_b[2], tol)
