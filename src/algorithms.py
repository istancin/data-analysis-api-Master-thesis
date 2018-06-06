# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 10:34:43 2018

@author: istancin
"""
import datetime
import sys
import random

from weka.classifiers import Classifier, Kernel
from weka.associations import Associator

from helper import args_to_weka_options
from data_manipulation import create_prediction_data
from loaders_savers import data_loader
from discretization import unsupervised_discretize
from parsers import jrip_parser, apriori_parser, rf_parser, logistic_parser, j48_parser, naive_bayes_parser, smo_parser, poly_kernel_parser
from converters import arff2df
from evaluation import evaluate


parsers_dict = {'JRip': jrip_parser,
                'Apriori': apriori_parser,
                'RandomForest': rf_parser,
                'Logistic': logistic_parser,
                'J48': j48_parser,
                'NaiveBayes': naive_bayes_parser,
                'SMO': smo_parser
                }
                
algorithms_path_dict = {'JRip': "weka.classifiers.rules.JRip",
                        'Apriori': "weka.associations.Apriori",
                        'RandomForest': "weka.classifiers.trees.RandomForest",
                        'Logistic': "weka.classifiers.functions.Logistic",
                        'J48': "weka.classifiers.trees.J48",
                        'NaiveBayes': "weka.classifiers.bayes.NaiveBayes",
                        'SMO': "weka.classifiers.functions.SMO"
                        }
                        
kernel_parsers_dict = {'SMO': poly_kernel_parser
                       }
                       
kernel_path_dict = {'SMO': "weka.classifiers.functions.supportVector.PolyKernel"
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
    args, _sufix= parsers_dict[algorithm_name]()
    classifier = Classifier(classname=algorithms_path_dict[algorithm_name],
                      options=args_to_weka_options(args, _sufix))
    classifier.build_classifier(data)
    evaluation = evaluate(classifier, data)

    if result_dest:
        with open(result_dest, 'a') as file:
            file.write(__print_algorithm_header(classifier.to_commandline(), __get_header_of_data(data), algorithm_name))
            file.write(str(classifier))
            file.write(evaluation.summary())
#==============================================================================
#             file.write(str(evaluation.percent_correct))
#==============================================================================
    else:
        print(__print_algorithm_header(classifier.to_commandline(), __get_header_of_data(data), algorithm_name))
        print(classifier)
        print(evaluation.summary())
        
        
def __build_kernel_classifier(algorithm_name, kernel_name, data, result_dest=None):
    """
    Function for building kernel clasifier based on arguments we send to function.
    algorithm_name is for example JRip or Logistic or RandomForest...
    algorithm_path is for example weka.classifiers.rules.JRip, or 
    weka.classifiers.trees.RandomForest, ... 
    
    Kernel name for now will be the same as algorithm name. Later when we 
    will want to use different kernels that needs to be changed.

    :param algorithm_name: string
    :param kernel_name: string
    :param algorithm_path: string
    :param data: weka arff data
    :param result_dest: results destination
    :return: None
    """
    args_cls, _sufix_cls = parsers_dict[algorithm_name]()
    args_ker, _sufix_ker = kernel_parsers_dict[kernel_name]()
    kernel = Kernel(classname=kernel_path_dict[kernel_name], options=args_to_weka_options(args_ker, _sufix_ker))
    classifier = Classifier(classname=algorithms_path_dict[algorithm_name],
                      options=args_to_weka_options(args_cls, _sufix_cls))
    classifier.kernel = kernel
    classifier.build_classifier(data)
    evaluation = evaluate(classifier, data)

    if result_dest:
        with open(result_dest, 'a') as file:
            file.write(__print_algorithm_header(classifier.to_commandline(), __get_header_of_data(data), algorithm_name))
            file.write(str(classifier))
            file.write(evaluation.summary())
#==============================================================================
#             file.write(str(evaluation.percent_correct))
#==============================================================================
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
    Function for building association algorithms. Based on name we select 
    proper algorithm.

    :param algorithm_name: string
    :param data: weka arff data
    :param result_dest: results destination
    :return: None
    """
    args, _sufix = parsers_dict[algorithm_name]()
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
    if algorithm_name == "RandomForest":
        for i in range(5):
            try:
                index = (sys.argv).index('--S-rf')
                del sys.argv[index]
                del sys.argv[index]
            except ValueError:
                pass
            (sys.argv).append('--S-rf')
            (sys.argv).append(str(random.randint(0,10000)))
            __build_classifier(algorithm_name, data, result_dest)
    else:
        __build_classifier(algorithm_name, data, result_dest)
    
    
def main_kernel_clasifiers(algorithm_name, kernel_name, result_dest=None, prediction=None):
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
    __build_kernel_classifier(algorithm_name, kernel_name, data, result_dest)


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