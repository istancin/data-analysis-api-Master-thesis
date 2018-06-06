# -*- coding: utf-8 -*-
"""
Created on Mon June 4 00:44:37 2018

@author: istancin
"""
import sys
import traceback

from weka.core import jvm

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
        '--resultdest', 'results.txt',
        '--label', 'WINNER', '--I-rf', '200',
        '--evaluation', 'cross_validate',
        '--prediction', 'yes',
        '--C-apriori', '0.6', '--N-apriori', '300', '--N-jrip', '60', 
        '--L-csvload', 'WINNER:1,0']
        
#==============================================================================
#     # List of dicts. Based on each dict permutations of arguments are created and added to 
#     # const part of arguments with __permutations_generator 
#==============================================================================
    list_variabil_dict = [{'--algorithm': ['JRip', 'RandomForest', 'J48', 'Logistic', 'NaiveBayes', 'SMO', ], 
    '--path': ['/home/linuxmint/Downloads/dataset_13_14.csv', '/home/linuxmint/Downloads/dataset_14_15.csv', '/home/linuxmint/Downloads/dataset_15_16.csv', '/home/linuxmint/Downloads/dataset_16_17.csv', '/home/linuxmint/Downloads/dataset_17_18.csv', ],
    '--average-n': ['8', '10', '8+', '10+'],
	'--includecol': ['EPR,WINNER,GAME_ID,TEAM_ID','EPR,EPR_OPP,WINNER,GAME_ID,TEAM_ID'],
	'--exclude-game-team-id': ['yes']
        }, 
		{'--algorithm': ['JRip', 'RandomForest', 'J48', 'Logistic', 'NaiveBayes', 'SMO', ], 
    '--path': ['/home/linuxmint/Downloads/dataset_13_14.csv', '/home/linuxmint/Downloads/dataset_14_15.csv', '/home/linuxmint/Downloads/dataset_15_16.csv', '/home/linuxmint/Downloads/dataset_16_17.csv', '/home/linuxmint/Downloads/dataset_17_18.csv', ],
    '--average-n': ['8', '10', '8+', '10+'],
	'--includecol': ['AST,WINNER,GAME_ID,TEAM_ID','AST,AST_OPP,WINNER,GAME_ID,TEAM_ID','AST,SAST,FTAST,PASS,WINNER,GAME_ID,TEAM_ID','AST,SAST,FTAST,PASS,AST_OPP,SAST_OPP,FTAST_OPP,PASS_OPP,WINNER,GAME_ID,TEAM_ID'],
	'--exclude-game-team-id': ['yes']
        }
        ]
    for variabil_dict in list_variabil_dict:
        for args in __permutations_generator(variabil_dict, const):
            sys.argv = args
            try:
                jvm.start()
                main_api()
            except Exception as e:
                print(traceback.format_exc())
            finally:
                pass
#==============================================================================
#         jvm.stop()
#==============================================================================


if __name__ == '__main__':
    main()