#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Helpers functions '''
# Authors: Sebastian Zając  <s.zajac@uksw.edu.pl>
#          Piotr Sułkowski  <psulkows@fuw.edu.pl>
#          Joanna Sułkowska <jsulkows@gmail.com>
#
# License: GPL-3.0

import genus

from genus.Threads import FactorizeThread


def data_analysis(worker_class, input_class, config):
    '''helper for Thread with map() method'''
    threads = []
    workers = worker_class.create_workers(input_class, config)
    for worker in workers:
        thread = FactorizeThread(worker)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    return workers

def protein_structure(config):
    '''run proteins deviding and analysis'''
    return data_analysis(genus.ProteinAnalysisWorker, genus.ProteinData, config)

def proteins_analysis(config):
    '''run proteins analysis from directory'''
    return data_analysis(genus.ProteinWorker, genus.ProteinData, config)


def rna_analysis(config):
    '''run RNA analysis from directory'''
    return data_analysis(genus.RNAWorker, genus.RNAData, config)


def results(data):
    'helper to get info for plots'
    lengths = []
    chords = []
    genuses = []
    names = []
    for element in data:
        if element.length > 0 and element.nr_chord > 0:
            genuses.append(element.genus)
            names.append(element.name)
            lengths.append(element.length)
            chords.append(element.nr_chord)

    return names, lengths, chords, genuses
