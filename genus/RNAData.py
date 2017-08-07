#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' RNA data class definition
    read all data from two columns files in directory

    !!! Data should by like in csv file from
    http://rna.bgsu.edu/rna3dhub

    config:
    -------
    config['data_dir'] : str
    - name for directory with your data or absolute path
    with Your data

    config['end_file'] : str
    - name of type Your data file, with '.'
    (for ex. '.csv')

    config['tab_types'] : False or list
    False - if You want all type connections
    ############# REMEMBER #####################
    cHW = cWH, tHW = tWH, cSW = cWS, tSW = tWS,
    cSH = cHS, tSH = tHS
    ############################################
    You can also write Your own list for ex.
    ['cWW'] - giwe You analise only cWW connections

'''
# Authors: Sebastian Zając  <s.zajac@uksw.edu.pl>
#          Piotr Sułkowski  <psulkows@fuw.edu.pl>
#          Joanna Sułkowska <jsulkows@gmail.com>
#
# License: GPL-3.0

import re
from os import listdir, path

from genus.Data import InputData

TAB_TYPES = ["cWW", "tWW", "cWH", "cHW", "tWH",
             "tHW", "cWS", "cSW", "tWS", "tSW",
             "cHH", "tHH", "cHS", "cSH", "tHS",
             "tSH", 'cSS', 'tSS']

DOUBLE_NAMES = ['cHW', 'tHW', 'cSW', 'tSW', 'cSH', 'tSH']


class RNAData(InputData):
    '''Load RNA data '''

    def __init__(self, path_dir, tab_types=TAB_TYPES
                 ):
        super().__init__()
        self.path = path_dir
        self.name = self.path[-8:-4]
        self.info = {'tab_types': tab_types,
                     'backbond': '',
                     'stats_acids': {},
                     'stats_types': {}}
        self.errors = {'lines': [],
                       'backbonds': [],
                       'types': []}

    @staticmethod
    def __check_backbond(back, in_back, out_back):
        if in_back == back:
            if out_back == in_back:
                return True
            else:
                return False
        else:
            return False

    def __check_line_b(self, line):
        '''Check backbond is ok'''
        # set backbond from first element
        if not self.info['backbond']:
            self.info['backbond'] = line[3]
        # check is one and first backbon
        if not self.__check_backbond(self.info['backbond'], line[3], line[13]):
            return False
        return True

    @staticmethod
    def __change_letters(string):
        first, second, third = string[0], string[1], string[2]
        return str(first) + str(third) + str(second)

    def read(self):
        dane = []
        with open(self.path) as f:
            for nr, chord_line in enumerate(f):
                chord_line = chord_line.strip()
                if chord_line:
                    data_line = re.split('\||"|,', chord_line)
                    if len(data_line) < 16:
                        self.errors['lines'].append([nr, data_line])
                    else:
                        self.name = data_line[1]
                        if not self.__check_line_b(data_line):
                            self.errors['backbonds'].append([nr, data_line])
                        else:
                            if len(data_line[8]) == 4:
                                if data_line[8][0] == 'n':
                                    nnt = data_line[8][-3:]
                            else:
                                nnt = data_line[8]
                            if nnt in self.info['tab_types']:
                                if nnt in DOUBLE_NAMES:
                                    nnt = self.__change_letters(nnt)
                                if int(data_line[5]) > 0 and int(data_line[15]) > 0:
                                    dane.append([int(data_line[5]),
                                                 int(data_line[15]),
                                                 data_line[4],
                                                 data_line[14],
                                                 nnt])
                            else:
                                self.errors['types'].append([nr, data_line])
        return dane

    @classmethod
    def generate_inputs(cls, config):
        '''read all files in dir with ends'''
        data_dir = config['data_dir']
        end = config['end_file']
        if config['tab_types']:
            for name in [f for f in listdir(data_dir) if f.endswith(end)]:
                yield cls(path.join(data_dir, name),
                          tab_types=config['tab_types'])
        else:
            for name in [f for f in listdir(data_dir) if f.endswith(end)]:
                yield cls(path.join(data_dir, name))
