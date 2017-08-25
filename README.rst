Genus
--------

To use simply do::

    >>> If You have two column data and You want compute genus of all files
    >>> use protein_analysis(config) from functions module.
    >>> config = {'data_dir': str ('data'), 'end_file': str ('.txt')}
    >>> If You want devide structure and find how to genus change with length
    >>> use protein_structure(config)
    >>> For RNA structures - At present take csv files from web and 
    >>> use rna_analysis(config)
    >>> config = {'data_dir': str ('data'), 'end_file': '.csv', 
    >>>           'tab_type': False or list_of_names }
    >>>  list_of_names = ['cWW'] (for example)