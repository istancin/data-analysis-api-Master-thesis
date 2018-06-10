# -*- coding: utf-8 -*-
"""
Created on Sat Jun  2 15:49:05 2018

@author: istancin
"""
import re

from pandas import DataFrame

from converters import arff2df, df2arff
from parsers import create_prediction_data_parser

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
    if not isinstance(data, DataFrame):
        df = arff2df(data)
    else:
        df = data
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


def __leave_one_row_per_game(df):
    """
    Removes "duplicates" from data. Each game will have only one
    row in data. Data will look like this:
    away team statistics, WINNER, home team statistics.
    
    So, home team statistics will have mark _OPP in dataset.
    WINNER = 1 means away team is winner, while WINNER = 0
    means home team is winner.

    :param df: dataframe
    :return: None
    """
    df.drop(df[df.index % 2 == 1].index, inplace=True)
    

def __replace_with_means(row, df_grouped_means):
    """
    Replacing real values in the row with the average of last
    n games (before currently selected game!!!). That average is 
    calculated in df_grouped_means.

    :param row: pandas series
    :param df_grouped_means: dataframe
    :return: pandas series
    """
    game_index = df_grouped_means.loc[int(row.TEAM_ID)].index.values.tolist().index(int(row.name))
    game_num = df_grouped_means.loc[int(row.TEAM_ID)].index.values.tolist()[game_index - 1]
    new_row = df_grouped_means.loc[(int(row.TEAM_ID),int(game_num))]
    #new_row = df_grouped_means.loc[(int(row.TEAM_ID),int(row.name))]
    new_row.name = row.name
    return new_row


def __set_original_column(df, map_index_gameid, column):
    """
    After we replaced original values with average values (function 
    __replace_with_means), we need to get some columns back to
    the original values. 

    :param df: dataframe
    :param map_index_gameid: list of tuples
    :param column: string
    :return: None
    """
    series = df.loc[:,column].copy()
    for x in series.iteritems():
        series.loc[x[0]] = map_index_gameid[x[0]][1]
    df.update(series)

        
def __put_one_game_in_one_row(df):
    """
    Originaly dataframe should have two rows for one game, 
    each row for one team. This function puts it all in
    one row.

    :param df: dataframe
    :return: dataframe
    """
    labels = df.columns.values.tolist()
    new_labels = list(map(lambda x: 'OPP_' + x, labels))
    df = df.reindex(columns=labels + new_labels)
    game_id_prev = 0
    for game_id in df['GAME_ID']:
        if game_id == game_id_prev:
            continue
        ind_w = df.loc[(df['GAME_ID'] == game_id) & ((df['WINNER'].astype('str') == str(1.0)) | (df['WINNER'].astype('str') == str(1)))].index[0]
        ind_l = df.loc[(df['GAME_ID'] == game_id) & ((df['WINNER'].astype('str') == str(0.0)) | (df['WINNER'].astype('str') == str(0)))].index[0]
        df.loc[ind_w, new_labels] = list(df.loc[ind_l, labels])
        df.loc[ind_l, new_labels] = list(df.loc[ind_w, labels])
        game_id_prev = game_id
    return df


def __rename_to_excluderow_arg(args, arg_name):
    """
    Helper function that "rename" prediction_excluderow into
    excluderow so we can use exclude_rows_from_data as it is.

    :param args: dict
    :return: dict
    """
    args['excluderow'] = args[arg_name]
    return args


def create_prediction_data(data):
    """
    Function that creates prediction data. Data for predictions
    are average of last n games of that team. Function gets 
    whole dataset and removes games for which average can not
    be calculated (less than n games), and replaces original
    values with averages. 

    :param df: dataframe
    :return: weka arff data
    """
    df = arff2df(data)
    args = create_prediction_data_parser()
    if '+' in args['average_n']:
        n = int(args['average_n'][:-1])
        expanding = True
    else:
        n = int(args['average_n'])
        expanding = False
    class_label = args['label']
    
    # Sort from first game to last and reset indexes
    df.sort_values('GAME_ID', axis=0, inplace=True)
    df.reset_index(inplace=True)
    
    # Create mapping for index and GAME_ID and WINNER. We will need it later.
    map_index_gameid = []
    map_index_winner = []
    for x in df.iterrows():
        map_index_gameid.append((x[0], x[1].GAME_ID))
        map_index_winner.append((x[0], x[1].WINNER))
    # Calculate means for each team
    if expanding:
        df_grouped_means = df.groupby(['TEAM_ID']).expanding(n).mean()
    else:
        df_grouped_means = df.groupby(['TEAM_ID']).rolling(n).mean()
        
    
    # Delete games where at least one team still did not played n games
    game_ids = []
    for row in df.iterrows():
        game_num = df_grouped_means.loc[int(row[1].TEAM_ID)].index.values.tolist().index(int(row[0]))
        # If selected row has Nan into df_grouped_means
        if game_num < n:
            game_ids.append(row[1].GAME_ID)
    game_ids = list(set(game_ids))
    df = df[~df.GAME_ID.isin(game_ids)]
    
    # Replace original value with mean of last n (calculated above)
    df.update(df.apply(__replace_with_means, args=(df_grouped_means,), axis=1))
    
    # Geting back original GAME_ID
    __set_original_column(df, map_index_gameid, 'GAME_ID')
    __set_original_column(df, map_index_winner, 'WINNER')
    
    # Put one game in one row
    df = __put_one_game_in_one_row(df)
    
    # Removing unneeded columns
    try:
        df.drop(['index', 'OPP_index', 'OPP_GAME_ID', 'OPP_WINNER'], axis=1, inplace=True)
        if args['after_pred_created_excluderow'] is not None:
            df = arff2df(exclude_rows_from_data(df, __rename_to_excluderow_arg(args, 'after_pred_created_excluderow')))
        if args['exclude_game_team_id'] == 'yes':
            df.drop(['GAME_ID', 'TEAM_ID', 'OPP_TEAM_ID'], axis=1, inplace=True)
    except:
        pass
    
    # Leave only one row per game
    __leave_one_row_per_game(df)
    
    # Saving prediction data
    if args['save_prediction_data'] != 'no':
        df.to_csv(args['save_prediction_data'], index=False)
    
    # Class label put as last and return
    return set_as_last_label(df2arff(df), class_label)