#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
    Class for clean protein list methods 
'''

import numpy as np


class ProteinList(list):

    def __init__(self, members):
        super().__init__(members)

    def numpy_array(self):
        return np.array(self)

    def compute_info(self):
        array = self.numpy_array()
        chords = len(array)
        maxi = array.max()
        mini = array.min()
        length = maxi - mini + 1
        return mini, maxi, length, chords

    def change(self):
        result = [[row[1], row[0]] if row[0] > row[
            1] else [row[0], row[1]] for row in self]
        return ProteinList(result)

    def rem_same_chords(self):
        result = [list(x) for x in set(tuple(x) for x in self)]
        return ProteinList(sorted(result))

    def rem_inout(self):
        return ProteinList([row for row in self if row[0] != row[1]])

    def zero_rem(self):
        result = self.numpy_array()
        if 0 in result:
            result = result + 1
        return ProteinList(result.tolist())

    def clean(self):
        return ProteinList(self.change().rem_same_chords().rem_inout().zero_rem())
