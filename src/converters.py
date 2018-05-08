# -*- coding: utf-8 -*-
"""
Created on Fri May 4 11:04:41 2018

@author: istancin
"""
from os import remove

import arff as liacarff
import pandas as pd


def arff2df(data):
    """
    Converts arff to pandas dataframe.

    :param data: string
    :return: pandas Dataframe
    """
    arff = liacarff.loads(str(data))
    attr = [a[0] for a in arff['attributes']]
    return pd.DataFrame(data=arff['data'], columns=attr)


def df2arff(df):
    """
    Converts pandas dataframe to arff data.

    :param df: pandas dataframe
    :return: weka arff data
    """
    from loaders_savers import load_csv # Imported here because of circular dependencies
    path = 'tmp_tmp432tmp123_tm_p_blabla3da.csv' # Stupid name to "ensure" we do not override something
    df.to_csv(path, index=False)
    try:
        data = load_csv(path)
    finally:
        remove(path)
    return data