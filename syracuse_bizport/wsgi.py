from .wsgi import *
from whitenoise.django import DjangoWhiteNoise

application = DjangoWhiteNoise(application)
