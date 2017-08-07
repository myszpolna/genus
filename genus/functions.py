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
    threads = []
    workers = worker_class.create_workers(input_class, config)
    for worker in workers:
        thread = FactorizeThread(worker)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    return workers


def proteins_analysis(config):
    return data_analysis(genus.ProteineWorker, genus.ProteineData, config)


def rna_analysis(config):
    return data_analysis(genus.RNAWorker, genus.RNAData, config)


def results(data):
    lengths = []
    chords = []
    genuses = []
    names = []
    for el in data:
        # print(el.__dict__)
        if el.length > 0 and el.nr_chord > 0:
            genuses.append(el.genus)
            names.append(el.name)
            lengths.append(el.length)
            chords.append(el.nr_chord)

    return names, lengths, chords, genuses
