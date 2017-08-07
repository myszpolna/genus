#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
This short module load all .dat files in list
'''
# Authors: Sebastian Zając  <s.zajac@uksw.edu.pl>
#          Piotr Sułkowski  <psulkows@fuw.edu.pl>
#          Joanna Sułkowska <jsulkows@gmail.com>
#
# License: GPL-3.0
import numpy as np

from genus.Worker import Worker


class ProteinWorker(Worker):
    ''' class for proteine genus analysis'''

    def map(self):
        ''' map work for one protein '''
        self.name = self.input_data.name
        data = self.input_data.read()
        self.length = self.compute_length(data)
        self.cl_data = self.__clear(data)
        self.nr_chord = len(self.cl_data)
        self.genus = self.compute_genus()

    def __clear(self, tab):
        ''' clear data  '''
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
        ''' change all chords from left to right'''
        result = [[row[1], row[0]] if row[0] > row[
            1] else [row[0], row[1]] for row in tab]
        return result

    @staticmethod
    def __identical_chords(tab):
        ''' remove identical chords '''
        result = [list(x) for x in set(tuple(x) for x in tab)]
        return sorted(result)

    @staticmethod
    def __double_chords(tab):
        ''' remove in = out chords'''
        result = [row for row in tab if row[0] != row[1]]
        return result

    @staticmethod
    def __zero_remove(tab):
        '''remove zero from data '''
        result = np.array(tab)
        if 0 in result:
            result = result + 1
        return result.tolist()
