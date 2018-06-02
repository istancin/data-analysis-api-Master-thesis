# -*- coding: utf-8 -*-
"""
Created on Fri May 4 11:04:41 2018

@author: istancin
"""
from argparse import ArgumentParser


def csv_loader_parser():
    """
    Csv loader parser. Returns tuple with args as dictionary
    and sufix that needs to be removed.

    :return: tuple
    """
    csv_loader_parser = ArgumentParser(description='Parser for loading CSV files.')
    csv_loader_parser.add_argument('--H', action='store_const', const="",
                                   help='No header row present in the data.')  # -H ne zahtjeva parametar pa je zbog toga postavljen action u store const "" kako bi "prevario" parser i spremio opciju u listu bez argumenata
    csv_loader_parser.add_argument('--N',
                                   help='The range of attributes to force type to be NOMINAL. "first" and "last" are accepted as well. Examples: "first-last", "1,4,5-27,50-last" (default: -none-)')
    csv_loader_parser.add_argument('--L',
                                   help='Optional specification of legal labels for nominal attributes. May be specified multiple times. Batch mode can determine this automatically (and so can incremental mode if the first in memory buffer load of instances contains an example of each legal value). The spec contains two parts separated by a ":". The first part can be a range of attribute indexes or a comma-separated list off attruibute names; the second part is a comma-separated list of labels. E.g "1,2,4-6:red,green,blue" or "att1,att2:red,green,blue"')
    csv_loader_parser.add_argument('--S',
                                   help='The range of attribute to force type to be STRING. "first" and "last" are accepted as well. Examples: "first-last", "1,4,5-27,50-last" (default: -none-)')
    csv_loader_parser.add_argument('--D',
                                   help='The range of attribute to force type to be DATE. "first" and "last" are accepted as well. Examples: "first-last", "1,4,5-27,50-last" (default: -none-)')
    csv_loader_parser.add_argument('--format',
                                   help='The date formatting string to use to parse date values. (default: "yyyy-MM-dd\'T\'HH:mm:ss")')
    csv_loader_parser.add_argument('--R',
                                   help='The range of attribute to force type to be NUMERIC. "first" and "last" are accepted as well. Examples: "first-last", "1,4,5-27,50-last" (default: -none-)')
    csv_loader_parser.add_argument('--M', help='The string representing a missing value. (default: ?)')
    csv_loader_parser.add_argument('--F',
                                   help='The field separator to be used. \'\t\' can be used as well. (default: \',\')')
    csv_loader_parser.add_argument('--E',
                                   help='The enclosure character(s) to use for strings. Specify as a comma separated list (e.g. ",\' (default: ",\')')
    csv_loader_parser.add_argument('--B', help='The size of the in memory buffer (in rows). (default: 100)')
    return vars((csv_loader_parser.parse_known_args())[0]), ''


def csv_saver_parser():
    """
    Csv saver parser. Returns tuple with args as dictionary
    and sufix that needs to be removed.

    :return: tuple
    """
    csv_saver_parser = ArgumentParser(description='Parser for saving data into CSV files.')
    csv_saver_parser.add_argument('--F',
                                  help='The field separator to be used. \'\t\' can be used as well. (default: \',\')')
    csv_saver_parser.add_argument('--M', help='The string representing a missing value. (default: ?)')
    csv_saver_parser.add_argument('--N', action='store_const', const="", help='Don\'t write a header row.')
    csv_saver_parser.add_argument('--decimal',
                                  help='The maximum number of digits to print after the decimal place for numeric values (default: 6)')
    csv_saver_parser.add_argument('--i', help='The input file')
    csv_saver_parser.add_argument('--o', help='The output file')
    return vars((csv_saver_parser.parse_known_args())[0]), ''


def arff_saver_parser():
    """
    Arff saver parser. Returns tuple with args as dictionary
    and sufix that needs to be removed.

    :return: tuple
    """
    arff_saver_parser = ArgumentParser(description='Parser for saving Arff files.')
    arff_saver_parser.add_argument('--i', help='The input file')
    arff_saver_parser.add_argument('--o', help='The output file')
    arff_saver_parser.add_argument('--compress',
                                   help='Compresses the data (uses \'.arff.gz\' as extension instead of \'.arff\') (default: off)')
    arff_saver_parser.add_argument('--decimal',
                                   help='The maximum number of digits to print after the decimal place for numeric values (default: 6)')
    return vars((arff_saver_parser.parse_known_args())[0]), ''


