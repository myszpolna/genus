#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u'''
    Class for list frequency
'''
class FrequencyList(list):
    u'''class for compute stats with anions and types'''
    def __init__(self, members):
        super().__init__(members)

    def frequency(self):
        u'''counts different elements in list'''
        counts = {}
        for item in self:
            counts.setdefault(item, 0)
            counts[item] += 1
        return counts
