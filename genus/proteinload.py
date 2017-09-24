#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u''' Protein data class definition
    read all data from two columns files in directory

    config:
    -------
    config['data_dir'] : str
    - name for directory with your data or absolute path
    with Your data

    config['end_file'] : str
    - name of type Your data file, with '.'
    (for ex. '.dat')

'''
# Authors: Sebastian Zając  <s.zajac@uksw.edu.pl>
#          Piotr Sułkowski  <psulkows@fuw.edu.pl>
#          Joanna Sułkowska <jsulkows@gmail.com>
#
# License: GPL-3.0

import re
from os import listdir, path
from genus import InputData


class ProteinData(InputData):
    u'''Load proteines from directory with data'''

    def __init__(self, path_dir):
        u''' init Proteine '''
        super().__init__()
        self.path = path_dir
        self.name = self.__take_name_from_path(self.path)

    def read(self):
        ''' read two columns data
             uzupełnić o wartości ujemne i zero !!!
        '''
        data = []
        result = []
        with open(self.path) as file:
            for _, line in enumerate(file):
                if line.strip():
                    line = re.sub('[\t|,-]', ' ', line)
                    tokens = line.split()
                    if len(tokens) == 2:
                        result = [int(x) for x in tokens]
                        data.append(result)
        return data

    @staticmethod
    def __take_name_from_path(path_dir):
        path_split = path_dir.split('/')
        num = len(path_split)
        return path_split[num - 1].split('.')[0]

    @classmethod
    def generate_inputs(cls, config):
        '''read all files in dir with ends'''
        data_dir = config['data_dir']
        end = config['end_file']
        for name in [f for f in listdir(data_dir) if f.endswith(end)]:
            yield cls(path.join(data_dir, name))
