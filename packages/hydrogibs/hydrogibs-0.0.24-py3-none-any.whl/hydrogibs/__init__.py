from .floods import GR4, QDF, SoCoSe
from .floods.RationalMethod import rational_method
from .misc.misc import Ressaut, crupedix
import os

with open('hydrogibs/test.csv') as file:
    contents = file.read()
