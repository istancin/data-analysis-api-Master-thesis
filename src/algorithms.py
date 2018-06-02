# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 10:34:43 2018

@author: istancin
"""
import datetime
import sys

from weka.classifiers import Classifier, Evaluation
from weka.associations import Associator
from weka.core.classes import Random

from helper import args_to_weka_options, create_prediction_data
from loaders_savers import data_loader
from discretization import unsupervised_discretize
from parsers import jrip_parser, apriori_parser, rf_parser, evaluate_parser, logistic_parser
from converters import arff2df


parsers_dict = {'JRip': jrip_parser,
                'Apriori': apriori_parser,
                'RandomForest': rf_parser,
                'Logistic': logistic_parser
                }
                
algorithms_path_dict = {'JRip': "weka.classifiers.rules.JRip",
                        'Apriori': "weka.associations.Apriori",
                        'RandomForest': "weka.classifiers.trees.RandomForest",
                        'Logistic': "weka.classifiers.functions.Logistic"
                        }


def __build_classifier(algorithm_name, data, result_dest=None):
    """
    Function for building clasifier based on arguments we send to function.
    algorithm_name is for example JRip or Logistic or RandomForest...
    algorithm_path is for example weka.classifiers.rules.JRip, or 
    weka.classifiers.trees.RandomForest, ...

    :param algorithm_name: string
    :param algorithm_path: string
    :param data: weka arff data
    :param result_dest: results destination
    :return: None
    """
    args, _sufix= parsers_dict[algorithm_name]()#jrip_parser()
    classifier = Classifier(classname=algorithms_path_dict[algorithm_name],
                      options=args_to_weka_options(args, _sufix))
    classifier.build_classifier(data)
    evaluation = __evaluate(classifier, data)

    if result_dest:
        with open(result_dest, 'a') as file:
            file.write(__print_algorithm_header(classifier.to_commandline(), __get_header_of_data(data), algorithm_name))
            file.write(str(classifier))
            file.write(evaluation.summary())
    else:
        print(__print_algorithm_header(classifier.to_commandline(), __get_header_of_data(data), algorithm_name))
        print(classifier)
        print(evaluation.summary())


def __get_header_of_data(data):
    """
    Function that will return us header of data.

    :param data: weka arff data
    :return: list header
    """
    df = arff2df(data)
    return list(df.columns.values)


def __build_associations(algorithm_name, data, result_dest=None):
    """
    Function for building ruleset with Apriori algorithm. Information
    about parameters of algorithm and ruleset are printed to console
    or writen to file depending on result_dest param.

    :param data: weka arff data
    :param result_dest: results destination
    :return: None
    """
    args, _sufix = parsers_dict[algorithm_name]()#apriori_parser()
    associator = Associator(classname=algorithms_path_dict[algorithm_name],
                      options=args_to_weka_options(args, _sufix))
    associator.build_associations(data)

    if result_dest:
        with open(result_dest, 'a') as file:
            file.write(__print_algorithm_header(associator.to_commandline(), __get_header_of_data(data), algorithm_name))
            file.write(str(associator))
    else:
        print(__print_algorithm_header(associator.to_commandline(), __get_header_of_data(data), algorithm_name))
        print(str(associator))
    
    
def __evaluate(classifier, data):
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
        
        
def __print_algorithm_header(algorithm_cmd, data_header, algorithm_name):
    """
    Private function that creates a header for given algorithm.

    :param algorithm_cmd: string
    :param header: string
    :param name: string
    :return: string
    """
    header = "\n\n\n========== " + algorithm_name + "=========\n"
    header += "Command line:\n\t" + str(sys.argv)
    header += "\nStart time: \n\t" + str(datetime.datetime.now())
    header += "\nHeader of dataset:\n\t" + str(data_header)
    header += "\nArguments of algorithm: \n\t"
    header += algorithm_cmd + '\n'
    return header
        
        
def main_clasifiers(algorithm_name, result_dest=None, prediction=None):
    """
    Function that is caled for usage of JRip. Based on command
    line arguments, data will be loaded and JRip rules will be
    generated with given data.

    :param result_dest: results destination
    """
    data = data_loader()
    if prediction == 'yes':
        data = create_prediction_data(data)
    data.class_is_last()
    __build_classifier(algorithm_name, data, result_dest)


def main_associations(algorithm_name, result_dest=None, prediction=None):
    """
    Function that is caled for usage of Apriori. Based on command
    line arguments, data will be loaded and Apriori rules will be
    generated with given data.

    :param result_dest: results destination
    """
    data = data_loader()
    if prediction == 'yes':
        data = create_prediction_data(data)
    data.class_is_last()
    data = unsupervised_discretize(data)
    __build_associations(algorithm_name, data, result_dest=result_dest)