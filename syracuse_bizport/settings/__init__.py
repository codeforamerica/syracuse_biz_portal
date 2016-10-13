import os

ENVIRONMENT = os.environ.get('ENVIRONMENT')

try:
  if 'live' in ENVIRONMENT:
    from .production import *
  elif 'staging' in ENVIRONMENT: 
  	from .staging import * 
  else:
    from .dev import *
except ImportError:
    pass