def process_data_parser():
    """
    Process data parser.

    :return: args as dictionary
    """
    process_data_parser = ArgumentParser(description='Process data parser.')
    process_data_parser.add_argument('--includecol', help='Which attributes will be included in data')
    process_data_parser.add_argument('--excludecol', help='Which attributes will be excluded from data')
    process_data_parser.add_argument('--excluderow',
                            help='Which rowa will be excluded from data. Format of input is <label><operation><condition>. More inputs can be separated with ;. For example "-excluderow WINS==50;PTS>=100" (two conditions)')
    process_data_parser.add_argument('--L',
                             help='Optional specification of legal labels for nominal attributes. May be specified multiple times. Batch mode can determine this automatically (and so can incremental mode if the first in memory buffer load of instances contains an example of each legal value). The spec contains two parts separated by a ":". The first part can be a range of attribute indexes or a comma-separated list off attruibute names; the second part is a comma-separated list of labels. E.g "1,2,4-6:red,green,blue" or "att1,att2:red,green,blue"')
    process_data_parser.add_argument('--label', help='The label on which we build the rules (default: last label in file')
    process_data_parser.add_argument('--discretize', choices=['yes', 'no'], default='no', help='Discretize data or not')
    return vars((process_data_parser.parse_known_args())[0])


def data_loader_parser():
    """
    Data loader parser.

    :return: args as dictionary
    """
    dl_parser = ArgumentParser(description='Data loader parser.')
    dl_parser.add_argument('--path', help='Path to the input file')
    dl_parser.add_argument('--dest', help='Path to the output file')
    dl_parser.add_argument('--filetype', choices=['csv', 'arff'], default='csv',
                           help='Type of the input file')
    return vars((dl_parser.parse_known_args())[0])


def main_api_parser():
    """
    Main api parser

    :return: args as dictionary
    """
    main_parser = ArgumentParser(description='Main parser for whole api.')
    main_parser.add_argument('--algorithm', choices=['JRip', 'Apriori', 'RandomForest', 'Logistic'], help='Which algorithm to use.')
    main_parser.add_argument('--prediction', choices=['no', 'yes'], default='yes', help='Are we predicting the data?')
    main_parser.add_argument('--resultdest', help = 'Destination of the file in which rules will be stored (default: no file - print to console')
    return vars((main_parser.parse_known_args())[0])
    
    
def create_prediction_data_parser():
    """
    Create prediction data parser.

    :return: args as dictionary
    """
    cpd_parser = ArgumentParser(description='Create prediction data parser.')
    cpd_parser.add_argument('--average-n', help='Number of games from which we calculate the average.')
    cpd_parser.add_argument('--label', help = 'Class label that will be set as last label.')
    cpd_parser.add_argument('--exclude-game-team-id', default='no', choices=['no','yes'],
                           help='If yes, then GAME_ID and TEAM_ID will be removed from dataset.')
    return vars((cpd_parser.parse_known_args())[0])
    
    
def evaluate_parser():
    """
    Parser for evaluation of algorithms.

    :return: args as dictionary
    """
    evaluate_parser = ArgumentParser(description='Evaluation parser.')
    evaluate_parser.add_argument('--evaluation', choices=['train_test', 'cross_validate', 'test_model'], default='test_model', 
                                 help='What evaluation to use.')
    evaluate_parser.add_argument('--folds', default=10, 
                                 help = 'Number of folds to use if cross_validation is selected.')
    evaluate_parser.add_argument('--train-size', default=66.0, 
                                 help = 'Percent of dataset that will be used for training.')
    return vars((evaluate_parser.parse_known_args())[0])


