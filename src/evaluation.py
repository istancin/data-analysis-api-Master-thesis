# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 15:48:46 2018

@author: istancin
"""
from weka.classifiers import Evaluation
from weka.core.classes import Random

from parsers import evaluate_parser


def evaluate(classifier, data):
    """
    Private function that makes evaluation of classifier on
    given data. With command line arguments we can chose which 
    evaluation to use.

    :param classifier: Classifier
    :param data: weka arff data
    :return: Evaluation
    """
    args = evaluate_parser()
    evaluation = Evaluation(data)
    if args['evaluation'] == 'train_test':
        evaluation.evaluate_train_test_split(classifier, data, int(args['train_size']), Random(1))
    elif args['evaluation'] == 'cross_validate':
        evaluation.crossvalidate_model(classifier, data, int(args['folds']), Random(42))
    else:
        evaluation.test_model(classifier, data)
    return evaluation