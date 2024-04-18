#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Preprocess BDI Questionnaire queries'''

import argparse
import sys
from os import makedirs
from os.path import basename, isdir, isfile, join, dirname, splitext

from nltk.corpus import stopwords as stopwords_nltk

__author__ = "Esteban Rissola"
__credits__ = ["Esteban Rissola"]
__version__ = "1.0.1"
__maintainer__ = "Esteban Rissola"
__email__ = "esteban.andres.rissola@gmail.com"

def load_stopwords(filepath):
    stopwords = set()
    with open(filepath, 'rt') as fp:
        for line in fp:
            stopwords.add(line.strip())
    return stopwords

def main():
    parser = argparse.ArgumentParser(description='BDI Questionnaire Preprocessing')
    help_msgs = []
    
    # Input arguments #
    help_msgs.append('raw query filepath (txt)')
    help_msgs.append('stopwords choice (default none)')

    # Output arguments #
    help_msgs.append('preprocessed query filepath (txt)')

    # Input arguments #
    parser.add_argument('-i', '--input', action='store', metavar='PATH', 
                        dest='bdi_raw_queries_filepath', required=True, 
                        help=help_msgs[0])
    
    parser.add_argument('-s', '--stopwords', action='store', metavar='nltk|PATH',
                        help=help_msgs[1], dest='stopwords_path', required=False, 
                        default='none')
    
    # Output arguments #
    parser.add_argument('-o', '--output_dir', action='store', metavar='PATH',
                        default=None, help=help_msgs[2], required=False)
    
    # Arguments parsing #
    args = parser.parse_args()

    # Check if input exists and is a file. Otherwise, exit #
    if not isfile(args.bdi_raw_queries_filepath):
        sys.exit(' %s -> the path does not point to a valid file')
    
    # The default output directory is the same as the input file if not specified #
    default_output_dir = dirname(args.bdi_raw_queries_filepath)
    if args.output_dir is None:
        args.output_dir = default_output_dir

    # Create the output directory if it does not exist #
    if not isdir(args.output_dir):
        makedirs(args.output_dir)

    if args.stopwords_path == 'none':
        # No stopwords removal #
        stopwords = set()
    elif args.stopwords_path == 'nltk':
        # 'Mild' list #
        stopwords = set(stopwords_nltk.words('english'))
    else:
        if isfile(args.stopwords_path):
            # 'Agressive' stopwords list #
            stopwords = load_stopwords(args.stopwords_path)
        else:
            sys.exit('The input path does not point to a valid file')

    # Remove stopwords and lowercase #
    bdi_norm_queries = []
    with open(args.bdi_raw_queries_filepath) as fp:
        for line in fp:
            query = ''
            tokens = line.strip().lower().split()
            for t in tokens:
                if not t in stopwords:
                    query += t + ' '
            bdi_norm_queries.append(query.strip())
    
    filename = splitext(basename(args.bdi_raw_queries_filepath))[0] + '_norm.txt'
    bdi_norm_queries_filepath = join(args.output_dir, filename)
    with open(bdi_norm_queries_filepath, 'wt') as fp:
        for i, q in enumerate(bdi_norm_queries):
            fp.write('%d\t%s\n' % (i + 1, q))
    return 0


if __name__ == '__main__':
    main()
