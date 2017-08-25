#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u'''
    RNA worker class definition.
    Devide from 5' to 3' and analyse
    with different types
'''
# Authors: Sebastian Zając  <s.zajac@uksw.edu.pl>
#          Piotr Sułkowski  <psulkows@fuw.edu.pl>
#          Joanna Sułkowska <jsulkows@gmail.com>
#
# License: GPL-3.0

import numpy as np

from genus.Worker import Worker


class RNAAnalysisWorker(Worker):
    u''' class for devided RNA analysis'''

    def map(self):
        u''' map work for one protein '''
        self.name = self.input_data.name
        self.cl_data = self.__clear(self.input_data.read())
        self.mini, self.maxi, self.length, self.nr_chord = self.__compute_info(
            self.cl_data)
        self.no_biff = self.__change(self.remove_biff(self.cl_data))
        self.b1_b2_list = self.__multiplicity(
            self.cl_data, self.mini, self.maxi)
        self.genuses = self.devide_and_compute(
            self.mini, self.maxi, self.no_biff)

    def __clear(self, tab):
        u''' clear data  '''
        tab1 = self.__change(tab)
        tab1 = self.__identical_chords(tab1)
        tab1 = self.__double_chords(tab1)
        tab1 = self.__zero_remove(tab1)
        return tab1

    @staticmethod
    def __compute_info(tab):
        new_tab = np.array(tab)
        chords = len(tab)
        maxi = new_tab.max()
        mini = new_tab.min()
        length = maxi - mini + 1
        return mini, maxi, length, chords

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

    @staticmethod
    def __multiplicity(tab, minimum, maximum):
        u'''compute biffurcation numbers'''
        ####
        # Tutaj moge dodac tworzenie tabeli od min do max
        # co jeden  - zamienic range(len(tab)) na enumerate
        # wtedy w nastepnej funkcji jade po elementach tej
        # tablicy i od razu mam licznik - potrzebny do odzyskiwania
        # wartosci genusu oraz poprzedniej dlugosci
        # jesli dlugosc danych się nie zmienia to nie liczę genusu tylko
        # kopiuje poprzednią wartość z wyników
        ####
        b1_b2_list = []
        for i in range(minimum, maximum + 1):
            b1 = 0
            b2 = 0
            for j in range(len(tab)):
                if tab[j][0] == i or tab[j][1] == i:
                    if tab[j][1] < i:
                        b1 += 1
                    elif tab[j][0] < i:
                        b1 += 1
                    else:
                        b2 += 1
            b1_b2_list.append(b1 + b2)
        return b1_b2_list

    def devide_and_compute(self, mini, maxi, tab):
        '''
            To tez trzeba zmienic i uzgodnić
        '''
        b1_b2_sum = 0
        counter = 0
        genuses = []
        data = []
        # test_length = 0
        for element in range(mini, maxi + 1):
            b1_b2_sum += self.b1_b2_list[counter]
            counter += 1
            data = [x for x in tab if x[1] <= b1_b2_sum and x[0] <= b1_b2_sum]
            if data != []:
                data = self.przelicznik(data)
                genuses.append(self.genus_one_backbone(data))
            else:
                genuses.append(0)
        return genuses
