#!/bin/python3

import argparse
import os
import pyranges as pr
import pandas as pd

def count_overlaps(target_file,fragments_dir):
    '''
    Counts the number of overlapping intervals between a target bed file and a 
    directory containing lots of bed files.
    inputs:
        target_file (string): path pointing to a bed file
        fragments_dir (string): path pointing to a directory, with structure dir/barcode/barcode.bed
    returns (pd.DataFrame): overlap counts. Each region in targets_file as columns, 
        each file in fragments_dir a row.
    '''
    grs = {}
    target = pr.read_bed(target_file)
    for entry in os.scandir(fragments_dir):
        barcode = os.path.split(entry.path)[1]
        fragments_file = os.path.join(entry.path, barcode+'.bed')
        grs[barcode] = pr.read_bed(fragments_file)
    r = pr.count_overlaps(grs,target)
    i = (r.Chromosome.astype(str) + ':' + r.Start.astype(str) + '-' + r.End.astype(str)).values
    return r.df.set_index(i).iloc[:,len(target.columns):].transpose()

################

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('TARGET_FILE')
    parser.add_argument('FEATURES_DIR')
    parser.add_argument('OUT_FILE')
    parser.add_argument('--COLLAPSE_TARGET',default=False,action='store_true')
    args=parser.parse_args()

    df = count_overlaps(args.TARGET_FILE,args.FEATURES_DIR)
    if args.COLLAPSE_TARGET:
        print("collapsing...")
        df = df.sum(axis=1)

    # Write
    df.to_csv(args.OUT_FILE,sep='\t')

