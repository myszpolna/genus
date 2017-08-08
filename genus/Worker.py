#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    Worker abstract class definition
'''
# Authors: Sebastian Zając  <s.zajac@uksw.edu.pl>
#          Piotr Sułkowski  <psulkows@fuw.edu.pl>
#          Joanna Sułkowska <jsulkows@gmail.com>
#
# License: GPL-3.0

from itertools import chain


class Worker(object):
    ''' Worker abstract class '''

    def __init__(self, input_data):
        self.input_data = input_data
        self.length = 0
        self.cl_data = []
        self.info = {}

    def map(self):
        ''' abstract map method'''
        raise NotImplementedError

    @classmethod
    def create_workers(cls, input_class, config):
        ''' workers creator'''
        workers = []
        for input_data in input_class.generate_inputs(config):
            workers.append(cls(input_data))
        return workers

    @staticmethod
    def __przelicznik(tab):
        ''' remove empty spots'''
        jeden = list(chain.from_iterable((row[0], row[1]) for row in tab))
        for i in range(1, max(jeden)):
            if i not in jeden and i < max(jeden):
                while i not in jeden:
                    for index, item in enumerate(jeden):
                        if item > i:
                            jeden[index] -= 1

        result = [[jeden[i], jeden[i + 1]] for i in range(0, len(jeden), 2)]
        return result

    @staticmethod
    def __bifurcations_part(tab, b_par, bif):
        ''' part of biff function '''
        while True:
            log = False
            for k in range(b_par - 1):
                if tab[bif[k]][1] < tab[bif[k + 1]][1]:
                    log = True
                    tab[bif[k]][1], tab[
                        bif[k + 1]][1] = tab[bif[k + 1]][1], tab[bif[k]][1]
            if not log:
                break
        return tab

    def __resolve_bifurcations(self, tab, n_chords):
        ''' Methods for resolve biffurcations in structure '''
        for i in range(1, 2 * n_chords):
            bif1 = []
            bif2 = []
            for j in range(n_chords):
                if tab[j][0] == i or tab[j][1] == i:
                    if tab[j][1] < i:
                        bif1.append(j)
                    elif tab[j][0] < i:
                        bif1.append(j)
                        tab[j][1] = tab[j][0]
                        tab[j][0] = i
                    else:
                        bif2.append(j)
            b1_len, b2_len = len(bif1), len(bif2)
            if b1_len > 1:
                tab = self.__bifurcations_part(tab, b1_len, bif1)
            if b2_len > 1:
                tab = self.__bifurcations_part(tab, b2_len, bif2)
            if b1_len + b2_len > 1:
                for row2 in tab:
                    if row2[0] > i:
                        row2[0] += b1_len + b2_len - 1
                    if row2[1] > i:
                        row2[1] += b1_len + b2_len - 1
            for k in range(1, b1_len):
                tab[bif1[k]][0] += k
            for l_n in range(b2_len):
                tab[bif2[l_n]][0] += b1_len + l_n
        return tab

    @staticmethod
    def __genus_one_backbone(tab):
        '''compute genus from clean data '''
        n_chords = len(tab)
        n_spots = 4 * n_chords
        remaining_chain = [1] * n_spots
        remaining_spots = n_spots
        edge = 0  # to chcemy policzyć - ilość brzegów
        while remaining_spots > 0:
            edge += 1
            nr_j = 0
            nr_k = 1
            while remaining_chain[nr_j] == 0:
                nr_j += 1
                if nr_j % 2 == 0:
                    nr_k += 1  # number of the atom
            side = nr_j % 2
            # print "Number: %i, Atom: %i, Side: %i " % (j, k, side)
            k_boundrary = nr_k
            side_boundrary = side
            remaining_chain[(k_boundrary - 1) * 2 + side_boundrary] = 0

            while True:
                i = 0
                while tab[i][0] != k_boundrary and tab[i][1] != k_boundrary:
                    i += 1
                if tab[i][0] == k_boundrary:
                    k_boundrary = tab[i][1]
                else:
                    k_boundrary = tab[i][0]
                side_boundrary = (1 + side_boundrary) % 2
                remaining_chain[(k_boundrary - 1) * 2 + side_boundrary] = 0
                if side_boundrary == 0:
                    k_boundrary = k_boundrary - 1
                else:
                    k_boundrary = k_boundrary + 1
                if k_boundrary == 0:
                    k_boundrary = 2 * n_chords
                if k_boundrary == 2 * n_chords + 1:
                    k_boundrary = 1
                side_boundrary = (1 + side_boundrary) % 2
                remaining_chain[(k_boundrary - 1) * 2 + side_boundrary] = 0
                remaining_spots = remaining_spots - 2

                if 2 * (k_boundrary - 1) + side_boundrary == 2 * (nr_k - 1) + side:
                    break

        genus = (2 + n_chords - 1 - edge) / 2
        # print "Number of boundaries: %i, genus: %i" % (r,genus)
        return int(genus)

    def compute_genus(self):
        ''' methods for genus compute from self.data
            You can use them only if You load data to self.data
            Returns
            -------
            genus_ : int
                genus value for data

            nobiff_data_ : list with [in,out]
                data without biffurcations
        '''
        if self.cl_data:
            self.nobiff_data_ = self.__resolve_bifurcations(
                self.__przelicznik(self.cl_data), self.nr_chord)
            return self.__genus_one_backbone(self.nobiff_data_)
