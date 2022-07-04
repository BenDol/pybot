import screeninfo

from settings import settings as settings

ps_cache = None

def primary_screen():
  global ps_cache
  if ps_cache is not None:
    return ps_cache

  for m in screeninfo.get_monitors():
    if m.is_primary:
      ps_cache = m
      return ps_cache
  return None

def resolution_factor(mon=primary_screen()):
  if is_4k(mon):
    return 1.5
  elif is_2k(mon):
    return 1.3333
  else:
    return 1

def normalized_res(mon=primary_screen()):
  rf = resolution_factor(mon)
  mon.height = mon.height * rf
  mon.width = mon.width * rf
  return mon

def is_2k(mon=primary_screen()):
  if settings['resolution'] == 'native':
    return mon.height > 1080 and mon.height <= 1440
  else:
    return settings['resolution'] == '2k'

def is_4k(mon=primary_screen()):
  if settings['resolution'] == 'native':
    return mon.height > 1440 and mon.height <= 2160
  else:
    return settings['resolution'] == '4k'

def resolution_ordinal(mon=primary_screen()):
  if is_4k(mon):
    return 2
  elif is_2k(mon):
    return 1
  else:
    return 0

def resolution_prefix(mon=primary_screen()):
  if is_4k(mon):
    return '.4k'
  elif is_2k(mon):
    return '.2k'
  else:
    return ''
