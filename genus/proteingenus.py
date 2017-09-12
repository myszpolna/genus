#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    Protein worker class definition.
    Load data, clean and compute genus
    for all structure.
    Parameters:
    -----------
    name: str - name of protein structure

    length: int - length of structure :
        max_node - min_node + 1

    cl_data: list - list of clear data

    nr_chord: int - number of chords in cl_data

    genus: int - genus of all structure
'''
# Authors: Sebastian Zając  <s.zajac@uksw.edu.pl>
#          Piotr Sułkowski  <psulkows@fuw.edu.pl>
#          Joanna Sułkowska <jsulkows@gmail.com>
#
# License: GPL-3.0

import numpy as np

from genus import Worker
from genus import ProteinList as pl


class ProteinWorker(Worker):
    ''' class for proteine genus analysis'''

    def map(self):
        ''' map work for one protein '''
        self.name = self.input_data.name
        self.cl_data = pl(self.input_data.read()).clean()
        self.mini, self.maxi,\
        self.length, self.nr_chord = self.cl_data.compute_info()
        self.genus = self.compute_genus()
