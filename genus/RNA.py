#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Analyse RNA from directory data.
compute genus for all structure
Parameters:
-----------
name - 4 letters name of structure

length - length of structure :
max - min + 1

cl_data - list of clear data

nr_chord - number of chords in cl_data

info - dict :
    Atribures:
    ---------
    stats_acids : dict - number of four acids
    stats_types : dict - number of all connections type

genus - int : genus of all structure
'''
# Authors: Sebastian Zając  <s.zajac@uksw.edu.pl>
#          Piotr Sułkowski  <psulkows@fuw.edu.pl>
#          Joanna Sułkowska <jsulkows@gmail.com>
#
# License: GPL-3.0

from genus.Worker import Worker
from genus.stat import FrequencyList as fl


class RNAWorker(Worker):
    ''' class for proteine genus analysis'''

    def map(self):
        ''' map work for one protein '''
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
        jeden = []
        for row in tab:
            jeden.append(row[0])
            jeden.append(row[1])
        minimal = min(jeden)
        maximal = max(jeden)
        del jeden
        return maximal - minimal + 1

    def __devide_data(self, tab):
        acids = []
        types = []
        for el in tab:
            acids.append(el[2])
            acids.append(el[3])
            types.append(el[4])
        return acids, types

    def __clear(self, tab):
        ''' clear data  '''
        tab1 = self.__change(tab)
        tab1 = self.__identical_chords(tab1)
        tab1 = self.__double_chords(tab1)
        tab1 = self.__zero_remove(tab1)
        return tab1

    @staticmethod
    def __change(tab):
        ''' change all chords from left to right'''
        result = [[row[1], row[0], row[3], row[2], row[4]] if row[0] > row[
            1] else row for row in tab]
        return result

    @staticmethod
    def __identical_chords(tab):
        ''' remove identical chords '''
        return sorted([list(x) for x in set(tuple(x) for x in tab)])

    @staticmethod
    def __double_chords(tab):
        ''' remove in = out chords'''
        result = [row for row in tab if row[0] != row[1]]
        return result

    @staticmethod
    def __zero_remove(tab):
        '''remove zero from data '''
        check = False
        for el in tab:
            if 0 in el:
                check = True
                break
        if check:
            return [[row[0]+1, row[1]+1, row[2], row[3], row[4]] for row in tab]
        else:
            return tab
