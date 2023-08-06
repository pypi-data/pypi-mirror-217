# -*- coding: utf-8 -*-

# Automatically generated from /home/mh/code/fdi/fdi/dataset/resources/ArrayDataset_DataModel.yml. Do not edit.

from collections import OrderedDict
from builtins import str
from builtins import list

import copy

import logging
# create logger
logger = logging.getLogger(__name__)


# Data Model specification for mandatory components
_Model_Spec = {
    'name': 'ArrayDataset_DataModel',
    'description': 'ArrayDataset class data model mandatory configuration',
    'parents': [
        None,
        ],
    'schema': '1.8',
    'metadata': {
        'description': {
                'data_type': 'string',
                'description': 'Description of this dataset',
                'default': 'UNKNOWN',
                'valid': '',
                },
        'type': {
                'data_type': 'string',
                'description': 'Data Type identification.',
                'default': 'ArrayDataset',
                'valid': '',
                },
        'unit': {
                'data_type': 'string',
                'description': 'Unit of every element.',
                'default': None,
                'valid': '',
                },
        'shape': {
                'data_type': 'list',
                'description': 'Number of elements in each dimension. Quick changers to the right.',
                'default': [],
                'valid': '',
                },
        'typecode': {
                'data_type': 'string',
                'description': 'Python internal storage code.',
                'default': 'UNKNOWN',
                'valid': '',
                },
        'version': {
                'data_type': 'string',
                'description': 'Version of dataset',
                'default': '0.3',
                'valid': '',
                },
        'FORMATV': {
                'data_type': 'string',
                'description': 'Version of dataset schema and revision',
                'default': '1.8.0.4',
                'valid': '',
                },
        },
    'datasets': {
        },
    }


Model = copy.deepcopy(_Model_Spec)

