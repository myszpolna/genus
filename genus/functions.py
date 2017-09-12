#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Helpers functions '''
# Authors: Sebastian Zając  <s.zajac@uksw.edu.pl>
#          Piotr Sułkowski  <psulkows@fuw.edu.pl>
#          Joanna Sułkowska <jsulkows@gmail.com>
#
# License: GPL-3.0

import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

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
    return data_analysis(genus.ProteinAnalysisWorker,
                         genus.ProteinData, config)


def protein_analysis(config):
    '''run proteins analysis from directory'''
    return data_analysis(genus.ProteinWorker,
                         genus.ProteinData, config)


def rna_analysis(config):
    '''run RNA analysis from directory'''
    return data_analysis(genus.RNAWorker,
                         genus.RNAData, config)


def results(data):
    '''helper to get info for plots'''
    lengths = []
    chords = []
    genuses = []
    names = []
    for _, element in enumerate(data):
        if element.length > 0 and element.nr_chord > 0:
            genuses.append(element.genus)
            names.append(element.name)
            lengths.append(element.length)
            chords.append(element.nr_chord)
            plt.plot(element.length,element.genus,'bo')
    plt.xlabel('Length')
    plt.ylabel('Genus')
    plt.title('Genus of all structure')
    plt.grid(True)
    plt.savefig( "result.png")
    plt.clf()
    tab = np.array(chords)/np.array(lengths)
    for i, _ in enumerate(tab):
        plt.plot(tab[i],genuses[i],'go')
    plt.xlabel('density_nch/length')
    plt.ylabel('Genus')
    plt.title('Genus')
    plt.grid(True)
    plt.savefig( "result2.png")
    plt.clf()
    return names, np.array(lengths), np.array(chords), genuses


def results_structure(data):
    '''helper to get info for plots'''
    lengths = []
    chords = []
    genuses = []
    names = []
    for element in data:
        if element.length > 0 and element.nr_chord > 0:
            genuses.append(element.genuses)
            names.append(element.name)
            lengths.append(element.length)
            chords.append(element.nr_chord)
            x = range(1,element.length+1)
            plt.plot(x, element.genuses)
            plt.xlabel('Position in sequence')
            plt.ylabel('Genus')
            plt.title('Genus - ' + element.name)
            plt.grid(True)
            plt.savefig(element.name + ".png")
            # plt.show()
            plt.clf()
            df1 = pd.DataFrame.from_items([('position', x)])
            df1['genus'] = element.genuses
            df1.to_csv(element.name+".csv", sep='\t', encoding='utf-8', index = False)

    return names, lengths, chords, genuses

