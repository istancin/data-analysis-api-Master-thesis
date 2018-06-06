# -*- coding: utf-8 -*-
"""
Created on Sun Apr 22 15:35:55 2018

@author: istancin
"""
import traceback

from weka.core import jvm

from algorithms import main_clasifiers, main_associations
from parsers import main_api_parser


def main_api():
    """
    Function in which we decides which algorithm to use.

    :return: None
    """
    args = main_api_parser()

    if args['algorithm'] == 'JRip':
        main_clasifiers(args['algorithm'], result_dest=args['resultdest'], prediction=args['prediction'])
    elif args['algorithm'] == 'Apriori':
        main_associations(args['algorithm'], result_dest=args['resultdest'], prediction=args['prediction'])
    elif args['algorithm'] == 'RandomForest':
        main_clasifiers(args['algorithm'], result_dest=args['resultdest'], prediction=args['prediction'])
    elif args['algorithm'] == 'Logistic':
        main_clasifiers(args['algorithm'], result_dest=args['resultdest'], prediction=args['prediction'])
    elif args['algorithm'] == 'J48':
        main_clasifiers(args['algorithm'], result_dest=args['resultdest'], prediction=args['prediction'])
    elif args['algorithm'] == 'NaiveBayes':
        main_clasifiers(args['algorithm'], result_dest=args['resultdest'], prediction=args['prediction'])
    elif args['algorithm'] == 'SMO':
        main_kernel_clasifiers(args['algorithm'], args['algorithm'], result_dest=args['resultdest'], prediction=args['prediction'])
    else:
        raise ValueError("Invalid --algorithm parameter.")


def main():
    """
    Main function of whole application.

    :return: None
    """
	try:
        jvm.start()
        main_api()
    except Exception as e:
        print(traceback.format_exc())
    finally:
        jvm.stop()


if __name__ == '__main__':
    main()