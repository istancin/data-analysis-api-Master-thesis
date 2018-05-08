# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 00:32:48 2018

@author: linuxmint
"""
import re

from converters import arff2df, df2arff


def __args_to_weka_options(args):
    """
    Function that creates list with options (args) in format
    approperiate for weka.

    :param args: dictionery with command line input
    :return: list of command line arguments
    """
    result = []
    for k,v in args.items():
        if v:
            result.append("-" + k)
            result.append(v)
        elif v == "":
            result.append("-" + k)
    return result


def args_to_weka_options(args, sufix):
    """
    Function that creates list with options (args) in format
    appropriate for weka. This function dictionary of
    command line input that is not the same as in weka and
    converts it so weka could recognize those commands.

    For example, our parser for JRip algorithm have -Njrip
    parameter, while weka accepts only -N. In that case we
    call this function and we pass argument sufix='jrip',
    and function will return us list of argument appropriate
    for weka (-N).

    :param args: dictionary with command line input
    :param sufix: string
    :return: list of command line arguments
    """
    if sufix == '':
        return __args_to_weka_options(args)
    result = []
    for k,v in args.items():
        if v:
            result.append("-" + k[:-len(sufix)])
            result.append(v)
        elif v == "":
            result.append("-" + k[:-len(sufix)])
    return result


def set_as_last_label(data, label):
    """
    Function that sets given label as last in data. Last label
    will always be class label.

    :param path: input file
    :param label: label of class
    :return: None
    """
    df = arff2df(data)
    df['temp_column_name'] = df[label]
    del df[label]
    column_names = df.columns.values
    column_names[-1] = label
    df.columns = column_names
    return df2arff(df)


def select_needed_columns(data, args):
    """
    Function that removes columns we do not need from data.
    Removes columns based on --includecol or --excludecol
    arguments.

    :param data: weka arff data
    :param args: dictionary with args
    :return: weka arff data
    """
    if args['includecol'] and args['excludecol']:
        raise ValueError('You can not use both, includecol and excludecol, at the same time.')
    df = arff2df(data)

    # Part of code in which we decide what to include into new csv
    if args['includecol']:
        return __include_selected_columns(df, args['includecol'].split(','))

    include = []
    all_columns = df.columns.values
    for col in all_columns:
        if col not in args['excludecol'].split(',') and str(col) not in args['excludecol'].split(
                ','):  # Second condition is here so it would work when there is no header in df
            include.append(col)
    return __include_selected_columns(df, include)


def __include_selected_columns(df, include):
    """
    Function that leaves only columns that are in include list
    and deletes all other columns.

    :param df: dataframe
    :param include: list of labels
    :return: weka arff data
    """
    all_columns = df.columns.values
    for col in all_columns:
        if col not in include and str(col) not in include: # Second condition is here so it would work when there is no header in df
            del df[col]
    return df2arff(df)


def exclude_rows_from_data(data, args):
    """
    Function that will exclude rows from data based on conditions
    in args[excluderow].

    :param data: weka arff data
    :param args: args
    :return: weka arff data
    """
    df = arff2df(data)
    # Go through all conditions and remove selected rows
    conditions = args['excluderow'].split(';')
    for condition in conditions:
        __delete_undesired_rows(df, __parse_excluderow_conditions(condition))
    return df2arff(df)


def __parse_excluderow_conditions(condition):
    """
    Splits condition into label, condition operator and condition bound.

    :param condition: string
    :return: tuple
    """
    spliter = re.search('([!=<>])+', condition).group(0)
    temp = condition.split(spliter)
    return temp[0], spliter, temp[1]


def __delete_undesired_rows(df, condition):
    """
    Function which drops some rows from dataframe based on condition.

    :param df: dataframe
    :param condition: tuple
    :return: None
    """
    label, operation, bound = condition
    if __is_number(bound):
        bound = float(bound)

    if operation == '==':
        df.drop(df[df[label] == bound].index, inplace=True)
    elif operation == '>=':
        df.drop(df[df[label] >= bound].index, inplace=True)
    elif operation == '<=':
        df.drop(df[df[label] <= bound].index, inplace=True)
    elif operation == '!=':
        df.drop(df[df[label] != bound].index, inplace=True)
    elif operation == '<':
        df.drop(df[df[label] < bound].index, inplace=True)
    elif operation == '>':
        df.drop(df[df[label] > bound].index, inplace=True)
    else:
        raise ValueError('Unknown comparation operator')


def create_nominal_value(data, arg):
    """
    Function that creates one-vs-rest nominal value in our data.
    For example, if label 'NUM' have values of 1,2 and 3, and
    we want that label to have only values 1 for 1 and 'rest' for
    2 or 3, we will call this function with value of arg='NUM:1,rest'.

    :param data: weka arff data
    :param arg: arg value
    :return: weka arff data
    """
    df = arff2df(data)
    column_name, labels = tuple(arg.split(':'))
    good_label = labels.split(',')[0] # Value we want to keep will always be first
    if __is_number(good_label):
        good_label = float(good_label)

    # Change undesired values into 'rest', save and return path
    df.loc[(df[column_name] != good_label), column_name] = 'rest'
    return df2arff(df)


def __is_number(s):
    """
    Function that checks if sting is float.

    :param s: string
    :return: boolean
    """
    try:
        float(s)
        return True
    except ValueError:
        return False