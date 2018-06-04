# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 00:32:48 2018

@author: istancin
"""


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