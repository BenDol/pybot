from os import walk

def list_dir(path):
	return next(walk(path), (None, None, []))[2]