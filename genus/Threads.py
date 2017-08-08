#!/usr/bin/env python3
# -*- coding: utf-8 -*-
u'''
Class for Thread
'''
# Authors: Sebastian Zając  <s.zajac@uksw.edu.pl>
#          Piotr Sułkowski  <psulkows@fuw.edu.pl>
#          Joanna Sułkowska <jsulkows@gmail.com>
#
# License: GPL-3.0
from threading import Thread


class FactorizeThread(Thread):
    u''' muslti thread for map() function'''
    def __init__(self, worker):
        super().__init__()
        self.worker = worker

    def run(self):
        self.worker = self.worker.map()
