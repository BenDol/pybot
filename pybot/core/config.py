import os
import json

def load(file):
  if not file.endswith(".json"):
    file += ".json"
  f = open(os.getcwd() + '/' + file, )
  conf = json.load(f)
  f.close()
  return conf