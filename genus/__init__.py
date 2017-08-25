# import abstract classes
from .abstract import InputData
from .abstract import Worker
# import classes for protein analysis
# load protein two columns data
from .proteinload import ProteinData
# methods for clean pprotein like data (two columns)
from .proteinclean import ProteinList
# compute genus for all structure
from .proteingenus import ProteinWorker
# devide and compute genus with one step 
from .proteinanalysis import ProteinAnalysisWorker
# import helpers
from .Threads import FactorizeThread
# only for rna analysis
from .stat import FrequencyList
from .functions import *
#import classes for RNA analysis
from .rnaload import RNAData
from .rnagenus import RNAWorker

