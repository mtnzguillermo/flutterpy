
import numpy as np
from ._notation_list import notation_list

class Notation():

    def __init__(self, name, relations):

        self.name = name
        self.relations = relations

notations = []
for notation in notation_list:
    Notation(notation['name'],notation['relations'])
