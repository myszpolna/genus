#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u'''
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

    info: dict :
        Atribures:
        ---------
        stats_acids : dict - number of four acids
        stats_types : dict - number of all connections type

    genus: int - genus of all structure
'''
# Authors: Sebastian Zając  <s.zajac@uksw.edu.pl>
#          Piotr Sułkowski  <psulkows@fuw.edu.pl>
#          Joanna Sułkowska <jsulkows@gmail.com>
#
# License: GPL-3.0

import numpy as np

from genus.Worker import Worker


class ProteinWorker(Worker):
    u''' class for proteine genus analysis'''

    def map(self):
        u''' map work for one protein '''
        self.name = self.input_data.name
        data = self.input_data.read()
        self.length = self.compute_length(data)
        self.cl_data = self.__clear(data)
        self.nr_chord = len(self.cl_data)
        self.genus = self.compute_genus()

    def __clear(self, tab):
        u''' clear data  '''
        tab1 = self.__change(tab)
        tab1 = self.__identical_chords(tab1)
        tab1 = self.__double_chords(tab1)
        tab1 = self.__zero_remove(tab1)
        return tab1

    @staticmethod
    def compute_length(tab):
        new_tab = np.array(tab)
        return new_tab.max() - new_tab.min() + 1

    @staticmethod
    def __change(tab):
        u''' change all chords from left to right'''
        result = [[row[1], row[0]] if row[0] > row[
            1] else [row[0], row[1]] for row in tab]
        return result

    @staticmethod
    def __identical_chords(tab):
        u''' remove identical chords '''
        result = [list(x) for x in set(tuple(x) for x in tab)]
        return sorted(result)

    @staticmethod
    def __double_chords(tab):
        u''' remove in = out chords'''
        result = [row for row in tab if row[0] != row[1]]
        return result

    @staticmethod
    def __zero_remove(tab):
        u'''remove zero from data '''
        result = np.array(tab)
        if 0 in result:
            result = result + 1
        return result.tolist()
