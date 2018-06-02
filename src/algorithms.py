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


def JRip(data, result_dest=None):
    """
    Function for building ruleset with JRip (Ripper) algorithm. Evaluation is
    also done. Information about parameters of algorithm, ruleset and
    evaluation results are printed to console or writen to file depending on
    result_dest param.

    :param data: weka arff data
    :param result_dest: results destination
    :return: None
    """
    name = "JRip"
    args, _sufix= jrip_parser()
    jrip = Classifier(classname="weka.classifiers.rules.JRip",
                      options=args_to_weka_options(args, _sufix))
    jrip.build_classifier(data)
    evaluation = __evaluate(jrip, data)

    if result_dest:
        with open(result_dest, 'a') as file:
            file.write(__print_algorithm_header(jrip.to_commandline(), __get_header_of_data(data), name))
            file.write(str(jrip))
            file.write(evaluation.summary())
    else:
        print(__print_algorithm_header(jrip.to_commandline(), __get_header_of_data(data), name))
        print(jrip)
        print(evaluation.summary())


def __get_header_of_data(data):
    """
    Function that will return us header of data.

    :param data: weka arff data
    :return: list header
    """
    df = arff2df(data)
    return list(df.columns.values)


def Apriori(data, result_dest=None):
    """
    Function for building ruleset with Apriori algorithm. Information
    about parameters of algorithm and ruleset are printed to console
    or writen to file depending on result_dest param.

    :param data: weka arff data
    :param result_dest: results destination
    :return: None
    """
    name = "Apriori"
    args, _sufix = apriori_parser()
    apriori = Associator(classname="weka.associations.Apriori",
                      options=args_to_weka_options(args, _sufix))
    apriori.build_associations(data)

    if result_dest:
        with open(result_dest, 'a') as file:
            file.write(__print_algorithm_header(apriori.to_commandline(), __get_header_of_data(data), name))
            file.write(str(apriori))
    else:
        print(__print_algorithm_header(apriori.to_commandline(), __get_header_of_data(data), name))
        print(str(apriori))
    
    
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


def RandomForrest(data, result_dest):
    """
    RandomForest classifier. Information
    about parameters of algorithm and ruleset are printed to console
    or written to file depending on result_dest param.

    :param apriori: apriori class
    :param header: string
    :return: string
    """
    args, _sufix= rf_parser()
    random_forest = Classifier(classname="weka.classifiers.trees.RandomForest",
                      options=args_to_weka_options(args, _sufix))
    random_forest.build_classifier(data)
    evaluation = __evaluate(random_forest, data)

    if result_dest:
        with open(result_dest, 'a') as file:
            file.write(__print_algorithm_header(random_forest.to_commandline(), __get_header_of_data(data), "Random Forest"))
            file.write(str(random_forest))
            file.write(evaluation.summary())
    else:
        print(__print_algorithm_header(random_forest.to_commandline(), __get_header_of_data(data), "Random Forest"))
        print(random_forest)
        print(evaluation.summary())
        
        
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
        
        
def Logistic(data, result_dest):
    """
    RandomForest classifier. Information
    about parameters of algorithm and ruleset are printed to console
    or written to file depending on result_dest param.

    :param apriori: apriori class
    :param header: string
    :return: string
    """
    args, _sufix= logistic_parser()
    logistic = Classifier(classname="weka.classifiers.functions.Logistic",
                      options=args_to_weka_options(args, _sufix))
    logistic.build_classifier(data)
    evaluation = __evaluate(logistic, data)

    if result_dest:
        with open(result_dest, 'a') as file:
            file.write(__print_algorithm_header(logistic.to_commandline(), __get_header_of_data(data), "Logistic Regression"))
            file.write(str(logistic))
            file.write(evaluation.summary())
    else:
        print(__print_algorithm_header(logistic.to_commandline(), __get_header_of_data(data), "Logistic Regression"))
        print(logistic)
        print(evaluation.summary())


def main_logistic(result_dest=None):
    """
    Function that is caled for usage of RandomForest. Based on command
    line arguments, data will be loaded and RandomForest classifier 
    will be built.

    :param result_dest: results destination
    """
    data = data_loader()
    data = create_prediction_data(data)
    data.class_is_last()
    Logistic(data, result_dest)
    


def main_JRip(result_dest=None, prediction=None):
    """
    Function that is caled for usage of JRip. Based on command
    line arguments, data will be loaded and JRip rules will be
    generated with given data.

    :param result_dest: results destination
    """
    data = data_loader()
    if prediction:
        data = create_prediction_data(data)
    data.class_is_last()
    JRip(data, result_dest)


def main_apriori(result_dest=None):
    """
    Function that is caled for usage of Apriori. Based on command
    line arguments, data will be loaded and Apriori rules will be
    generated with given data.

    :param result_dest: results destination
    """
    data = data_loader()
    data.class_is_last()
    data = unsupervised_discretize(data)
    Apriori(data, result_dest)
    
    
def main_random_forest(result_dest=None):
    """
    Function that is caled for usage of RandomForest. Based on command
    line arguments, data will be loaded and RandomForest classifier 
    will be built.

    :param result_dest: results destination
    """
    data = data_loader()
    data = create_prediction_data(data)
    data.class_is_last()
    RandomForrest(data, result_dest)