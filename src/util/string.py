def string_repeat(a_string, target_length):
  number_of_repeats = target_length // len(a_string) + 1
  a_string_repeated = a_string * number_of_repeats
  return a_string_repeated[:target_length]
