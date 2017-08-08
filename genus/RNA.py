#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u'''
    RNA worker class definition.
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

from genus.Worker import Worker
from genus.stat import FrequencyList as fl


class RNAWorker(Worker):
    u''' class for proteine genus analysis'''

    def map(self):
        u''' map work for one protein '''
        self.name = self.input_data.name
        data = self.input_data.read()
        if len(data) > 1:
            self.length = self.compute_length(data)
            self.cl_data = self.__clear(data)
            self.nr_chord = len(self.cl_data)
        else:
            return self
        if self.nr_chord != 0:
            acids, types = self.__devide_data(self.cl_data)
            self.info['stats_acids'] = fl(acids).frequency()
            self.info['stats_types'] = fl(types).frequency()
            self.genus = self.compute_genus()

    @staticmethod
    def compute_length(tab):
        u'''length compute static method'''
        jeden = []
        for row in tab:
            jeden.append(row[0])
            jeden.append(row[1])
        minimal = min(jeden)
        maximal = max(jeden)
        del jeden
        return maximal - minimal + 1

    @staticmethod
    def __devide_data(tab):
        u'''devide data for info'''
        acids = []
        types = []
        for element in tab:
            acids.append(element[2])
            acids.append(element[3])
            types.append(element[4])
        return acids, types

    def __clear(self, tab):
        u''' clear data  '''
        tab1 = self.__change(tab)
        tab1 = self.__identical_chords(tab1)
        tab1 = self.__double_chords(tab1)
        tab1 = self.__zero_remove(tab1)
        return tab1

    @staticmethod
    def __change(tab):
        u''' change all chords from left to right'''
        result = [[row[1], row[0], row[3], row[2], row[4]] if row[0] > row[
            1] else row for row in tab]
        return result

    @staticmethod
    def __identical_chords(tab):
        u''' remove identical chords '''
        return sorted([list(x) for x in set(tuple(x) for x in tab)])

    @staticmethod
    def __double_chords(tab):
        u''' remove in = out chords'''
        result = [row for row in tab if row[0] != row[1]]
        return result

    @staticmethod
    def __zero_remove(tab):
        u'''remove zero from data '''
        check = False
        for row in tab:
            if 0 in row:
                check = True
                break
        if check:
            return [[row[0]+1, row[1]+1, row[2], row[3], row[4]] for row in tab]
        else:
            return tab
