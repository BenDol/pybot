def map_dump(m, replace_key=None, replace_value=None):
  for key, value in sorted(m.items(), key=lambda x: x[0]):
    k = replace_key if replace_key is not None else key
    v = replace_value if replace_value is not None else value
    print("{} : {}".format(k, v))