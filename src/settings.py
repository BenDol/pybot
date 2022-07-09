import os
import json

f = open(os.getcwd() + '/settings.json', )
settings = json.load(f)
f.close()