def jrip_parser():
    """
    JRip parser. Returns tuple with args as dictionary
    and sufix that needs to be removed.

    :return: tuple
    """
    jrip_parser = ArgumentParser(description='Parser for JRip usage')
    jrip_parser.add_argument('--Fjrip', default='3',
                             help='Set number of folds for REP One fold is used as pruning set. (default 3)')
    jrip_parser.add_argument('--Njrip', default='2',
                             help='Set the minimal weights of instances within a split. (default 2.0)')
    jrip_parser.add_argument('--Ojrip', default='2', help='Set the number of runs of optimizations. (Default: 2)')
    jrip_parser.add_argument('--Djrip', action='store_const', const="",
                             help='Set whether turn on the debug mode (Default: false)')
    jrip_parser.add_argument('--Sjrip', default='1', help='The seed of randomization (Default: 1)')
    jrip_parser.add_argument('--Ejrip', action='store_const', const="",
                             help='Whether NOT check the error rate>=0.5 in stopping criteria  (default: check)')
    jrip_parser.add_argument('--Pjrip', action='store_const', const="",
                             help='Whether NOT use pruning (default: use pruning)')
    return vars((jrip_parser.parse_known_args())[0]), 'jrip'


def apriori_parser():
    """
    Apriori parser.  Returns tuple with args as dictionary
    and sufix that needs to be removed.

    :return: tuple
    """
    apriori_parser = ArgumentParser(description='Parser for Apriori usage')
    apriori_parser.add_argument('--Napriori', default='10', help='The required number of rules. (default = 10)')
    apriori_parser.add_argument('--Tapriori', help='The metric type by which to rank rules. (default = confidence)')
    apriori_parser.add_argument('--Capriori', default='0.9', help='The minimum confidence of a rule. (default = 0.9)')
    apriori_parser.add_argument('--Dapriori', default='0.05',
                                help='The delta by which the minimum support is decreased in each iteration. (default = 0.05)')
    apriori_parser.add_argument('--Uapriori', default='1.0', help='Upper bound for minimum support. (default = 1.0)')
    apriori_parser.add_argument('--Mapriori', default='0.1',
                                help='The lower bound for the minimum support. (default = 0.1)')
    apriori_parser.add_argument('--Sapriori',
                                help='If used, rules are tested for significance at the given level. Slower. (default = no significance testing)')
    apriori_parser.add_argument('--Iapriori', action='store_const', const="",
                                help='If set the itemsets found are also output. (default = no)')
    apriori_parser.add_argument('--Rapriori', action='store_const', const="",
                                help='Remove columns that contain all missing values (default = no)')
    apriori_parser.add_argument('--Vapriori', action='store_const', const="",
                                help='Report progress iteratively. (default = no)')
    apriori_parser.add_argument('--Aapriori', action='store_const', const="",
                                help='If set class association rules are mined. (default = no)')
    apriori_parser.add_argument('--Zapriori', action='store_const', const="",
                                help='Treat zero (i.e. first value of nominal attributes) as missing')
    apriori_parser.add_argument('--Bapriori',
                                help='If used, two characters to use as rule delimiters in the result of toString: the first to delimit fields, the second to delimit items within fields. (default = traditional toString result)')
    apriori_parser.add_argument('--capriori', help='The class index. (default = last)')
    return vars((apriori_parser.parse_known_args())[0]), 'apriori'


def unsupervised_discretize_parser():
    """
    Unsuprovised discretize parser. Returns tuple with args as dictionary
    and sufix that needs to be removed

    :return: tuple
    """
    unsup_discretize = ArgumentParser(description='Parser for weka unsuprovised discretization.')
    unsup_discretize.add_argument('--unset-class-temporarilyunsdisc', action='store_const', const="",
                                  help='Unsets the class index temporarily before the filter is applied to the data. (default: no)')
    unsup_discretize.add_argument('--Bunsdisc',
                                  help='Specifies the (maximum) number of bins to divide numeric attributes into. (default = 10)')
    unsup_discretize.add_argument('--Munsdisc',
                                  help='Specifies the desired weight of instances per bin for equal-frequency binning. If this is set to a positive number then the -B option will be ignored. (default = -1)')
    unsup_discretize.add_argument('--Funsdisc', action='store_const', const="",
                                  help='Use equal-frequency instead of equal-width discretization.')
    unsup_discretize.add_argument('--Ounsdisc', action='store_const', const="",
                                  help='Optimize number of bins using leave-one-out estimate of estimated entropy (for equal-width discretization). If this is set then the -B option will be ignored.')
    unsup_discretize.add_argument('--Runsdisc',
                                  help='Specifies list of columns to Discretize. First and last are valid indexes. (default: first-last)')
    unsup_discretize.add_argument('--Vunsdisc', action='store_const', const="",
                                  help='Invert matching sense of column indexes.')
    unsup_discretize.add_argument('--Dunsdisc', action='store_const', const="",
                                  help='Output binary attributes for discretized attributes.')
    unsup_discretize.add_argument('--Yunsdisc', action='store_const', const="",
                                  help='Use bin numbers rather than ranges for discretized attributes.')
    unsup_discretize.add_argument('--precisionunsdisc',
                                  help='Precision for bin boundary labels. (default = 6 decimal places).')
    unsup_discretize.add_argument('--spread-attribute-weightunsdisc', action='store_const', const="",
                                  help='When generating binary attributes, spread weight of old attribute across new attributes. Do not give each new attribute the old weight.')
    return vars((unsup_discretize.parse_known_args())[0]), 'unsdisc'
    
    
