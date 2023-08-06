# -*- coding: utf-8 -*-

# Automatically generated from /home/mh/code/fdi/fdi/dataset/resources/UnstructuredDataset_DataModel.yml. Do not edit.

from collections import OrderedDict
from builtins import str


import copy

import logging
# create logger
logger = logging.getLogger(__name__)


# Data Model specification for mandatory components
_Model_Spec = {
    'name': 'UnstructuredDataset_DataModel',
    'description': 'UnstructuredDataset class data model mandatory configuration',
    'parents': [
        None,
        ],
    'schema': '1.6',
    'metadata': {
        'description': {
                'data_type': 'string',
                'description': 'Description of this dataset',
                'default': 'UNKNOWN',
                'valid': '',
                },
        'type': {
                'data_type': 'string',
                'description': 'Class name.',
                'default': 'UnstructuredDataset',
                'valid': '',
                'typecode': 'B',
                },
        'doctype': {
                'data_type': 'string',
                'description': "Data/doc Type identification. 'json', 'xml'. or nul.",
                'default': None,
                'valid': '',
                'typecode': 'B',
                },
        'version': {
                'data_type': 'string',
                'description': 'Version of dataset',
                'default': '0.1',
                'valid': '',
                },
        'FORMATV': {
                'data_type': 'string',
                'description': 'Version of dataset schema and revision',
                'default': '1.6.0.1',
                'valid': '',
                },
        },
    'datasets': {
        },
    }

Model = copy.deepcopy(_Model_Spec)
