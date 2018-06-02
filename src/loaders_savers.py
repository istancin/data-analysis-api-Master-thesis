# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 18:15:34 2018

@author: istancin
"""
import traceback

from weka.core import jvm
from weka.core.converters import Loader, Saver

from discretization import unsupervised_discretize
from parsers import process_data_parser, csv_loader_parser, data_loader_parser, arff_saver_parser, csv_saver_parser
from helper import args_to_weka_options
from data_manipulation import select_needed_columns, exclude_rows_from_data, set_as_last_label, create_nominal_value


def load_csv(path):
    """
    Function for importing data from csv. Function uses weka implementation
    of CSVLoader.

    :param path: input file
    :return: weka arff data
    """
    args, _sufix = csv_loader_parser()
    loader = Loader(classname='weka.core.converters.CSVLoader',
                    options=args_to_weka_options(args, _sufix))
    return loader.load_file(path)


def load_arff(path):
    """
    Function for importing data from arff file. Function uses weka implementation
    of ArffLoader.

    :param path: input file
    :return: weka arff data
    """
    loader = Loader(classname="weka.core.converters.ArffLoader")
    return loader.load_file(path)


def save_csv(data, dest):
    """
    Function for saving weka arff data into csv file. Function uses weka
    implementation of CSVSaver.

    :param data: weka arff data
    :param dest: output file
    :return: None
    """
    args, _sufix = csv_saver_parser()
    saver = Saver(classname='weka.core.converters.CSVSaver',
                  options=args_to_weka_options(args, _sufix))
    saver.save_file(data, dest)


def save_arff(data, dest):
    """
    Function for saving data into arff file. Function uses weka implementation
    of ArffSaver.

    :param data: weka arff data
    :param dest: output file
    :return: None
    """
    args, _sufix = arff_saver_parser()
    saver = Saver(classname='weka.core.converters.ArffSaver',
                  options=args_to_weka_options(args, _sufix))
    saver.save_file(data, dest)


def data_loader():
    """
    Function that should be called from other modules for loading data.
    Depending on --filetype argument function will load data with appropriate
    function. After data is loaded, it will be processed in
    __process_data function based on command line arguments.

    :return: weka arff data
    """
    args = data_loader_parser()
    if args['filetype'] == 'csv':
        data = load_csv(args['path'])
    else:
        data = load_arff(args['path'])
    return __process_data(data)


def __process_data(data):
    """
    Function that adjusts data based on command line arguments.

    :param data: weka arff data
    :param args: args as dictionary
    :return: weka arff data
    """
    args = process_data_parser()
    if args['L'] and 'rest' in args['L']:
        data = create_nominal_value(data, args['L'])
    if args['excluderow']:
        data = exclude_rows_from_data(data, args)
    if args['includecol'] or args['excludecol']:
        data = select_needed_columns(data, args)
    if args['label']:
        data = set_as_last_label(data, args['label'])
    if args['discretize'] == 'yes':
        data = unsupervised_discretize(data)
    return data


def csv2arff():
    """
    Function that loads csv and saves it to arff.

    :return: None
    """
    args = data_loader_parser()
    save_arff(load_csv(args['path']), args['dest'])


if __name__ == '__main__':
    try:
        jvm.start()
        csv2arff()
    except Exception as e:
        print(traceback.format_exc())
    finally:
        jvm.stop()