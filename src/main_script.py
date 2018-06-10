# -*- coding: utf-8 -*-
"""
Created on Mon June 4 00:44:37 2018

@author: istancin
"""
import sys
import traceback
import copy

from weka.core import jvm
import pandas as pd

from main import main_api



def __update_count(count, max_count):
    """
    Updating count for next permutation. If all permutations are 
    done, return -1 as stoping criteria.

    :param max_count: list
    :param count: list
    :return: list
    """
    n = len(count)
    for i in range(n):
        if (count[n-i-1]) < max_count[n-i-1]:
            count[n-i-1] += 1
            break
        elif count == max_count:
            count = -1
            break
        else:
            count[n-i-1] = 0
    return count


def __append_args(max_count, count, keys, dictionary):
    """
    Function that creates current permutation based on count(indexes that 
    needs to used in this permutation), updates count for next
    permutation.
    
    -dictionary keys are arguments to use while its value is a list of 
    values that needs to be permuted for that key(cmd arg).
    -max_count is here as a stoping criteria. It's list that says how
    many values are in value list of dictionary.
    -count is a list in which we store what are the current elements 
    that we need to pick from each of value lists in dictionary.
    -keys is a list of keys in dictionary

    :param max_count: list
    :param count: list
    :param keys: list
    :param dictionary: dictionary
    :return: tuple
    """
    result = []
    for i in range(len(keys)):
        result.append(keys[i])
        result.append(str(dictionary[keys[i]][count[i]]))
    count = __update_count(count, max_count)
    return count, result
        
        
def __permutations_generator(dictionary, const):
    """
    Function that creates all possible permutations of arguments based on
    const and dict it gets. For example:
    
    const = ['--algorithm', 'Jrip']
    dictionary = {'--path': ['t1.txt', 't2.txt'],
                '--N-jrip': ['50', '70']}
                
    Creates fallowing permutations:
    ['--algorithm', 'Jrip', '--path', 't1.txt', '--N-jrip', '50']
    ['--algorithm', 'Jrip', '--path', 't1.txt', '--N-jrip', '70']
    ['--algorithm', 'Jrip', '--path', 't2.txt', '--N-jrip', '50']
    ['--algorithm', 'Jrip', '--path', 't2.txt', '--N-jrip', '70']
    
    Const part will always be in result while arguments from
    dictionary will be permutated.

    :param dictionary: dictionary
    :param const: list
    :yield: list
    """
    max_count = list()
    count = list()
    keys = list()
    for k, v in dictionary.items():
        max_count.append(len(v)-1)
        count.append(0)
        keys.append(k)
    
    while count != -1:
        args = []
        for x in const:
            args.append(x)
        count, arg = __append_args(max_count, count, keys, dictionary)
        args += arg
        yield args


def __create_stats_data(args, stats_config, stats_config_default_columns, stats, index, column, accuracy_mean, accuracy_std):
    index = tuple([args[args.index(x) + 1] for x in stats_config[0]])
    column = [args[args.index(x) + 1] for x in stats_config[1]]
    column_mean = tuple(column + [stats_config_default_columns[0]])
    column_std = tuple(column + [stats_config_default_columns[1]])
    return index, column_mean, column_std
#==============================================================================
#     stats_lists = [[args[args.index(x) + 1] for x in stats_config[0]],
#                    [args[args.index(x) + 1] for x in stats_config[1]]]
#     stats_lists_cpy = copy.deepcopy(stats_lists)
#     stats_lists[1].append(stats_config_default_columns[0])
#     stats_lists_cpy[1].append(stats_config_default_columns[1])
#     stats_lists.append(accuracy_mean)
#     stats_lists_cpy.append(accuracy_std)
#     stats.append(stats_lists)
#     stats.append(stats_lists_cpy)
#     if stats_lists[0] not in index:
#         index.append(stats_lists[0])
#     if stats_lists[1] not in column:
#         column.append(stats_lists[1])
#     if stats_lists_cpy[1] not in column:
#         column.append(stats_lists_cpy[1])
#     return stats, index, column
#==============================================================================


def __create_excel_stats(stats, xlsx_name):
    writer = pd.ExcelWriter(xlsx_name)
    stats.to_excel(writer, 'Sheet1')
    writer.save()


def main():
    """
    Main function for running multiple tests at once. __permutations_generator
    creates different all the permutations based on const and 
    list_variabil_dict that we manualy create here in this function. Those 
    permutation are actually cmd line arguments which we than use to call 
    main_api function from main.py. Basiclly it's automation for
    runing many different algorithms at once.
    
    const will be in each cmd line.
    list_variabil_dict is a list of dicts. Function will iterate
    over all dicts create all permutations for each dict.
    

    :param dictionary: dictionary
    :param const: list
    :yield: list
    """
    const = ['/home/linuxmint/main.py', '--filetype', 'csv', 
        #'--resultdest', 'results.txt',
        '--label', 'WINNER', '--I-rf', '200',
        '--evaluation', 'cross_validate',
        '--prediction', 'no',
        '--C-apriori', '0.6', '--N-apriori', '300', '--N-jrip', '60', 
        '--L-csvload', 'WINNER:1,0']
        
