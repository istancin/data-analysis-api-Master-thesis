# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 15:35:55 2018

@author: linuxmint
"""
import traceback

from weka.core import jvm

from algorithms import main_JRip, main_apriori, main_random_forest
from parsers import main_api_parser


def main_api():
    """
    Main function of whole aplication.

    :return: None
    """
    args = main_api_parser()

    if args['algorithm'] == 'JRip':
        if args['prediction'] == 'no':
            main_JRip(result_dest=args['resultdest'])
        elif args['prediction'] == 'yes': 
            main_JRip(result_dest=args['resultdest'], prediction=True)
    elif args['algorithm'] == 'Apriori':
        main_apriori(result_dest=args['resultdest'])
    elif args['algorithm'] == 'RandomForest':
        main_random_forest(result_dest=args['resultdest'])
    else:
        raise ValueError("Invalid --algorithm parameter.")


if __name__ == '__main__':
    try:
        jvm.start()
        main_api()
    except Exception as e:
        print(traceback.format_exc())
    finally:
        jvm.stop()