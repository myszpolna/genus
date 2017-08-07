#!/usr/bin/env python3
# -*- coding: utf-8 -*-

''' Input Data abstract class definition
'''
# Authors: Sebastian Zając  <s.zajac@uksw.edu.pl>
#          Piotr Sułkowski  <psulkows@fuw.edu.pl>
#          Joanna Sułkowska <jsulkows@gmail.com>
#
# License: GPL-3.0


class InputData(object):
    '''Abstract class of Input Data '''

    def read(self):
        ''' abstract of read method'''
        raise NotImplementedError

    @classmethod
    def generate_inputs(cls, config):
        ''' abstract of generate_inputs method'''
        raise NotImplementedError