#==============================================================================
#     # List of dicts. Based on each dict permutations of arguments are created and added to 
#     # const part of arguments with __permutations_generator 
#==============================================================================
    list_variabil_dict = [{'--algorithm': ['JRip', 'RandomForest', 'J48', 'Logistic', 'NaiveBayes', 'SMO'], 
    '--path': ['/home/linuxmint/Downloads/dataset_13_14_prediction.csv', '/home/linuxmint/Downloads/dataset_14_15_prediction.csv', '/home/linuxmint/Downloads/dataset_15_16_prediction.csv', '/home/linuxmint/Downloads/dataset_16_17_prediction.csv', '/home/linuxmint/Downloads/dataset_17_18_prediction.csv'],
	#'--excludecol': ['WIN_GROUP,WIN_GROUP_OPP,SOME2,SOME2_OPP,FG_PCT,FG_PCT_OPP,MIN,TEAM_CITY,TEAM_ABBREAVIATION,TEAM_NAME,WINS,EPR1,EPR2,EPR3,EPR4,TO,TO1,TO2,TO3,SOME,SOME1,SOME3,SOME4,SOME5,SOME6,SOME11,SOME22,SOME33,SOME44,SOME55,SOME66,NEW,NEW1,OLD,OLD1,FG_PCT_OPP,WINS_OPP,EPR1_OPP,EPR2_OPP,EPR3_OPP,EPR4_OPP,TO_OPP,TO1_OPP,TO2_OPP,TO3_OPP,SOME_OPP,SOME1_OPP,SOME3_OPP,SOME4_OPP,SOME5_OPP,SOME6_OPP,NEW_OPP,NEW1_OPP,OLD_OPP'],
    '--includecol': ['AST,OPP_AST,WINNER', 'SAST,OPP_SAST,WINNER', 'AST,SAST,FTAST,PASS,OPP_AST,OPP_SAST,OPP_FTAST,OPP_PASS,WINNER', 'EPR,OPP_EPR,WINNER', 'EPR,AST,OPP_EPR,OPP_AST,WINNER', 'AST,AST_OPP,OPP_AST,OPP_AST_OPP,WINNER', 'SAST,SAST_OPP,OPP_SAST,OPP_SAST_OPP,WINNER', 'AST,SAST,FTAST,PASS,AST_OPP,SAST_OPP,FTAST_OPP,PASS_OPP,OPP_AST,OPP_SAST,OPP_FTAST,OPP_PASS,OPP_AST_OPP,OPP_SAST_OPP,OPP_FTAST_OPP,OPP_PASS_OPP,WINNER', 'EPR,EPR_OPP,OPP_EPR,OPP_EPR_OPP,WINNER', 'EPR,AST,EPR_OPP,AST_OPP,OPP_EPR,OPP_AST,OPP_EPR_OPP,OPP_AST_OPP,WINNER'],
	'--exclude-game-team-id': ['no']
        },
        {'--algorithm': ['JRip', 'RandomForest', 'J48', 'Logistic', 'NaiveBayes', 'SMO'], 
    '--path': ['/home/linuxmint/Downloads/dataset_13_14_prediction.csv', '/home/linuxmint/Downloads/dataset_14_15_prediction.csv', '/home/linuxmint/Downloads/dataset_15_16_prediction.csv', '/home/linuxmint/Downloads/dataset_16_17_prediction.csv', '/home/linuxmint/Downloads/dataset_17_18_prediction.csv'],
	'--includecol': ['UFG_PCT,OPP_UFG_PCT,WINNER', 'CFG_PCT,OPP_CFG_PCT,WINNER', 'UFG_PCT,CFG_PCT,OPP_UFG_PCT,OPP_CFG_PCT,WINNER', 'SOME,OPP_SOME,WINNER', 'SOME1,OPP_SOME1,WINNER', 'SOME2,OPP_SOME2,WINNER', 'SOME3,OPP_SOME3,WINNER', 'SOME4,OPP_SOME4,WINNER', 'SOME5,OPP_SOME5,WINNER', 'SOME6,OPP_SOME6,WINNER', 'SOME22,OPP_SOME22,WINNER' ]
     }
        ]
        
    stats_configs = [(('--path',), ('--algorithm', '--includecol'), 'epr_ast_analysis.xlsx'),
                     (('--path',), ('--algorithm', '--includecol'), 'UCFG_analysis.xlsx')]
    
    
    column = list()
    
    stats = list()
    index = list()
    column = list()
    stats_config_default_columns = ['mean', 'std']
    for i, variabil_dict in enumerate(list_variabil_dict):
        if stats_configs:
            stats_config = stats_configs[i]
            index = pd.MultiIndex.from_product([variabil_dict[x] for x in stats_config[0]])
            temp = [variabil_dict[x] for x in stats_config[1]]
            temp.append(stats_config_default_columns)
            columns = pd.MultiIndex.from_product(temp)
            xlsx_name = stats_config[2]
            stats = pd.DataFrame(index=index, columns=columns)
        for args in __permutations_generator(variabil_dict, const):
            sys.argv = args
            try:
                jvm.start()
                accuracy_mean, accuracy_std = main_api()
                if stats_config:
                    index, column_mean, column_std = __create_stats_data(args, stats_config, stats_config_default_columns, stats,  index, column, accuracy_mean, accuracy_std)
                    stats.loc[index, column_mean] = accuracy_mean
                    stats.loc[index, column_std] = accuracy_std
            except Exception as e:
                print(traceback.format_exc())
            finally:
                pass
#==============================================================================
#         jvm.stop()
#==============================================================================
        __create_excel_stats(stats, xlsx_name)

if __name__ == '__main__':
    main()