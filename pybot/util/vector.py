# system
import random

def random_point(top_left, bottom_right):
  x = random.randint(top_left[0], bottom_right[0])
  y = random.randint(top_left[1], bottom_right[1])
  return x, y