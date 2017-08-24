#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u'''
    Protein worker class definition.
    Devide from 5' to 3' and analyse
'''
# Authors: Sebastian Zając  <s.zajac@uksw.edu.pl>
#          Piotr Sułkowski  <psulkows@fuw.edu.pl>
#          Joanna Sułkowska <jsulkows@gmail.com>
#
# License: GPL-3.0

import numpy as np

from genus import Worker
from genus import ProteinList as pl

class ProteinAnalysisWorker(Worker):
    u''' class for devided proteine analysis'''

    def map(self):
        u''' map work for one protein '''
        self.name = self.input_data.name
        self.cl_data = pl(self.input_data.read()).clean()
        self.mini, self.maxi, \
        self.length, self.nr_chord = self.cl_data.compute_info()
        self.no_biff = pl(self.remove_biff(self.cl_data)).change()
        self.b1_b2_list = self.__multiplicity(
            self.cl_data, self.mini, self.maxi)
        self.genuses = self.devide_and_compute(
            self.mini, self.maxi, self.no_biff)


    @staticmethod
    def __multiplicity(tab, minimum, maximum):
        u'''compute biffurcation numbers'''
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
        u'''Devide data and compute genus for all data with lag 1'''
        b1_b2_sum = 0
        counter = 0
        genuses = []
        data = []
        length_data = 0
        for element in range(mini, maxi + 1):
            b1_b2_sum += self.b1_b2_list[counter]
            counter += 1
            data = [x for x in tab if x[1] <= b1_b2_sum and x[0] <= b1_b2_sum]
            if data != []:
                if len(data) != length_data:
                    length_data = len(data)
                    data = self.przelicznik(data)
                    genuses.append(self.genus_one_backbone(data))
                else:
                    genuses.append(genuses[(len(genuses)-1)])
            else:
                genuses.append(0)
        return genuses