def rf_parser():
    """
    RandomForest parser.  Returns tuple with args as dictionary
    and sufix that needs to be removed.

    :return: tuple
    """
    rf_parser = ArgumentParser(description='Parser for RandomForest usage')
    rf_parser.add_argument('--Prf', default='100', help='Size of each bag, as a percentage of the training set size. (default 100)')
    rf_parser.add_argument('--Orf', action='store_const', const="", help='Calculate the out of bag error.')
    rf_parser.add_argument('--store-out-of-bag-predictionsrf', action='store_const', const="", help='Whether to store out of bag predictions in internal evaluation object.')
    rf_parser.add_argument('--output-out-of-bag-complexity-statisticsrf', action='store_const', const="",
                                help='Whether to output complexity-based statistics when out-of-bag evaluation is performed.')
    rf_parser.add_argument('--printrf', action='store_const', const="", help='Print the individual classifiers in the output')
    rf_parser.add_argument('--attribute-importancerf', action='store_const', const="",
                                help='Compute and output attribute importance (mean impurity decrease method)')
    rf_parser.add_argument('--Irf',
                                help='Number of iterations.(current value 100)')
    rf_parser.add_argument('--num-slotsef', 
                                help='Number of execution slots.(default 1 - i.e. no parallelism)(use 0 to auto-detect number of cores)')
    rf_parser.add_argument('--Krf',  default='0', 
                                help='Number of attributes to randomly investigate. (default 0)(<1 = int(log_2(#predictors)+1)).')
    rf_parser.add_argument('--Mrf', default='1', 
                                help='Set minimum number of instances per leaf.(default 1)')
    rf_parser.add_argument('--Vrf',
                                help='Set minimum numeric class variance proportion of train variance for split (default 1e-3).')
    rf_parser.add_argument('--Srf', default='1', 
                                help='Seed for random number generator. (default 1)')
    rf_parser.add_argument('--depthrf', default='0', 
                                help='The maximum depth of the tree, 0 for unlimited. (default 0)')
    rf_parser.add_argument('--Nrf', default='0', help='Number of folds for backfitting (default 0, no backfitting).')
    rf_parser.add_argument('--Urf', action='store_const', const="",
                                help='Allow unclassified instances.')
    rf_parser.add_argument('--Brf', action='store_const', const="",
                                help='Break ties randomly when several attributes look equally good.')
    rf_parser.add_argument('--output-debug-inforf', action='store_const', const="",
                                help='If set, classifier is run in debug mode and may output additional info to the console')
    rf_parser.add_argument('--do-not-check-capabilitiesrf', action='store_const', const="",
                                help='If set, classifier capabilities are not checked before classifier is built (use with caution).')
    rf_parser.add_argument('--num-decimal-placesrf',
                                help='The number of decimal places for the output of numbers in the model (default 2).')
    rf_parser.add_argument('--batch-sizerf',
                                help='The desired batch size for batch prediction  (default 100).')
    return vars((rf_parser.parse_known_args())[0]), 'rf'
    
    
def logistic_parser():
    """
    Logistic regression parser.  Returns tuple with args as dictionary
    and sufix that needs to be removed.

    :return: tuple
    """
    lr_parser = ArgumentParser(description='Logistic regression parser')
    lr_parser.add_argument('--Dlogistic', action='store_const', const="", help='Turn on debugging output.')
    lr_parser.add_argument('--Rlogistic', help='Set the ridge in the log-likelihood.')
    lr_parser.add_argument('--Mlogistic', default='-1', help='Set the maximum number of iterations (default -1, until convergence).')
    return vars((lr_parser.parse_known_args())[0]), 'logistic'