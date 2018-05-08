# -*- coding: utf-8 -*-
"""
Created on Fri May  4 02:33:01 2018

@author: linuxmint
"""
from weka.filters import Filter

from helper import args_to_weka_options
from parsers import unsuprovised_discretize_parser


def unsuprevised_discretize(data):
    """
    Function for discretization of data. Function uses weka implementation
    weka.filters.unsupervised.attribute.Discretize.

    :param data: weka arff data
    :return: weka arff data
    """
    args, _sufix = unsuprovised_discretize_parser()

    filt = Filter(classname='weka.filters.unsupervised.attribute.Discretize',
                  options=args_to_weka_options(args, _sufix))
    filt.inputformat(data)
    return filt.filter(data)