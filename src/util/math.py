#a is with b +- range
def is_within(a, b, rng):
  return a >= (b - rng) and a <= (b + rng)